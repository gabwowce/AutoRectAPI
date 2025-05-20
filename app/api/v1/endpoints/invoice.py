from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from repositories import invoice as crud_invoice

router = APIRouter()

@router.get("/", response_model=list[InvoiceOut])
def get_all_invoices(db: Session = Depends(get_db)):
    raw_data = crud_invoice.get_all_invoices_with_clients(db)  # tavo custom SELECT
    return [
        {
            **invoice.__dict__,
            "links": generate_links("invoices", invoice.invoice_id, ["update_status", "delete"])
        }
        for invoice in raw_data
    ]
    
@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return crud_invoice.create_invoice(db, invoice)

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
    return updated
