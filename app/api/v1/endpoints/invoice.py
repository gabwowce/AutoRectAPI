# app/api/endpoints/invoice.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceStatusUpdate, InvoiceOut
from app.repositories import invoice as crud_invoice
from utils.hateoas import generate_links

router = APIRouter(prefix="/invoices", tags=["Invoices"])


# ---------- COLLECTION ----------
@router.get("/", response_model=dict)  # grąžinam HAL kolekciją
def get_all_invoices(db: Session = Depends(get_db)):
    invoices = crud_invoice.get_invoice(db)            # list[dict]
    return {
        "_links": generate_links("invoices"),
        "_embedded": {
            "invoices": [
                {
                    **inv,
                    "_links": generate_links(
                        "invoices",
                        inv["saskaitos_id"],
                        extra={"order": f"/orders/{inv['uzsakymo_id']}"},
                        actions=["update_status", "delete"],
                    ),
                }
                for inv in invoices
            ]
        },
    }


# ---------- SINGLE INVOICE ----------
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = crud_invoice.get_by_id(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return {
        **inv.__dict__,
        "_links": generate_links(
            "invoices",
            invoice_id,
            extra={"order": f"/orders/{inv.uzsakymo_id}"},
            actions=["update_status", "delete"],
        ),
    }


# ---------- CREATE ----------
@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    created = crud_invoice.create_invoice(db, invoice)

    return {
        **created.__dict__,
        "_links": generate_links(
            "invoices",
            created.saskaitos_id,
            extra={"order": f"/orders/{created.uzsakymo_id}"},
            actions=["update_status", "delete"],
        ),
    }


# ---------- DELETE ----------
@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    success = crud_invoice.delete_invoice(db, invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # 204 – jokio turinio, todėl nieko negrąžinam


# ---------- UPDATE STATUS ----------
@router.patch("/{invoice_id}/status", response_model=InvoiceOut)
def update_status(
    invoice_id: int,
    status: InvoiceStatusUpdate,
    db: Session = Depends(get_db),
):
    updated = crud_invoice.update_invoice_status(db, invoice_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return {
        **updated.__dict__,
        "_links": generate_links(
            "invoices",
            invoice_id,
            extra={"order": f"/orders/{updated.uzsakymo_id}"},
            actions=["update_status", "delete"],
        ),
    }
