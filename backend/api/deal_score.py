from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.price_history import PriceHistory

router = APIRouter()

@router.get("/deal-score/{product_id}")
def get_deal_score(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .all()
    )

    score = 100
    reasons = []

    if len(history) >= 2:
        prices = [h.price for h in history]
        lowest_price = min(prices)
        highest_price = max(prices)

        if product.current_price > lowest_price:
            price_gap_percent = ((product.current_price - lowest_price) / lowest_price) * 100
            deduction = min(price_gap_percent, 40)
            score -= deduction
            reasons.append(f"Currently {round(price_gap_percent, 1)}% above lowest recorded price")
        else:
            reasons.append("Currently at or near the lowest recorded price")
    else:
        score -= 10
        reasons.append("Not enough price history yet for a trend-based score")

    if not product.rating:
        score -= 10
        reasons.append("No rating available")
    elif product.rating < 3.5:
        score -= 20
        reasons.append("Low product rating")
    elif product.rating >= 4.3:
        reasons.append("Highly rated product")

    if not product.in_stock:
        score -= 30
        reasons.append("Currently out of stock")

    score = max(0, min(100, round(score)))

    return {
        "product_id": product_id,
        "product_name": product.name,
        "deal_score": score,
        "reasons": reasons,
    }