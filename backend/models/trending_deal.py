from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class TrendingDeal(Base):
    __tablename__ = "trending_deals"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    discount_percent = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    source_url = Column(String, nullable=False, unique=True)
    platform = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())