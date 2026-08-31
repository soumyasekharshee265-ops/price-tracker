from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    current_price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    in_stock = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())