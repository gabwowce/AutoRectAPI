from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

from app.schemas.location import LocationOut

# 1️⃣ Bendras pagrindas visoms schemoms
class CarBase(BaseModel):
    marke: str
    modelis: str
    metai: int
    numeris: str
    vin_kodas: str
    spalva: str
    kebulo_tipas: str
    pavarų_deze: str
    variklio_turis: float
    galia_kw: int
    kuro_tipas: str
    rida: int
    sedimos_vietos: int
    klimato_kontrole: bool
    navigacija: bool
    kaina_parai: float
    automobilio_statusas: str
    technikines_galiojimas: date
    dabartine_vieta_id: int
    pastabos: Optional[str]

# 2️⃣ Kūrimo schema (naudojama POST metu)
class CarCreate(CarBase):
    pass

# 3️⃣ Atnaujinimo schema (naudojama PUT/PATCH metu)
class CarUpdate(CarBase):
    pass

class CarOut(CarBase):
    automobilio_id: int
    lokacija: Optional[LocationOut]
    links: List[dict]

    class Config:
        orm_mode = True

class CarStatusUpdate(BaseModel):
    status: str