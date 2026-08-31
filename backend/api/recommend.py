from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.product import Product
from agent.search_agent import client

router = APIRouter()

class RecommendRequest(BaseModel):
    message: str

@router.post("/recommend")
def get_recommendation(data: RecommendRequest, db: Session = Depends(get_db)):
    products = db.query(Product).limit(30).all()

    product_list_text = "\n".join([
        f"- {p.name} | Price: ₹{p.current_price} | Rating: {p.rating} | In stock: {bool(p.in_stock)}"
        for p in products
    ]) or "No products currently in database."

    prompt = f"""
You are a helpful shopping assistant. A user is asking for a product recommendation.

Available products in our database:
{product_list_text}

User's request: "{data.message}"

Based on the available products, give a short, friendly recommendation (2-4 sentences).
If none of the available products fit well, say so honestly and suggest what to search for instead.
Do not make up products that aren't in the list above.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
    )

    reply = response.choices[0].message.content.strip()

    return {
        "user_message": data.message,
        "recommendation": reply,
    }