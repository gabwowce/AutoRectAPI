from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional

class ReservationBase(BaseModel):
    kliento_id: int
    automobilio_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    rezervacijos_pradzia: Optional[date] = None
    rezervacijos_pabaiga: Optional[date] = None
    busena: Optional[str] = None

class ReservationOut(ReservationBase):
    rezervacijos_id: int
    kliento_id: int
    automobilio_id: int
    links: List[Dict]

    class Config:
        orm_mode = True

class ReservationSummary(BaseModel):
    rezervacijos_id: int
    kliento_id: int            
    automobilio_id: int        
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str                
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
