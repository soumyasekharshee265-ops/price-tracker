from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.product import Product
from models.stock_status import StockStatus

router = APIRouter()

class StockAlertCreate(BaseModel):
    product_id: int

@router.post("/stock-alerts")
def create_stock_alert(data: StockAlertCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    log_entry = StockStatus(
        product_id=product.id,
        is_in_stock=bool(product.in_stock),
    )
    db.add(log_entry)
    db.commit()

    return {
        "message": "Now tracking stock status for this product",
        "product_name": product.name,
        "currently_in_stock": bool(product.in_stock),
    }

@router.get("/stock-status/{product_id}")
def get_stock_status(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    history = (
        db.query(StockStatus)
        .filter(StockStatus.product_id == product_id)
        .order_by(StockStatus.checked_at.desc())
        .limit(10)
        .all()
    )

    return {
        "product_id": product_id,
        "product_name": product.name,
        "currently_in_stock": bool(product.in_stock),
        "recent_checks": [
            {"in_stock": h.is_in_stock, "checked_at": h.checked_at.isoformat()}
            for h in history
        ],
    }