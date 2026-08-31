"""
Fills the trending_deals table gradually, a couple of categories/queries
per run, so we stay well within the free API quotas instead of hammering
them all at once. Run this as part of the scheduler alongside
price_refresher.

Two independent pools get refreshed each run:
- CATEGORIES: appliance/electronics categories, powers "Shop by Top
  Categories" on the homepage.
- BUDGET_QUERIES: low-priced generic items (accessories, jewelry, kitchen
  gadgets...), which naturally span ₹50–₹3000+ and are what populates the
  "Deals Under ₹X" price-bucket cards. These get their own category
  strings so they never mix into the appliance category list.
"""
from database import SessionLocal
from models.trending_deal import TrendingDeal
from agent.search_agent import search_amazon, search_flipkart, search_myntra, _normalize_url

CATEGORIES = [
    "Smartphones", "Laptops", "Headphones", "Smart TVs",
    "Refrigerators", "Washing Machines", "Air Conditioners",
    "Water Purifiers", "Smart Watches", "Cameras",
    "Speakers", "Kitchen Appliances",
]

BUDGET_QUERIES = [
    "mobile accessories", "kitchen gadgets", "keychain",
    "fashion jewelry", "sunglasses", "wallet", "stationery items",
    "hair accessories", "phone case", "travel accessories",
    "socks", "kitchen tools",
]

CATEGORIES_PER_RUN = 2        
PRODUCTS_PER_CATEGORY = 5     

BUDGET_PER_RUN = 2
PRODUCTS_PER_BUDGET_QUERY = 6  


def _get_next_items(db, all_items):
    """Pick the categories/queries with the fewest stored deals so far, so
    every one eventually gets filled instead of just the first few."""
    counts = {item: 0 for item in all_items}
    existing = db.query(TrendingDeal.category).all()
    for (cat,) in existing:
        if cat in counts:
            counts[cat] += 1

    return sorted(all_items, key=lambda c: counts[c])


def _save_results(db, category, results):
    added = 0
    for item in results:
        if "error" in item or not item.get("price") or not item.get("title"):
            continue
        source_url = item["source_url"]
        if "/search?" in source_url:
            continue

        normalized = _normalize_url(source_url)
        existing = (
            db.query(TrendingDeal)
            .filter(TrendingDeal.category == category)
            .all()
        )
        match = next(
            (d for d in existing if _normalize_url(d.source_url) == normalized),
            None,
        )

        if match:
            match.price = item["price"]
            match.original_price = item.get("original_price")
            match.discount_percent = item.get("discount_percent")
            match.rating = item.get("rating")
            if item.get("image_url"):
                match.image_url = item["image_url"]
            continue

        deal = TrendingDeal(
            category=category,
            title=item["title"],
            price=item["price"],
            original_price=item.get("original_price"),
            discount_percent=item.get("discount_percent"),
            rating=item.get("rating"),
            image_url=item.get("image_url"),
            source_url=source_url,
            platform=item.get("platform"),
        )
        db.add(deal)
        added += 1
    return added


def refresh_trending_deals():
    db = SessionLocal()
    added = 0

    try:
        categories = _get_next_items(db, CATEGORIES)[:CATEGORIES_PER_RUN]
        print(f"[deals] Refreshing categories: {categories}")

        for category in categories:
            results = []
            results.extend(search_amazon(category, max_results=PRODUCTS_PER_CATEGORY))
            results.extend(search_flipkart(category, max_results=PRODUCTS_PER_CATEGORY))
            added += _save_results(db, category, results)

        budget_items = _get_next_items(db, BUDGET_QUERIES)[:BUDGET_PER_RUN]
        print(f"[deals] Refreshing budget items: {budget_items}")

        for query in budget_items:
            results = []
            results.extend(search_amazon(query, max_results=PRODUCTS_PER_BUDGET_QUERY))
            results.extend(search_flipkart(query, max_results=PRODUCTS_PER_BUDGET_QUERY))
            results.extend(search_myntra(query, max_results=PRODUCTS_PER_BUDGET_QUERY))
            added += _save_results(db, query, results)

        db.commit()
        print(f"[deals] Added {added} new deals.")

    finally:
        db.close()


if __name__ == "__main__":
    refresh_trending_deals()