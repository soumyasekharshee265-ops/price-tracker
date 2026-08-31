from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.product import Product
from models.alert import Alert

router = APIRouter()

class AlertCreate(BaseModel):
    product_id: int
    target_price: float
    alert_type: str  

@router.post("/alerts")
def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == alert_data.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if alert_data.alert_type not in ["drop", "recovery"]:
        raise HTTPException(status_code=400, detail="alert_type must be 'drop' or 'recovery'")

    new_alert = Alert(
        product_id=alert_data.product_id,
        target_price=alert_data.target_price,
        alert_type=alert_data.alert_type,
        status="active",
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return {
        "message": "Alert created successfully",
        "alert_id": new_alert.id,
        "product_name": product.name,
        "target_price": new_alert.target_price,
        "alert_type": new_alert.alert_type,
    }

@router.get("/alerts/{product_id}")
def get_alerts_for_product(product_id: int, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.product_id == product_id).all()

    return {
        "product_id": product_id,
        "total_alerts": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "target_price": a.target_price,
                "alert_type": a.alert_type,
                "status": a.status,
                "created_at": a.created_at.isoformat(),
            }
            for a in alerts
        ],
    }

@router.delete("/alerts/{alert_id}")
def cancel_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "cancelled"
    db.commit()

    return {"message": "Alert cancelled successfully", "alert_id": alert_id}