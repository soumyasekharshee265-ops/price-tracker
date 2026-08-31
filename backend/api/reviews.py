from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import get_db
from models.review import Review

router = APIRouter()


class ReviewCreate(BaseModel):
    name: str
    email: str
    message: str
    rating: int = Field(ge=1, le=5)


@router.post("/reviews")
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    email = payload.email.strip()
    message = payload.message.strip()

    if not name or not email or not message:
        raise HTTPException(status_code=400, detail="All fields are required")

    entry = Review(name=name, email=email, message=message, rating=payload.rating)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "id": entry.id,
        "name": entry.name,
        "message": entry.message,
        "rating": entry.rating,
    }


@router.get("/reviews")
def list_reviews(limit: int = 30, db: Session = Depends(get_db)):
    entries = (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "total": len(entries),
        "reviews": [
            {"id": r.id, "name": r.name, "message": r.message, "rating": r.rating}
            for r in entries
        ],
    }