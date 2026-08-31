from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class StockStatus(Base):
    __tablename__ = "stock_status"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    is_in_stock = Column(Boolean, default=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())