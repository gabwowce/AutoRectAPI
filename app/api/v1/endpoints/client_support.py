from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.client_support import ClientSupportCreate, ClientSupportOut, ClientSupportUpdate
from crud import client_support
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/support",
    tags=["Client Support"]
)

@router.post("/", response_model=ClientSupportOut)
def create_support(support: ClientSupportCreate, db: Session = Depends(get_db)):
    created = client_support.create_support_request(db, support)
    return {
        **created.__dict__,
        "links": generate_links("support", created.uzklausos_id, ["delete"])
    }

@router.get("/", response_model=list[ClientSupportOut])
def get_all_supports(db: Session = Depends(get_db)):
    items = client_support.get_all_support_requests(db)
    return [
        {
            **item.__dict__,
            "links": generate_links("support", item.uzklausos_id, ["delete"])
        }
        for item in items
    ]

@router.get("/{uzklausos_id}", response_model=ClientSupportOut)
def get_support(uzklausos_id: int, db: Session = Depends(get_db)):
    support = client_support.get_support_request_by_id(db, uzklausos_id)
    if not support:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **support.__dict__,
        "links": generate_links("support", support.uzklausos_id, ["delete"])
    }

@router.patch("/{uzklausos_id}", response_model=ClientSupportOut)
def answer_to_support(uzklausos_id: int, data: ClientSupportUpdate, db: Session = Depends(get_db)):
    updated = client_support.update_support_request(db, uzklausos_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **updated.__dict__,
        "links": generate_links("support", updated.uzklausos_id, ["delete"])
    }
