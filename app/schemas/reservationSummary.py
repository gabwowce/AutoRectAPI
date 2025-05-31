from datetime import date
from typing import Dict, List
from pydantic import BaseModel

class ReservationSummary(BaseModel):
    rezervacijos_id: int
    kliento_id: int            # 👈
    automobilio_id: int        # 👈
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    busena: str                # 👈
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
