from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        locale="en-IN",
    )
    page = context.new_page()

    page.goto("https://www.flipkart.com/search?q=Smart+Watches", timeout=20000)
    page.wait_for_selector("div.p0C73x", timeout=15000)

    cards = page.query_selector_all("div.p0C73x")

    card = cards[4] 
    card.scroll_into_view_if_needed()
    page.wait_for_timeout(2000) 

    img_count_after_wait = len(card.query_selector_all("img"))
    print(f"imgs after extra wait: {img_count_after_wait}", flush=True)

    html = card.evaluate("el => el.outerHTML")
    print("--- Card HTML (first 2500 chars) ---", flush=True)
    print(html[:2500], flush=True)

    browser.close()