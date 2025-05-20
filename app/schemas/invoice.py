from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

# 1️⃣ Bendras pagrindas be `links` (tik bendri laukai)
class InvoiceBase(BaseModel):
    order_id: int
    total: float
    invoice_date: date

# 2️⃣ Sukūrimui iš kliento pusės
class InvoiceCreate(InvoiceBase):
    pass

# 3️⃣ Atnaujinimui (tik statuso keitimas)
class InvoiceStatusUpdate(BaseModel):
    status: str

# 4️⃣ Atsakymui į klientą su papildoma info
class InvoiceOut(InvoiceBase):
    invoice_id: int
    client_first_name: str
    client_last_name: str
    status: str
    links: List[Dict]

    class Config:
        orm_mode = True
