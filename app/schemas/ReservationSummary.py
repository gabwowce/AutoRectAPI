from pydantic import BaseModel
from datetime import date

class ReservationSummary(BaseModel):
    rezervacijos_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    marke: str
    modelis: str
    vardas: str
    pavarde: str
