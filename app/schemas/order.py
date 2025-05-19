from pydantic import BaseModel
from datetime import date

class OrderBase(BaseModel):
    kliento_id: int
    automobilio_id: int
    darbuotojo_id: int
    nuomos_data: date
    grazinimo_data: date
    paemimo_vietos_id: int
    grazinimo_vietos_id: int
    bendra_kaina: int
    uzsakymo_busena: str
    turi_papildomas_paslaugas: bool

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    uzsakymo_id: int

    class Config:
        orm_mode = True
