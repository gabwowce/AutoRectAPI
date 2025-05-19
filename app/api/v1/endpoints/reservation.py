from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import reservation as schemas
from app.repositories import reservation as repo

router = APIRouter(
    prefix="/reservation",
)

@router.get("/", response_model=list[schemas.Reservation])
def get_all_reservations(db: Session = Depends(get_db)):
    return repo.get_all(db)

@router.get("/{rezervacijos_id}", response_model=schemas.Reservation)
def get_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    res = repo.get_by_id(db, rezervacijos_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return repo.create(db, reservation)

@router.delete("/{rezervacijos_id}")
def delete_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, rezervacijos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"ok": True}
