from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import client as schemas
from app.repositories import client as repo

router = APIRouter(
    prefix="/client",
)

@router.get("/", response_model=list[schemas.Client])
def get_all_clients(db: Session = Depends(get_db)):
    return repo.get_all(db)

@router.get("/{kliento_id}", response_model=schemas.Client)
def get_client(kliento_id: int, db: Session = Depends(get_db)):
    client = repo.get_by_id(db, kliento_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return repo.create(db, client)

@router.delete("/{kliento_id}")
def delete_client(kliento_id: int, db: Session = Depends(get_db)):
    success = repo.delete(db, kliento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True}
