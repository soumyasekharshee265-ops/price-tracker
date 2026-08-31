"""
One-off script: finds every category/query in trending_deals that has at
least one row with a missing image_url, and re-scrapes just those —
instead of waiting for deals_refresher's slow 2-per-run rotation to
eventually reach them. Reuses deals_refresher's _save_results(), which
already updates image_url on existing rows when a fresh scrape finds one.
Run manually whenever you want stale "No image" rows fixed right away.
"""
from database import SessionLocal
from models.trending_deal import TrendingDeal
from agent.search_agent import search_amazon, search_flipkart, search_myntra
from scheduler.deals_refresher import _save_results, CATEGORIES, BUDGET_QUERIES

PRODUCTS_PER_CATEGORY = 5
PRODUCTS_PER_BUDGET_QUERY = 6


def backfill_missing_images():
    db = SessionLocal()
    updated = 0

    try:
        categories_missing_image = {
            cat for (cat,) in
            db.query(TrendingDeal.category)
            .filter(TrendingDeal.image_url.is_(None))
            .distinct()
            .all()
        }

        print(f"[backfill] Categories/queries with missing images: {categories_missing_image}")

        for category in categories_missing_image:
            results = []
            results.extend(search_amazon(category, max_results=PRODUCTS_PER_CATEGORY))
            results.extend(search_flipkart(category, max_results=PRODUCTS_PER_CATEGORY))

            
            if category in BUDGET_QUERIES:
                results.extend(search_myntra(category, max_results=PRODUCTS_PER_BUDGET_QUERY))

            updated += _save_results(db, category, results)

        db.commit()
        print(f"[backfill] Done. {updated} rows touched (new + image-updated).")

    finally:
        db.close()


if __name__ == "__main__":
    backfill_missing_images()