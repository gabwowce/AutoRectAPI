from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.client_support import ClientSupportCreate, ClientSupportOut, ClientSupportUpdate
from app.repositories import client_support

router = APIRouter(
    prefix="/support",
    tags=["Client Support"]
)

def build_support_links(support) -> list[dict]:
    return [
        {"rel": "self", "href": f"/support/{support.uzklausos_id}"},
        {"rel": "client", "href": f"/clients/{support.kliento_id}"},
        {"rel": "employee", "href": f"/employees/{support.darbuotojo_id}"},
        {"rel": "answer", "href": f"/support/{support.uzklausos_id}"},
        {"rel": "delete", "href": f"/support/{support.uzklausos_id}"}
    ]

@router.post("/", response_model=ClientSupportOut, operation_id="createSupport")
def create_support(support: ClientSupportCreate, db: Session = Depends(get_db)):
    created = client_support.create_support_request(db, support)
    return {
        **created.__dict__,
        "links": build_support_links(created)
    }

@router.get("/", response_model=list[ClientSupportOut], operation_id="getAllSupports")
def get_all_supports(db: Session = Depends(get_db)):
    items = client_support.get_all_support_requests(db)
    return [
        {
            **item.__dict__,
            "links": build_support_links(item)
        }
        for item in items
    ]

@router.get("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="getSupport")
def get_support(uzklausos_id: int, db: Session = Depends(get_db)):
    support = client_support.get_support_request_by_id(db, uzklausos_id)
    if not support:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **support.__dict__,
        "links": build_support_links(support)
    }

@router.patch("/{uzklausos_id}", response_model=ClientSupportOut, operation_id="answerToSupport")
def answer_to_support(uzklausos_id: int, data: ClientSupportUpdate, db: Session = Depends(get_db)):
    updated = client_support.update_support_request(db, uzklausos_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Support request not found")
    return {
        **updated.__dict__,
        "links": build_support_links(updated)
    }

@router.get("/unanswered", response_model=list[ClientSupportOut], operation_id="getUnansweredSupports")
def get_unanswered_supports(db: Session = Depends(get_db)):
    items = client_support.get_unanswered_requests(db)
    return [
        {
            **item.__dict__,
            "links": build_support_links(item)
        }
        for item in items
    ]
