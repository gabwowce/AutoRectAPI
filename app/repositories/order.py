from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate

def get_all(db: Session):
    return db.query(Order).all()

def get_by_id(db: Session, uzsakymo_id: int):
    return db.query(Order).filter(Order.uzsakymo_id == uzsakymo_id).first()

def create(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete(db: Session, uzsakymo_id: int):
    db_order = get_by_id(db, uzsakymo_id)
    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    return False
    
def get_order_counts_by_status(db: Session):
    results = (
        db.query(Order.uzsakymo_busena, func.count().label("value"))
        .group_by(Order.uzsakymo_busena)
        .all()
    )

    # Žemėlapis pavadinimų iš duomenų į frontend formatą
    status_map = {
        "vykdomas": "Vykdomi",
        "užbaigtas": "Užbaigti",
        "atšauktas": "Atšaukti"
    }

    return [
        {
            "name": status_map.get(row.uzsakymo_busena, row.uzsakymo_busena),
            "value": row.value
        }
        for row in results
    ]
