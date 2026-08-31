from urllib.parse import urlparse
from database import SessionLocal
from models.product import Product
from models.price_history import PriceHistory
from agent.search_agent import (
    get_amazon_product_by_url,
    get_flipkart_product_by_url,
    extract_product_from_url,
)


def _safe_float(value):
    """AI extraction sometimes returns the literal string "null" (or other
    junk text) instead of a real null/None for numeric fields like rating.
    That string sails through json.loads() fine (it's valid JSON), but
    Postgres rejects it outright when saving to a numeric column, crashing
    the whole refresh cycle. This normalizes anything not cleanly
    convertible to a float into None instead."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_latest_data(url):
    """Route to the right lookup method based on the product's platform —
    same logic used when a product URL is first searched."""
    domain = urlparse(url).netloc.lower()

    if "amazon." in domain or "amzn." in domain:
        data = get_amazon_product_by_url(url)
        if data:
            return data
        return extract_product_from_url(url, platform="amazon")

    if "flipkart." in domain:
        return get_flipkart_product_by_url(url)

    platform = domain.replace("www.", "").split(".")[0]
    return extract_product_from_url(url, platform=platform)


def refresh_prices():
    db = SessionLocal()

    try:
        products = db.query(Product).all()
        updated_count = 0
        failed_count = 0

        for product in products:
            try:
                data = fetch_latest_data(product.url)

                if not data or "error" in data or data.get("price") is None:
                    failed_count += 1
                    print(f"[SKIP] Could not refresh: {product.name}")
                    continue

                safe_price = _safe_float(data["price"])
                if safe_price is None:
                    failed_count += 1
                    print(f"[SKIP] Invalid price for: {product.name}")
                    continue

                product.current_price = safe_price
                product.rating = _safe_float(data.get("rating"))
                if data.get("in_stock") is not None:
                    product.in_stock = 1 if data["in_stock"] else 0

                history_entry = PriceHistory(
                    product_id=product.id,
                    price=safe_price,
                )
                db.add(history_entry)
                db.commit()
                updated_count += 1

            except Exception as e:
                db.rollback()
                failed_count += 1
                print(f"[ERROR] Failed to refresh {product.name}: {e}")

        print(f"Price refresh complete. Updated: {updated_count}, Failed: {failed_count}")

    finally:
        db.close()