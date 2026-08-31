from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
from models.product import Product
from models.coupon import Coupon

router = APIRouter()

class CouponCreate(BaseModel):
    product_id: Optional[int] = None
    source: str
    code: str
    discount_description: Optional[str] = None
    expiry_date: Optional[datetime] = None

@router.post("/coupons")
def add_coupon(data: CouponCreate, db: Session = Depends(get_db)):
    if data.product_id:
        product = db.query(Product).filter(Product.id == data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

    new_coupon = Coupon(
        product_id=data.product_id,
        source=data.source,
        code=data.code,
        discount_description=data.discount_description,
        expiry_date=data.expiry_date,
    )
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return {
        "message": "Coupon added successfully",
        "coupon_id": new_coupon.id,
        "code": new_coupon.code,
    }

@router.get("/coupons/{product_id}")
def get_coupons_for_product(product_id: int, db: Session = Depends(get_db)):
    now = datetime.utcnow()

    product_coupons = (
        db.query(Coupon)
        .filter(Coupon.product_id == product_id)
        .filter((Coupon.expiry_date == None) | (Coupon.expiry_date >= now))
        .all()
    )

    sitewide_coupons = (
        db.query(Coupon)
        .filter(Coupon.product_id == None)
        .filter((Coupon.expiry_date == None) | (Coupon.expiry_date >= now))
        .all()
    )

    def format_coupon(c):
        return {
            "id": c.id,
            "source": c.source,
            "code": c.code,
            "discount_description": c.discount_description,
            "expiry_date": c.expiry_date.isoformat() if c.expiry_date else None,
        }

    return {
        "product_id": product_id,
        "product_specific_coupons": [format_coupon(c) for c in product_coupons],
        "sitewide_coupons": [format_coupon(c) for c in sitewide_coupons],
    }