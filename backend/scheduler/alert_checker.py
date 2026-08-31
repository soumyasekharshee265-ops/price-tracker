from database import SessionLocal
from models.alert import Alert
from models.product import Product

def check_alerts():
    db = SessionLocal()

    try:
        active_alerts = db.query(Alert).filter(Alert.status == "active").all()

        triggered_count = 0

        for alert in active_alerts:
            product = db.query(Product).filter(Product.id == alert.product_id).first()

            if not product:
                continue

            current_price = product.current_price

            if alert.alert_type == "drop" and current_price <= alert.target_price:
                alert.status = "triggered"
                triggered_count += 1
                print(f"[DROP ALERT] {product.name} hit ₹{current_price} (target: ₹{alert.target_price})")

            elif alert.alert_type == "recovery" and current_price >= alert.target_price:
                alert.status = "triggered"
                triggered_count += 1
                print(f"[RECOVERY ALERT] {product.name} rose to ₹{current_price} (target: ₹{alert.target_price})")

        db.commit()
        print(f"Alert check complete. {triggered_count} alert(s) triggered.")

    finally:
        db.close()

if __name__ == "__main__":
    check_alerts()