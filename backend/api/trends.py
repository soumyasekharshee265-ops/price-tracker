from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models.product import Product
from models.price_history import PriceHistory

router = APIRouter()

@router.get("/trends/{product_id}")
def get_price_trends(product_id: int, days: int = 30, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    since_date = datetime.utcnow() - timedelta(days=days)

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .filter(PriceHistory.recorded_at >= since_date)
        .order_by(PriceHistory.recorded_at.asc())
        .all()
    )

    if not history:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "days": days,
            "message": "No price history yet for this range",
            "history": [],
        }


    daily_prices = {}
    for h in history:
        day_key = h.recorded_at.date()
        daily_prices[day_key] = {"price": h.price, "recorded_at": h.recorded_at}

    daily_history = sorted(daily_prices.values(), key=lambda x: x["recorded_at"])
    prices = [d["price"] for d in daily_history]

    return {
        "product_id": product_id,
        "product_name": product.name,
        "days": days,
        "highest_price": max(prices),
        "lowest_price": min(prices),
        "average_price": round(sum(prices) / len(prices), 2),
        "current_price": product.current_price,
        "data_points": len(daily_history),
        "history": [
            {"price": d["price"], "recorded_at": d["recorded_at"].isoformat()}
            for d in daily_history
        ],
    }