from database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    db.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE"))
    db.commit()
    print("Done — products and everything referencing them (price history, stock status, alerts, coupons, etc.) have been cleared.")
finally:
    db.close()