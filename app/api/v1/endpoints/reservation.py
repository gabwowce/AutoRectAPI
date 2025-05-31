from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.api.deps import get_db
from app.schemas import reservation as schemas
from app.repositories import reservation as repo
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

# 🟦 GET /reservations/latest — statinis endpoint turi būti pirmas!
@router.get("/latest", response_model=list[schemas.ReservationSummary],
            operation_id="getLatestReservations")
def get_latest_reservations(db: Session = Depends(get_db), limit: int = 5):
    results = repo.get_latest_reservations_with_details(db, limit)
    return [
        {
            "rezervacijos_id": r.rezervacijos_id,
            "kliento_id":      r.kliento_id,
            "automobilio_id":  r.automobilio_id,
            "rezervacijos_pradzia": r.rezervacijos_pradzia,
            "rezervacijos_pabaiga": r.rezervacijos_pabaiga,
            "busena":          r.busena,
            "marke":           r.marke,
            "modelis":         r.modelis,
            "vardas":          r.vardas,
            "pavarde":         r.pavarde,
            "links": [
                {"rel": "self", "href": f"/reservations/{r.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{r.kliento_id}"},
                {"rel": "car",   "href": f"/cars/{r.automobilio_id}"}
            ],
        }
        for r in results
    ]


# 🔍 GET /reservations/search
@router.get("/search", response_model=list[schemas.ReservationOut], operation_id="searchReservations")
def search_reservations(
    db: Session = Depends(get_db),
    kliento_id: Optional[int] = None,
    automobilio_id: Optional[int] = None,
    nuo: Optional[date] = None,
    iki: Optional[date] = None,
    busena: Optional[str] = None
):
    results = repo.search_reservations(
        db,
        kliento_id=kliento_id,
        automobilio_id=automobilio_id,
        nuo=nuo,
        iki=iki,
        busena=busena
    )
    return [
        {
            **res.__dict__,
            "links": [
                {"rel": "self", "href": f"/reservations/{res.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{res.kliento_id}"},
                {"rel": "car", "href": f"/cars/{res.automobilio_id}"}
            ]
        }
        for res in results
    ]

# 📄 GET /reservations — visos
@router.get("/", response_model=list[schemas.ReservationOut], operation_id="getAllReservations")
def get_all_reservations(db: Session = Depends(get_db)):
    reservations = repo.get_all(db)
    return [
        {
            **res.__dict__,
            "links": [
                {"rel": "self", "href": f"/reservations/{res.rezervacijos_id}"},
                {"rel": "client", "href": f"/clients/{res.kliento_id}"},
                {"rel": "car", "href": f"/cars/{res.automobilio_id}"}
            ]
        }
        for res in reservations
    ]

# 📄 GET /reservations/{id}
@router.get("/{rezervacijos_id:int}", response_model=schemas.ReservationOut, operation_id="getReservationById")
def get_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    res = repo.get_by_id(db, rezervacijos_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {
        **res.__dict__,
        "links": generate_links("reservations", res.rezervacijos_id, ["delete"])
    }

# ✏️ PUT /reservations/{id}
@router.put("/{rezervacijos_id:int}", response_model=schemas.ReservationOut, operation_id="updateReservation")
def update_reservation(
    rezervacijos_id: int,
    updated: schemas.ReservationUpdate,
    db: Session = Depends(get_db),
):
    existing = repo.get_by_id(db, rezervacijos_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Reservation not found")

    updated_res = repo.update(db, rezervacijos_id, updated)
    return {
        **updated_res.__dict__,
        "links": generate_links("reservations", updated_res.rezervacijos_id, ["delete"])
    }

# ➕ POST /reservations
@router.post("/", response_model=schemas.ReservationOut, operation_id="createReservation")
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    created = repo.create(db, reservation)
    return {
        **created.__dict__,
        "links": generate_links("reservations", created.rezervacijos_id, ["delete"])
    }

# ❌ DELETE /reservations/{id}
@router.delete("/{rezervacijos_id:int}", operation_id="deleteReservation")
def delete_reservation(rezervacijos_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, rezervacijos_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"ok": True}
