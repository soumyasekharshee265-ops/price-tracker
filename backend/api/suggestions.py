from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.suggestion import Suggestion

router = APIRouter()


class SuggestionCreate(BaseModel):
    name: str
    email: str
    suggestion: str


@router.post("/suggestions")
def create_suggestion(payload: SuggestionCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    email = payload.email.strip()
    text = payload.suggestion.strip()

    if not name or not email or not text:
        raise HTTPException(status_code=400, detail="All fields are required")

    entry = Suggestion(name=name, email=email, suggestion=text)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "id": entry.id,
        "name": entry.name,
        "suggestion": entry.suggestion,
    }


@router.get("/suggestions")
def list_suggestions(limit: int = 30, db: Session = Depends(get_db)):
    entries = (
        db.query(Suggestion)
        .order_by(Suggestion.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "total": len(entries),
        "suggestions": [
            {"id": s.id, "name": s.name, "suggestion": s.suggestion}
            for s in entries
        ],
    }