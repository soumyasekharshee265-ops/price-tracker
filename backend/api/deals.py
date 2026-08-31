from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.trending_deal import TrendingDeal

router = APIRouter()

CATEGORIES = [
    "Smartphones", "Laptops", "Headphones", "Smart TVs",
    "Refrigerators", "Washing Machines", "Air Conditioners",
    "Water Purifiers", "Smart Watches", "Cameras",
    "Speakers", "Kitchen Appliances",
]

@router.get("/deals")
def get_deals(
    category: Optional[str] = None,
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(TrendingDeal)

    if category and category != "All":
        query = query.filter(TrendingDeal.category == category)

    deals = query.order_by(TrendingDeal.discount_percent.desc().nullslast()).limit(limit).all()

    return {
        "category": category or "All",
        "total": len(deals),
        "categories": CATEGORIES,
        "deals": [
            {
                "id": d.id,
                "category": d.category,
                "title": d.title,
                "price": d.price,
                "original_price": d.original_price,
                "discount_percent": d.discount_percent,
                "rating": d.rating,
                "image_url": d.image_url,
                "source_url": d.source_url,
                "platform": d.platform,
            }
            for d in deals
        ],
    }


@router.get("/deals/under/{max_price}")
def get_deals_under_price(
    max_price: float,
    min_price: float = Query(0),
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db),
):
    deals = (
        db.query(TrendingDeal)
        .filter(TrendingDeal.price > min_price, TrendingDeal.price <= max_price)
        .order_by(TrendingDeal.discount_percent.desc().nullslast(), TrendingDeal.price.asc())
        .limit(limit)
        .all()
    )

    return {
        "min_price": min_price,
        "max_price": max_price,
        "total": len(deals),
        "deals": [
            {
                "id": d.id,
                "category": d.category,
                "title": d.title,
                "price": d.price,
                "original_price": d.original_price,
                "discount_percent": d.discount_percent,
                "rating": d.rating,
                "image_url": d.image_url,
                "source_url": d.source_url,
                "platform": d.platform,
            }
            for d in deals
        ],
    }


@router.get("/deals/discount/{min_percent}")
def get_deals_by_discount(
    min_percent: float,
    max_percent: Optional[float] = None,
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(TrendingDeal).filter(TrendingDeal.discount_percent >= min_percent)
    if max_percent is not None:
        query = query.filter(TrendingDeal.discount_percent < max_percent)

    deals = query.order_by(TrendingDeal.discount_percent.desc()).limit(limit).all()

    return {
        "min_percent": min_percent,
        "max_percent": max_percent,
        "total": len(deals),
        "deals": [
            {
                "id": d.id,
                "category": d.category,
                "title": d.title,
                "price": d.price,
                "original_price": d.original_price,
                "discount_percent": d.discount_percent,
                "rating": d.rating,
                "image_url": d.image_url,
                "source_url": d.source_url,
                "platform": d.platform,
            }
            for d in deals
        ],
    }