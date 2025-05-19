from pydantic import BaseModel
from datetime import date

class ReservationBase(BaseModel):
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    rezervacijos_id: int

    class Config:
        orm_mode = True
