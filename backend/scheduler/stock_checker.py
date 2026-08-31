from database import SessionLocal
from models.product import Product
from models.stock_status import StockStatus

def check_stock():
    db = SessionLocal()

    try:
        products = db.query(Product).all()
        changed_count = 0

        for product in products:
            latest_log = (
                db.query(StockStatus)
                .filter(StockStatus.product_id == product.id)
                .order_by(StockStatus.checked_at.desc())
                .first()
            )

            current_status = bool(product.in_stock)

            if not latest_log or latest_log.is_in_stock != current_status:
                new_log = StockStatus(
                    product_id=product.id,
                    is_in_stock=current_status,
                )
                db.add(new_log)
                changed_count += 1
                status_text = "back in stock" if current_status else "out of stock"
                print(f"[STOCK CHANGE] {product.name} is now {status_text}")

        db.commit()
        print(f"Stock check complete. {changed_count} status change(s) logged.")

    finally:
        db.close()

if __name__ == "__main__":
    check_stock()