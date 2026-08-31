from database import SessionLocal
from models.product import Product

db = SessionLocal()

try:
    products = db.query(Product).order_by(Product.created_at.asc()).all()
    print(f"\nTotal products in database: {len(products)}\n")
    for p in products:
        print(f"[{p.id}] ({p.source}) {p.name[:70]}")
finally:
    db.close()