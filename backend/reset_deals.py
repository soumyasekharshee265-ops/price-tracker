from database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    db.execute(text("TRUNCATE TABLE trending_deals RESTART IDENTITY"))
    db.commit()
    print("Done — trending_deals table cleared.")
finally:
    db.close()