from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.repositories import car as car_repo
from app.schemas.car import CarOut, CarCreate, CarUpdate, CarStatusUpdate
from utils.hateoas import generate_links
from typing import Optional

router = APIRouter(
    prefix="/cars",  
)


@router.get("/", response_model=list[CarOut])
def get_all_cars(db: Session = Depends(get_db)):
    cars = car_repo.get_all(db)
    return [
        {
            **car.__dict__,
            "links": generate_links("cars", car.id, ["update", "delete", "update_status"])
        }
        for car in cars
    ]

@router.get("/{car_id}", response_model=CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = car_repo.get_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        **car.__dict__,
        "links": generate_links("cars", car.id, ["update", "delete", "update_status"])
    }

@router.post("/", response_model=CarOut)
def create_car(data: CarCreate, db: Session = Depends(get_db)):
    car = car_repo.create(db, data.dict())
    return {
        **car.__dict__,
        "links": generate_links("cars", car.id, ["update", "delete", "update_status"])
    }


@router.put("/{car_id}", response_model=CarOut)
def update_car(car_id: int, data: CarUpdate, db: Session = Depends(get_db)):
    updated = car_repo.update(db, car_id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        **updated.__dict__,
        "links": generate_links("cars", updated.id, ["update", "delete", "update_status"])
    }


@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted = car_repo.delete(db, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}

@router.patch("/{car_id}/status", response_model=CarOut)
def update_car_status(car_id: int, data: CarStatusUpdate, db: Session = Depends(get_db)):
    updated = car_repo.update_status(db, car_id, data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return {
        **updated.__dict__,
        "links": generate_links("cars", updated.id, ["update", "delete", "update_status"])
    }

@router.get("/stats/by-status")
def get_car_stats_by_status(db: Session = Depends(get_db)):
    return car_repo.get_car_counts_by_status(db)

@router.get("/search", response_model=list[CarOut])
def search_cars(
    db: Session = Depends(get_db),
    marke: Optional[str] = None,
    modelis: Optional[str] = None,
    spalva: Optional[str] = None,
    status: Optional[str] = None,
    kuro_tipas: Optional[str] = None,
    metai: Optional[int] = None,
    sedimos_vietos: Optional[int] = None
):
    results = car_repo.search_cars(
        db,
        marke=marke,
        modelis=modelis,
        spalva=spalva,
        status=status,
        kuro_tipas=kuro_tipas,
        metai=metai,
        sedimos_vietos=sedimos_vietos
    )

    return [
        {
            **car.__dict__,
            "links": generate_links("cars", car.id, ["update", "delete", "update_status"])
        }
        for car in results
    ]

@router.get("/cars/free", response_model=List[CarOut])
def get_free_cars(db: Session = Depends(get_db)):
    cars = (
        db.query(Car)
        .filter(Car.automobilio_statusas == "laisvas")
        .all()
    )
    return cars

