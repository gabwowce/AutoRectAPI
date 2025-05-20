from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from crud import invoice as crud_invoice

router = APIRouter()

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
