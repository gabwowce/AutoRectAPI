from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from sqlalchemy import desc
from models.reservation import Reservation
from models.car import Car
from models.client import Client

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
    
def get_latest_reservations_with_details(db: Session, limit: int = 5):
    return (
        db.query(
            Reservation.rezervacijos_id,
            Reservation.rezervacijos_pradzia,
            Reservation.rezervacijos_pabaiga,
            Car.marke,
            Car.modelis,
            Client.vardas,
            Client.pavarde,
        )
        .join(Car, Reservation.automobilio_id == Car.automobilio_id)
        .join(Client, Reservation.kliento_id == Client.kliento_id)
        .order_by(desc(Reservation.rezervacijos_pradzia))
        .limit(limit)
        .all()
    )

