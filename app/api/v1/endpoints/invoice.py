from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from repositories import invoice as crud_invoice
from utils.hateoas import generate_links

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

def generate_invoice_links(invoice) -> list[dict]:
    return [
        {"rel": "self", "href": f"/invoices/{invoice.invoice_id}"},
        {"rel": "order", "href": f"/orders/{invoice.order_id}"},
        {"rel": "client", "href": f"/clients/{invoice.kliento_id}"},
        {"rel": "update_status", "href": f"/invoices/{invoice.invoice_id}/status"},
        {"rel": "delete", "href": f"/invoices/{invoice.invoice_id}"}
    ]


@router.get("/", response_model=list[InvoiceOut])
def get_all_invoices(db: Session = Depends(get_db)):
    raw_data = crud_invoice.get_all_invoices_with_clients(db)
    return [
        {
            **invoice.__dict__,
            "links": generate_invoice_links(invoice)
        }
        for invoice in raw_data
    ]

@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    created = crud_invoice.create_invoice(db, invoice)
    return {
        **created.__dict__,
        "links": generate_invoice_links(created)
    }
@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    success = crud_invoice.delete_invoice(db, invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"detail": "Invoice deleted"}

@router.patch("/{invoice_id}/status", response_model=InvoiceOut)
def update_status(invoice_id: int, status: InvoiceStatusUpdate, db: Session = Depends(get_db)):
    updated = crud_invoice.update_invoice_status(db, invoice_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        **updated.__dict__,
        "links": generate_invoice_links(updated)
    }
