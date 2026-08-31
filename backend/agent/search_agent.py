import os
import re
import json
import time
import requests
from urllib.parse import urlparse
from ddgs import DDGS
from openai import OpenAI, RateLimitError
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from agent.prompts import EXTRACTION_PROMPT
from ddgs.exceptions import DDGSException
from playwright.sync_api import sync_playwright

load_dotenv()

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", 
)
MODEL_NAME = "llama3.2"

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

EMPTY_PRODUCT = {
    "title": None, "price": None, "original_price": None, "discount_percent": None,
    "rating": None, "num_ratings": None, "in_stock": None, "image_url": None,
    "source_url": None, "platform": None,
}


def _parse_amazon_price(text):
    """Amazon shows prices like '₹1,299'. This handles plain text price strings."""
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def search_amazon(query, max_results=5, headless=True):
    """Scrapes Amazon India search results using a real browser via Playwright.
    Replaces the old OpenWeb Ninja API call — no key, no rate limit."""
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
            page.goto(search_url, timeout=20000)
            page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=15000)

            cards = page.query_selector_all('div[data-component-type="s-search-result"]')

            for card in cards[:max_results]:
                link_el = card.query_selector("a.s-line-clamp-2") or card.query_selector("h2 a")
                relative_url = link_el.get_attribute("href") if link_el else None
                source_url = f"https://www.amazon.in{relative_url}" if relative_url else None
                if source_url:
                    source_url = resolve_final_url(source_url)

                price_el = card.query_selector("span.a-price > span.a-offscreen")
                price = _parse_amazon_price(price_el.inner_text()) if price_el else None

                original_price_el = card.query_selector("span.a-price.a-text-price > span.a-offscreen")
                original_price = _parse_amazon_price(original_price_el.inner_text()) if original_price_el else None

                rating_el = card.query_selector("span.a-icon-alt")
                rating = None
                if rating_el:
                    match = re.search(r"[\d.]+", rating_el.inner_text())
                    rating = float(match.group()) if match else None

                image_el = card.query_selector("img.s-image")
                image_url = image_el.get_attribute("src") if image_el else None
                image_alt = image_el.get_attribute("alt") if image_el else None

                title_el = card.query_selector("h2 span")
                selector_title = title_el.inner_text().strip() if title_el else None

                if image_alt and (not selector_title or len(image_alt.strip()) > len(selector_title)):
                    title = image_alt.strip()
                else:
                    title = selector_title

                if not title or not source_url or price is None:
                    continue

                discount_percent = None
                if original_price and original_price > price:
                    discount_percent = round((1 - price / original_price) * 100, 1)

                results.append({
                    **EMPTY_PRODUCT,
                    "title": title,
                    "price": price,
                    "original_price": original_price,
                    "discount_percent": discount_percent,
                    "rating": rating,
                    "num_ratings": None,
                    "in_stock": True,
                    "image_url": image_url,
                    "source_url": source_url,
                    "platform": "amazon",
                })

        except Exception as e:
            return [{"error": "amazon_scrape_failed", "message": str(e)}]
        finally:
            browser.close()

    return results


def resolve_final_url(url):
    """Follow redirects to turn short links (e.g. amzn.in/d/xxxx) into the
    real canonical product URL that contains the ASIN."""
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=10, allow_redirects=True)
        return response.url
    except Exception:
        return url


def extract_asin_from_url(url):
    match = re.search(r"/(?:dp|gp/product|product)/([A-Z0-9]{10})", url, re.IGNORECASE)
    return match.group(1).upper() if match else None


def get_amazon_product_by_url(url, headless=True):
    """Fetch a single Amazon product directly from its own product page via
    Playwright — no API. Resolves short links (amzn.in / amzn.to) first."""
    resolved_url = resolve_final_url(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            page.goto(resolved_url, timeout=20000)
            page.wait_for_selector("#productTitle", timeout=15000)

            title_el = page.query_selector("#productTitle")
            title = title_el.inner_text().strip() if title_el else None

            price_el = page.query_selector("span.a-price > span.a-offscreen")
            price = _parse_amazon_price(price_el.inner_text()) if price_el else None

            original_price_el = page.query_selector("span.a-price.a-text-price > span.a-offscreen")
            original_price = _parse_amazon_price(original_price_el.inner_text()) if original_price_el else None

            rating_el = page.query_selector("span.a-icon-alt")
            rating = None
            if rating_el:
                match = re.search(r"[\d.]+", rating_el.inner_text())
                rating = float(match.group()) if match else None

            image_el = page.query_selector("#landingImage")
            image_url = image_el.get_attribute("src") if image_el else None

            if not title or price is None:
                return None

            discount_percent = None
            if original_price and original_price > price:
                discount_percent = round((1 - price / original_price) * 100, 1)

            return {
                **EMPTY_PRODUCT,
                "title": title,
                "price": price,
                "original_price": original_price,
                "discount_percent": discount_percent,
                "rating": rating,
                "num_ratings": None,
                "in_stock": True,
                "image_url": image_url,
                "source_url": resolved_url,
                "platform": "amazon",
            }

        except Exception:
            return None
        finally:
            browser.close()


def _parse_flipkart_price(text):
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


FLIPKART_BADGE_IMAGE_MARKERS = ("static-assets-web.flixcart.com", "fk-p-linchpin-web")


def _extract_flipkart_product_image(card):
    """Flipkart cards sometimes have a small trust-badge <img> (e.g.
    'Flipkart Assured') BEFORE the real product photo in the DOM, so
    grabbing the first <img> can return the badge instead of the product.
    Also, Flipkart lazy-loads images — the real photo can sit in
    data-src while src still holds a placeholder. This checks every
    <img> in the card and returns the first one that looks like a real
    product photo, preferring data-src over src."""
    for img_el in card.query_selector_all("img"):
        candidate = img_el.get_attribute("data-src") or img_el.get_attribute("src")
        if not candidate:
            continue
        if any(marker in candidate for marker in FLIPKART_BADGE_IMAGE_MARKERS):
            continue 
        return candidate
    return None


def search_flipkart(query, max_results=5, headless=True):
    """Scrapes Flipkart search results using a real browser via Playwright.
    Replaces the old QuickCommerceAPI call — no key, no rate limit."""
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}"
            page.goto(search_url, timeout=20000)

            try:
                page.wait_for_selector("div.p0C73x", timeout=8000)
                cards = page.query_selector_all("div.p0C73x")

                
                page.mouse.wheel(0, 2500)
                page.wait_for_timeout(1500)
            except Exception:
                cards = []

            for card in cards[:max_results]:
                card.scroll_into_view_if_needed()
                page.wait_for_timeout(400)

                link_el = card.query_selector("a.atJtCj")
                title = link_el.get_attribute("title") if link_el else None
                relative_url = link_el.get_attribute("href") if link_el else None
                source_url = f"https://www.flipkart.com{relative_url}" if relative_url else None

                price_el = card.query_selector("div.hZ3P6w")
                price = _parse_flipkart_price(price_el.inner_text()) if price_el else None

                original_price_el = card.query_selector("div.kRYCnD")
                original_price = _parse_flipkart_price(original_price_el.inner_text()) if original_price_el else None

                discount_el = card.query_selector("div.HQe8jr span")
                discount_percent = None
                if discount_el:
                    match = re.search(r"[\d.]+", discount_el.inner_text())
                    discount_percent = float(match.group()) if match else None

                rating_el = card.query_selector("div.MKiFS6")
                rating = None
                if rating_el:
                    match = re.search(r"[\d.]+", rating_el.inner_text())
                    rating = float(match.group()) if match else None

                image_url = _extract_flipkart_product_image(card)

                if not title or not source_url or price is None:
                    continue

                results.append({
                    **EMPTY_PRODUCT,
                    "title": title,
                    "price": price,
                    "original_price": original_price,
                    "discount_percent": discount_percent,
                    "rating": rating,
                    "num_ratings": None,
                    "in_stock": True,
                    "image_url": image_url,
                    "source_url": source_url,
                    "platform": "flipkart",
                })

            if not results:
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                page_text = soup.get_text(separator=" ", strip=True)[:4000]

                ai_data = extract_product_data_ai(page_text)
                if isinstance(ai_data, dict) and "error" not in ai_data:
                    results.append({
                        **EMPTY_PRODUCT,
                        **ai_data,
                        "source_url": search_url,
                        "platform": "flipkart",
                    })

        except Exception as e:
            return [{"error": "flipkart_scrape_failed", "message": str(e)}]
        finally:
            browser.close()

    return results


def _parse_croma_price(text):
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def search_croma(query, max_results=5, headless=True):
    """Scrapes Croma search results using a real browser via Playwright."""
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            page.goto("https://www.croma.com/", timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            close_btn = page.query_selector("#close")
            if close_btn:
                close_btn.click()
            page.wait_for_timeout(1000)

            search_box = page.locator("input[name='search']").nth(1)
            search_box.click()
            search_box.fill(query)
            search_box.press("Enter")
            page.wait_for_selector("li.product-item", timeout=15000)
            page.wait_for_timeout(1000)

            cards = page.query_selector_all("li.product-item")

            for card in cards[:max_results]:
                link_el = card.query_selector("a[href*='/p/']")
                relative_url = link_el.get_attribute("href") if link_el else None
                source_url = f"https://www.croma.com{relative_url}" if relative_url else None

                image_el = card.query_selector("img")
                title = image_el.get_attribute("title") or image_el.get_attribute("alt") if image_el else None
                image_url = image_el.get_attribute("data-src") or image_el.get_attribute("src") if image_el else None

                price_el = card.query_selector("div.new-price span.amount")
                price = _parse_croma_price(price_el.inner_text()) if price_el else None

                original_price_el = card.query_selector("span.old-price span.amount")
                original_price = _parse_croma_price(original_price_el.inner_text()) if original_price_el else None

                discount_el = card.query_selector("span.discount")
                discount_percent = None
                if discount_el:
                    match = re.search(r"[\d.]+", discount_el.inner_text())
                    discount_percent = float(match.group()) if match else None

                rating_el = card.query_selector("span.rating-text")
                rating = None
                if rating_el:
                    match = re.search(r"[\d.]+", rating_el.inner_text())
                    rating = float(match.group()) if match else None

                if not title or not source_url or price is None:
                    continue

                results.append({
                    **EMPTY_PRODUCT,
                    "title": title,
                    "price": price,
                    "original_price": original_price,
                    "discount_percent": discount_percent,
                    "rating": rating,
                    "num_ratings": None,
                    "in_stock": True,
                    "image_url": image_url,
                    "source_url": source_url,
                    "platform": "croma",
                })

        except Exception as e:
            return [{"error": "croma_scrape_failed", "message": str(e)}]
        finally:
            browser.close()

    return results


def _parse_myntra_price(text):
    if not text:
        return None
    text = re.sub(r"Rs\.?", "", text)  
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def search_myntra(query, max_results=5, headless=True):
    """Scrapes Myntra search results using a real browser via Playwright."""
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            search_url = f"https://www.myntra.com/{query.replace(' ', '+')}"
            page.goto(search_url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_selector("li.product-base", timeout=15000)

            cards = page.query_selector_all("li.product-base")

            for card in cards[:max_results]:
                brand_el = card.query_selector("h3.product-brand")
                name_el = card.query_selector("h4.product-product")
                brand = brand_el.inner_text().strip() if brand_el else ""
                name = name_el.inner_text().strip() if name_el else ""
                title = f"{brand} {name}".strip() or None

                link_el = card.query_selector("a")
                relative_url = link_el.get_attribute("href") if link_el else None
                source_url = f"https://www.myntra.com/{relative_url}" if relative_url else None

                price_el = card.query_selector("span.product-discountedPrice")
                price = _parse_myntra_price(price_el.inner_text()) if price_el else None

                original_price_el = card.query_selector("span.product-strike")
                original_price = _parse_myntra_price(original_price_el.inner_text()) if original_price_el else None

                discount_el = card.query_selector("span.product-discountPercentage")
                discount_percent = None
                if discount_el:
                    match = re.search(r"[\d.]+", discount_el.inner_text())
                    discount_percent = float(match.group()) if match else None

                rating_container = card.query_selector("div.product-ratingsContainer")
                rating = None
                if rating_container:
                    rating_span = rating_container.query_selector("span")
                    if rating_span:
                        match = re.search(r"[\d.]+", rating_span.inner_text())
                        rating = float(match.group()) if match else None

                image_el = card.query_selector("img")
                image_url = image_el.get_attribute("src") if image_el else None

                if not title or not source_url or price is None:
                    continue

                results.append({
                    **EMPTY_PRODUCT,
                    "title": title,
                    "price": price,
                    "original_price": original_price,
                    "discount_percent": discount_percent,
                    "rating": rating,
                    "num_ratings": None,
                    "in_stock": True,
                    "image_url": image_url,
                    "source_url": source_url,
                    "platform": "myntra",
                })

        except Exception as e:
            return [{"error": "myntra_scrape_failed", "message": str(e)}]
        finally:
            browser.close()

    return results

def get_flipkart_product_by_url(url):
    """Fetch a single Flipkart product via the generic scrape+AI pipeline —
    Flipkart's product-page CSS classes are auto-generated and reused across
    unrelated elements, making hand-picked selectors unreliable. JSON-LD +
    AI extraction is more robust here."""
    return extract_product_from_url(url, platform="flipkart")



def extract_jsonld_data(soup):
    data = {}
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            raw = json.loads(script.string)
        except (TypeError, json.JSONDecodeError):
            continue

        candidates = raw if isinstance(raw, list) else [raw]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            nodes = item.get("@graph", [item])
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                if node.get("@type") not in ("Product", "http://schema.org/Product"):
                    continue

                if node.get("name"):
                    data["title"] = node["name"]

                image = node.get("image")
                if image:
                    data["image_url"] = image[0] if isinstance(image, list) else image

                offers = node.get("offers")
                if offers:
                    offer = offers[0] if isinstance(offers, list) else offers
                    if offer.get("price"):
                        try:
                            data["price"] = float(offer["price"])
                        except (TypeError, ValueError):
                            pass
                    avail = offer.get("availability", "")
                    if avail:
                        data["in_stock"] = "InStock" in avail

                rating = node.get("aggregateRating")
                if rating:
                    try:
                        data["rating"] = float(rating.get("ratingValue"))
                    except (TypeError, ValueError):
                        pass
    return data


def fetch_page_text(url):
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        jsonld_data = extract_jsonld_data(soup)
        image_url = jsonld_data.get("image_url")

        if not image_url:
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                image_url = og_image["content"]

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:4000], image_url, jsonld_data
    except Exception:
        return None, None, {}

def scrape_product_page_playwright(url, headless=True):
    """Loads a product page in a real browser (so JS-rendered content actually
    appears), then extracts the same things fetch_page_text() did:
    JSON-LD structured data, og:image, and visible page text for AI cleanup.
    Used for Meesho, Croma, Myntra, and any other site that doesn't work
    with a plain requests.get(). Also returns the final resolved URL, since
    short share-links (like dl.flipkart.com) redirect to the real product
    page after loading."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            locale="en-IN",
        )
        page = context.new_page()

        try:
            page.goto(url, timeout=20000)
            if "dl.flipkart.com" in url:
                try:
                    page.wait_for_url(lambda u: "flipkart.com" in u and "/p/" in u, timeout=10000)
                except Exception:
                    pass

            page.wait_for_timeout(2500) 

            final_url = page.url

            if "flipkart.com" in final_url and "/p/" not in final_url:
                return None, None, {}, url

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            jsonld_data = extract_jsonld_data(soup)
            image_url = jsonld_data.get("image_url")

            if not image_url:
                og_image = soup.find("meta", property="og:image")
                if og_image and og_image.get("content"):
                    image_url = og_image["content"]

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            return text[:4000], image_url, jsonld_data, final_url

        except Exception:
            return None, None, {}, url
        finally:
            browser.close()

def _title_grounded_in_source(title, source_text):
    """Guards against hallucination: checks that the AI's extracted title
    actually came from the page text it was given, not invented. At least
    half the title's meaningful words (3+ letters) must literally appear
    in the source text."""
    if not title or not source_text:
        return False
    title_words = [w for w in re.findall(r"[a-zA-Z0-9]+", title.lower()) if len(w) >= 3]
    if not title_words:
        return False
    source_lower = source_text.lower()
    matched = sum(1 for w in title_words if w in source_lower)
    return matched >= max(1, len(title_words) // 2)

def extract_product_data_ai(page_text, jsonld_data=None, max_retries=2):
    jsonld_data = jsonld_data or {}
    if not page_text:
        return {"error": "fetch_failed"}

    prompt = EXTRACTION_PROMPT.format(content=page_text)
    last_raw = None

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,   
                temperature=0,    
            )
            raw_output = response.choices[0].message.content.strip()
            last_raw = raw_output

            try:
                ai_data = json.loads(raw_output)
            except json.JSONDecodeError:
                continue  

            merged = {**ai_data, **{k: v for k, v in jsonld_data.items() if v is not None}}

            if merged.get("title") and not _title_grounded_in_source(merged["title"], page_text):
                continue 

            return merged if merged else {"error": "invalid_json", "raw": raw_output}

        except RateLimitError:
            time.sleep(5 * (attempt + 1))

    return {"error": "extraction_failed", "raw": last_raw}


def extract_product_from_url(url, platform=None):
    page_text, image_url, jsonld_data, final_url = scrape_product_page_playwright(url)

    if page_text is None:
        return {"error": "scrape_failed", "source_url": url, "platform": platform}

    data = extract_product_data_ai(page_text, jsonld_data)
    if "error" in data:
        data["source_url"] = final_url
        data["platform"] = platform
        return data

    result = {**EMPTY_PRODUCT, **data}
    result["source_url"] = final_url
    result["platform"] = platform or urlparse(final_url).netloc.replace("www.", "").split(".")[0]
    if image_url and not result.get("image_url"):
        result["image_url"] = image_url
    return result


def search_meesho(query, max_results=3):
    urls = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(f"{query} site:meesho.com", max_results=max_results):
                urls.append(r["href"])
    except DDGSException:
        pass

    return [extract_product_from_url(url, platform="meesho") for url in urls]



def is_url(text):
    text = text.strip()
    return text.startswith("http://") or text.startswith("https://")


def _identify_and_fetch(url):
    """Get the single pasted product's own data first."""
    domain = urlparse(url).netloc.lower()

    if "amazon." in domain or "amzn." in domain:
        resolved_url = resolve_final_url(url)
        product = get_amazon_product_by_url(resolved_url)
        if product:
            return product
        return extract_product_from_url(resolved_url, platform="amazon")

    if "flipkart." in domain:
        return get_flipkart_product_by_url(url)

    platform = domain.replace("www.", "").split(".")[0]
    return extract_product_from_url(url, platform=platform)


def search_by_url(url):
    anchor_product = _identify_and_fetch(url.strip())
    title = anchor_product.get("title") if isinstance(anchor_product, dict) else None
    anchor_src = anchor_product.get("source_url") if isinstance(anchor_product, dict) else None
    anchor_platform = anchor_product.get("platform") if isinstance(anchor_product, dict) else None

    other_results = []
    if title:
        for platform in get_relevant_platforms(title):
            if platform == anchor_platform:
                continue 
            search_fn = PLATFORM_SEARCH_FUNCTIONS.get(platform)
            if search_fn:
                other_results.extend(search_fn(title, max_results=3))

    seen = {_normalize_url(anchor_src)} if anchor_src else set()
    deduped = []
    for r in other_results:
        src = r.get("source_url") if isinstance(r, dict) else None
        if src:
            norm = _normalize_url(src)
            if norm in seen:
                continue
            seen.add(norm)
        deduped.append(r)

    same_product_matches = filter_same_product(deduped, title) if title else deduped

    return [anchor_product] + same_product_matches


def sort_by_price(results):
    """Cheapest first. Items with no usable price (errors, nulls) go last,
    in their original relative order."""
    priced = [r for r in results if isinstance(r, dict) and r.get("price") is not None]
    unpriced = [r for r in results if not (isinstance(r, dict) and r.get("price") is not None)]
    priced.sort(key=lambda r: r["price"])
    return priced + unpriced


def _tokenize(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


ACCESSORY_WORDS = {
    "case", "cover", "tempered", "glass", "protector", "skin", "pouch",
    "strap", "guard", "cable", "charger", "adapter", "holder", "stand",
    "screenguard", "screenprotector", "backcover", "flipcover",
}


def _relevance_score(query, title):
    """How well a result's title matches the search query. Every shared word
    counts, but words containing digits (model numbers like 'A78', '5G')
    count double, since those are usually what actually pins down the exact
    product — 'Oppo' alone matches every Oppo product ever made.

    Accessory listings (cases, covers, chargers...) often share the exact
    brand and model number with the real product, which would otherwise let
    a ₹499 phone case outrank the ₹19,000 phone it's made for. If the title
    mentions an accessory word the query itself never asked for, it's
    treated as a mismatch regardless of word overlap."""
    query_tokens = _tokenize(query)
    title_tokens = _tokenize(title)
    if not query_tokens:
        return 0

    if title_tokens & ACCESSORY_WORDS and not (query_tokens & ACCESSORY_WORDS):
        return 0

    score = 0
    for token in query_tokens:
        if token in title_tokens:
            score += 2 if any(ch.isdigit() for ch in token) else 1
    return score


def sort_by_relevance(results, anchor_text):
    """Scores every result by how many query words its title actually
    contains (model-number words count double), so a search for 'Oppo A78 5G'
    ranks real A78 listings above generic Oppo accessories or other brands
    entirely. Only results that clear half the best score seen count as
    genuine matches — and among those, only ones with a real photo and link
    are eligible for the top of the list, sorted by price first and rating
    as the tiebreaker. Weak (but non-zero) matches still show up, pushed
    below the real matches. Results with ZERO word overlap with the query
    (e.g. a completely different brand/product) are dropped entirely —
    they're not a "weaker match", they're unrelated."""
    if not anchor_text:
        return sort_by_price(results)

    valid = [r for r in results if isinstance(r, dict) and "error" not in r]
    invalid = [r for r in results if not (isinstance(r, dict) and "error" not in r)]

    scored = [(r, _relevance_score(anchor_text, r.get("title"))) for r in valid]
    max_score = max((s for _, s in scored), default=0)
    threshold = max(1, max_score / 2)

    strong = [r for r, s in scored if s >= threshold]
    weak = [r for r, s in scored if 0 < s < threshold]


    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

    def has_photo_and_url(r):
        image_url = r.get("image_url") or ""
        source_url = r.get("source_url") or ""
        looks_like_image = image_url.lower().split("?")[0].endswith(IMAGE_EXTENSIONS)
        looks_like_product_link = source_url.startswith("http") and "/search?" not in source_url
        return looks_like_image and looks_like_product_link

    complete = [r for r in strong if has_photo_and_url(r)]
    incomplete = [r for r in strong if not has_photo_and_url(r)]

    def best_deal_key(r):
        price = r.get("price")
        rating = r.get("rating") or 0
        return (price if price is not None else float("inf"), -rating)

    complete_sorted = sorted(complete, key=best_deal_key)

    return complete_sorted + sort_by_price(incomplete) + sort_by_price(weak) + invalid



CATEGORY_KEYWORDS = {
    "electronics": [
        "laptop", "mobile", "phone", "smartphone", "tv", "television",
        "fridge", "refrigerator", "air conditioner", "washing machine",
        "camera", "headphone", "earphone", "earbuds", "speaker",
        "smartwatch", "tablet", "charger", "router", "printer", "monitor",
        "microwave", "power bank", "keyboard", "mouse",
    ],
    "fashion": [
        "shirt", "t-shirt", "tshirt", "jeans", "dress", "kurta", "saree",
        "jacket", "shoes", "sneakers", "sandals", "heels", "handbag",
        "wallet", "belt", "sunglasses", "trouser", "jogger", "hoodie",
        "top", "salwar", "lehenga",
    ],
    "beauty": [
        "lipstick", "foundation", "makeup", "skincare", "serum",
        "moisturizer", "sunscreen", "perfume", "fragrance", "shampoo",
        "conditioner", "kajal", "mascara", "nail polish", "face wash",
        "cream", "lotion", "compact", "concealer", "eyeliner", "primer",
    ],
}

PLATFORM_CATEGORIES = {
    "myntra": {"fashion", "beauty"},
}

ALWAYS_SEARCH_PLATFORMS = ["amazon", "flipkart"]

PLATFORM_SEARCH_FUNCTIONS = {
    "amazon": search_amazon,
    "flipkart": search_flipkart,
    "myntra": search_myntra,
}


def classify_categories(text):
    text_lower = f" {(text or '').lower()} "
    matched = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lower):
                matched.add(category)
                break
    return matched


def get_relevant_platforms(text):
    categories = classify_categories(text)
    relevant = list(ALWAYS_SEARCH_PLATFORMS)
    for platform, platform_categories in PLATFORM_CATEGORIES.items():
        if platform_categories & categories:
            relevant.append(platform)
    return relevant



BRAND_STOPWORDS = {"the", "for", "with", "and", "of", "a", "an", "new"}


def _extract_brand_tokens(title, max_words=2):
    words = re.findall(r"[a-zA-Z0-9]+", (title or "").lower())
    words = [w for w in words if w not in BRAND_STOPWORDS]
    return words[:max_words]


def filter_same_product(results, anchor_title):
    """Keeps only cross-platform results that are genuinely the SAME
    product as the anchor — strong title overlap AND matching brand.
    Anything else (similar items, other brands, wrong category) is
    dropped entirely, not just ranked lower."""
    if not anchor_title:
        return sort_by_price(results)

    valid = [r for r in results if isinstance(r, dict) and "error" not in r]
    scored = [(r, _relevance_score(anchor_title, r.get("title"))) for r in valid]
    max_score = max((s for _, s in scored), default=0)
    threshold = max(2, max_score * 0.6) 

    anchor_brand = set(_extract_brand_tokens(anchor_title))

    matches = []
    for r, score in scored:
        if score < threshold:
            continue
        if anchor_brand and not (anchor_brand & _tokenize(r.get("title"))):
            continue
        matches.append(r)

    return sort_by_price(matches)


def _normalize_url(url):
    """Strips query-string/tracking params (utm_source, ref, etc.) so the
    same product URL with different tracking params doesn't count as two
    different products during dedup."""
    if not url:
        return url
    return url.split("?")[0].rstrip("/")


def search_and_extract(query, max_results=10):
    if is_url(query):
        return search_by_url(query)

    platforms = get_relevant_platforms(query)
    results = []
    for platform in platforms:
        search_fn = PLATFORM_SEARCH_FUNCTIONS.get(platform)
        if search_fn:
            results.extend(search_fn(query, max_results))
    return sort_by_relevance(results, query)