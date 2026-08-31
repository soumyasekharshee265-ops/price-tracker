from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    source = Column(String, nullable=False)
    code = Column(String, nullable=False)
    discount_description = Column(String, nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)