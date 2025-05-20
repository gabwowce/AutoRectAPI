from sqlalchemy.orm import Session
from models import client_support
from schemas.client_support import ClientSupportCreate

def create_support_request(db: Session, support_data: ClientSupportCreate):
    db_support = client_support.ClientSupport(**support_data.dict())
    db.add(db_support)
    db.commit()
    db.refresh(db_support)
    return db_support

def get_all_support_requests(db: Session):
    return db.query(client_support.ClientSupport).all()

def get_support_request_by_id(db: Session, uzklausos_id: int):
    return db.query(client_support.ClientSupport).filter_by(uzklausos_id=uzklausos_id).first()

def update_support_request(db: Session, uzklausos_id: int, data: ClientSupportUpdate):
    support = db.query(ClientSupport).filter(ClientSupport.uzklausos_id == uzklausos_id).first()
    if not support:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(support, key, value)
    db.commit()
    db.refresh(support)
    return support
