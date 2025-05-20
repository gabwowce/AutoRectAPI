from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import order as schemas
from app.repositories import order as repo
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/", response_model=list[schemas.OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    orders = repo.get_all(db)
    return [
        {
            **order.__dict__,
            "links": generate_links("orders", order.uzsakymo_id, ["delete"])
        }
        for order in orders
    ]

@router.get("/{uzsakymo_id}", response_model=schemas.OrderOut)
def get_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    order = repo.get_by_id(db, uzsakymo_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        **order.__dict__,
        "links": generate_links("orders", order.uzsakymo_id, ["delete"])
    }

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    created = repo.create(db, order)
    return {
        **created.__dict__,
        "links": generate_links("orders", created.uzsakymo_id, ["delete"])
    }

@router.delete("/{uzsakymo_id}")
def delete_order(uzsakymo_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, uzsakymo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}
