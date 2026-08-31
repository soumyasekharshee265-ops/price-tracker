from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product

router = APIRouter()

@router.get("/compare")
def compare_products(query: str, db: Session = Depends(get_db)):
    matches = (
        db.query(Product)
        .filter(Product.name.ilike(f"%{query}%"))
        .all()
    )

    if not matches:
        return {
            "query": query,
            "total_found": 0,
            "products": [],
            "message": "No matching products found in database. Try searching first.",
        }

    comparison = []
    for product in matches:
        comparison.append({
            "id": product.id,
            "name": product.name,
            "source": product.source,
            "current_price": product.current_price,
            "original_price": product.original_price,
            "rating": product.rating,
            "in_stock": bool(product.in_stock),
            "url": product.url,
            "image_url": product.image_url,
        })

    comparison.sort(key=lambda p: p["current_price"])

    best_price = comparison[0]

    return {
        "query": query,
        "total_found": len(comparison),
        "best_price_option": {
            "name": best_price["name"],
            "source": best_price["source"],
            "price": best_price["current_price"],
        },
        "products": comparison,
    }