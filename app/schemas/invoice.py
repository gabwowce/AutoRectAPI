from pydantic import BaseModel
from datetime import date

class InvoiceOut(BaseModel):
    saskaitos_id: int
    uzsakymo_id: int
    suma: float
    saskaitos_data: date
    kliento_vardas: str
    kliento_pavarde: str
    busena: str

    class Config:
        orm_mode = True
