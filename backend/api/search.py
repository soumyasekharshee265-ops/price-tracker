from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.price_history import PriceHistory
from agent.search_agent import search_and_extract

router = APIRouter()

@router.get("/search")
def search_products(query: str, db: Session = Depends(get_db)):
    results = search_and_extract(query)

    saved_products = []

    for item in results:
        if "error" in item:
            continue

        if item.get("price") is None or item.get("title") is None:
            continue

        price = item.get("price")
        original_price = item.get("original_price")

        if original_price is not None and price > original_price:
            continue

        if original_price is not None and price == original_price:
            item["original_price"] = None

        if price <= 0:
            continue

        existing = db.query(Product).filter(Product.url == item["source_url"]).first()

        if existing:
            existing.current_price = item["price"]
            existing.rating = item.get("rating")
            existing.in_stock = 1 if item.get("in_stock") else 0
            product = existing
        else:
            product = Product(
                name=item["title"],
                url=item["source_url"],
                source=item.get("platform", "web"),
                image_url=item.get("image_url"),
                current_price=item["price"],
                original_price=item.get("original_price"),
                rating=item.get("rating"),
                in_stock=1 if item.get("in_stock") else 0,
            )
            db.add(product)
            db.flush()

        history_entry = PriceHistory(
            product_id=product.id,
            price=item["price"],
        )
        db.add(history_entry)

        item["product_id"] = product.id
        saved_products.append(item)

    db.commit()

    return {
        "query": query,
        "total_found": len(results),
        "total_saved": len(saved_products),
        "results": results,
    }