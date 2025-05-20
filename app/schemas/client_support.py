from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClientSupportBase(BaseModel):
    kliento_id: int
    darbuotojo_id: int
    tema: str
    pranesimas: str
    atsakymas: Optional[str] = None
    pateikimo_data: datetime
    atsakymo_data: Optional[datetime] = None

class ClientSupportCreate(ClientSupportBase):
    pass

class ClientSupport(ClientSupportBase):
    uzklausos_id: int

    class Config:
        orm_mode = True
