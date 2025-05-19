from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

def get_all(db: Session):
    return db.query(Reservation).all()

def get_by_id(db: Session, rezervacijos_id: int):
    return db.query(Reservation).filter(Reservation.rezervacijos_id == rezervacijos_id).first()

def create(db: Session, reservation: ReservationCreate):
    db_res = Reservation(**reservation.dict())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

def delete(db: Session, rezervacijos_id: int):
    db_res = get_by_id(db, rezervacijos_id)
    if db_res:
        db.delete(db_res)
        db.commit()
        return True
    return False
