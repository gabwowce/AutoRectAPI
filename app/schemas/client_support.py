from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

# 1️⃣ Bendras pagrindas visoms schemoms
class ClientSupportBase(BaseModel):
    kliento_id: int
    darbuotojo_id: int
    tema: str
    pranesimas: str
    atsakymas: Optional[str] = None
    pateikimo_data: datetime
    atsakymo_data: Optional[datetime] = None

# 2️⃣ Kurti naują užklausą
class ClientSupportCreate(ClientSupportBase):
    pass

# 3️⃣ Atnaujinti užklausą (jei norėsi)
class ClientSupportUpdate(BaseModel):
    atsakymas: Optional[str]
    atsakymo_data: Optional[datetime]

# 4️⃣ Schema grąžinimui (su ID ir HATEOAS nuorodomis)
class ClientSupportOut(ClientSupportBase):
    uzklausos_id: int
    links: List[Dict]

    class Config:
        orm_mode = True
