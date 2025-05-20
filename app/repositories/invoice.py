from sqlalchemy.orm import Session
from models import saskaita as saskaita_model
from models import uzsakymai as uzsakymas_model
from models import klientai as klientas_model
from sqlalchemy import join
from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceStatusUpdate

def get_invoice(db: Session):
    results = (
        db.query(
            saskaita_model.Saskaita.saskaitos_id,
            saskaita_model.Saskaita.uzsakymo_id,
            saskaita_model.Saskaita.suma,
            saskaita_model.Saskaita.saskaitos_data,
            klientas_model.Client.vardas.label("kliento_vardas"),
            klientas_model.Client.pavarde.label("kliento_pavarde"),
            uzsakymas_model.Uzsakymas.uzsakymo_busena.label("busena"),
        )
        .join(uzsakymas_model.Uzsakymas, saskaita_model.Saskaita.uzsakymo_id == uzsakymas_model.Uzsakymas.uzsakymo_id)
        .join(klientas_model.Client, uzsakymas_model.Uzsakymas.kliento_id == klientas_model.Client.kliento_id)
        .all()
    )
    return results

def create_invoice(db: Session, invoice_data: InvoiceCreate):
    invoice = Invoice(**invoice_data.dict())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def delete_invoice(db: Session, invoice_id: int):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
        return True
    return False

def update_invoice_status(db: Session, invoice_id: int, status_data: InvoiceStatusUpdate):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if invoice:
        invoice.status = status_data.status
        db.commit()
        db.refresh(invoice)
        return invoice
    return None
