from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import reservation as schemas
from app.repositories import reservation as repo
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

@router.get("/", response_model=list[schemas.ReservationOut])
def get_all_reservations(db: Session = Depends(get_db)):
    reservations = repo.get_all(db)
    return [
        {
            **res.__dict__,
            "links": generate_links("reservations", res.rezervacijos_id, ["delete"])
        }
        for res in reservations
    ]

@router.get("/{rezervacijos_id}", response_model=schemas.ReservationOut)
def get_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    res = repo.get_by_id(db, rezervacijos_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {
        **res.__dict__,
        "links": generate_links("reservations", res.rezervacijos_id, ["delete"])
    }

@router.post("/", response_model=schemas.ReservationOut)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    created = repo.create(db, reservation)
    return {
        **created.__dict__,
        "links": generate_links("reservations", created.rezervacijos_id, ["delete"])
    }

@router.delete("/{rezervacijos_id}")
def delete_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, rezervacijos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"ok": True}
