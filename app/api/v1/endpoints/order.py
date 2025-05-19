from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import order as schemas
from app.repositories import order as repo

router = APIRouter(
    prefix="/order",
)

@router.get("/", response_model=list[schemas.Order])
def get_all_orders(db: Session = Depends(get_db)):
    return repo.get_all(db)

@router.get("/{uzsakymo_id}", response_model=schemas.Order)
def get_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    order = repo.get_by_id(db, uzsakymo_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return repo.create(db, order)

@router.delete("/{uzsakymo_id}")
def delete_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, uzsakymo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}
