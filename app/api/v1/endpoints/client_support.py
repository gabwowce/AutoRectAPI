from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.client_support import ClientSupportCreate, ClientSupport
from crud import client_support

router = APIRouter()

@router.post("/", response_model=ClientSupport)
def create_support(support: ClientSupportCreate, db: Session = Depends(get_db)):
    return client_support.create_support_request(db, support)

@router.get("/", response_model=list[ClientSupport])
def get_all_supports(db: Session = Depends(get_db)):
    return client_support.get_all_support_requests(db)

@router.get("/{uzklausos_id}", response_model=ClientSupport)
def get_support(uzklausos_id: int, db: Session = Depends(get_db)):
    support = client_support.get_support_request_by_id(db, uzklausos_id)
    if not support:
        raise HTTPException(status_code=404, detail="Support request not found")
    return support
