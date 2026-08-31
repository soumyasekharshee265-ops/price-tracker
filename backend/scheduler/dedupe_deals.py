"""
One-off cleanup: finds existing trending_deals rows that are actually the
same product (same category + same normalized source_url, ignoring
tracking params like ref=/qid=/iid=), and merges them into a single row —
keeping the one with the most complete data (has an image, has a rating)
and deleting the rest. Run manually whenever duplicates build up from
before the normalized-URL dedup fix.
"""
from database import SessionLocal
from models.trending_deal import TrendingDeal
from agent.search_agent import _normalize_url


def dedupe_deals():
    db = SessionLocal()
    removed = 0

    try:
        all_deals = db.query(TrendingDeal).all()

        groups = {}
        for deal in all_deals:
            key = (deal.category, _normalize_url(deal.source_url))
            groups.setdefault(key, []).append(deal)

        for key, deals in groups.items():
            if len(deals) <= 1:
                continue

            def completeness(d):
                return (d.image_url is not None, d.rating is not None)

            best = max(deals, key=completeness)
            for d in deals:
                if d.id != best.id:
                    db.delete(d)
                    removed += 1

        db.commit()
        print(f"[dedupe] Removed {removed} duplicate rows.")

    finally:
        db.close()


if __name__ == "__main__":
    dedupe_deals()