from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.price_history import PriceHistory

router = APIRouter()

@router.get("/fake-discount/{product_id}")
def check_fake_discount(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product.original_price or not product.current_price:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "verdict": "unknown",
            "message": "Not enough price data to check for a fake discount",
        }

    claimed_discount_percent = round(
        ((product.original_price - product.current_price) / product.original_price) * 100, 1
    )

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .all()
    )

    if not history:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "verdict": "unknown",
            "claimed_discount_percent": claimed_discount_percent,
            "message": "No price history yet to verify this discount",
        }

    prices = [h.price for h in history]
    highest_recorded_price = max(prices)

    if product.original_price > highest_recorded_price * 1.1:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "verdict": "fake_discount",
            "claimed_discount_percent": claimed_discount_percent,
            "highest_recorded_price": highest_recorded_price,
            "message": f"Claimed original price (₹{product.original_price}) is higher than any price we've actually recorded (₹{highest_recorded_price})",
        }

    return {
        "product_id": product_id,
        "product_name": product.name,
        "verdict": "genuine_discount",
        "claimed_discount_percent": claimed_discount_percent,
        "highest_recorded_price": highest_recorded_price,
        "message": "This discount appears genuine based on recorded price history",
    }