from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.price_history import PriceHistory
from agent.search_agent import client

router = APIRouter()

@router.get("/predict/{product_id}")
def predict_price(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.recorded_at.asc())
        .all()
    )

    if len(history) < 3:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "recommendation": "not_enough_data",
            "message": "Need more price history to make a reliable prediction. Check back after a few more price updates.",
        }

    price_trend_text = "\n".join([
        f"{h.recorded_at.strftime('%Y-%m-%d')}: ₹{h.price}"
        for h in history
    ])

    prompt = f"""
You are a price trend analyst. Here is the price history for a product:

Product: {product.name}
Current price: ₹{product.current_price}

Price history (oldest to newest):
{price_trend_text}

Based on this trend, analyze whether the price is likely to drop soon, stay stable, or rise.

Respond ONLY with valid JSON in this exact format:
{{
  "recommendation": "buy_now" or "wait_a_few_days" or "wait_for_sale",
  "reasoning": "short 1-2 sentence explanation",
  "confidence": "low" or "medium" or "high"
}}
"""

    response = client.chat.completions.create(
        model="gemini-3.5-flash-lite",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_output = response.choices[0].message.content.strip()

    import json
    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "recommendation": "unknown",
            "message": "Could not generate a reliable prediction right now",
        }

    return {
        "product_id": product_id,
        "product_name": product.name,
        "current_price": product.current_price,
        "recommendation": result.get("recommendation"),
        "reasoning": result.get("reasoning"),
        "confidence": result.get("confidence"),
    }


@router.get("/buy-timing/{product_id}")
def buy_timing(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .all()
    )

    if not history:
        return {
            "product_id": product_id,
            "verdict": "unknown",
            "message": "Not enough price history yet to give a recommendation.",
        }

    prices = [h.price for h in history]
    lowest_price = min(prices)
    current_price = product.current_price
    gap = current_price - lowest_price

    if gap <= 3:
        verdict = "good_time"
        message = "It's a good time to buy"
    elif gap < 1000:
        verdict = "thinking"
        message = "You are thinking about what you will do, But it's not a good time to buy"
    else:
        verdict = "wait"
        message = "Wait patiently next time to buy"

    return {
        "product_id": product_id,
        "product_name": product.name,
        "current_price": current_price,
        "lowest_price": lowest_price,
        "price_gap": gap,
        "verdict": verdict,
        "message": message,
    }