from pydantic import BaseModel, EmailStr
from datetime import date

class ClientBase(BaseModel):
    vardas: str
    pavarde: str
    el_pastas: EmailStr
    telefono_nr: str
    gimimo_data: date
    registracijos_data: date
    bonus_taskai: int
    links: List[Dict]

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    kliento_id: int

    class Config:
        orm_mode = True
