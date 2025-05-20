from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceBase(BaseModel):
    order_id: int
    total: float
    invoice_date: date
    links: List[Dict]

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceStatusUpdate(BaseModel):
    status: str

class InvoiceOut(InvoiceBase):
    invoice_id: int
    client_first_name: str
    client_last_name: str
    status: str

    class Config:
        orm_mode = True
