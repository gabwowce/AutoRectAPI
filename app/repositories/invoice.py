from sqlalchemy.orm import Session
from models import saskaita as saskaita_model
from models import uzsakymai as uzsakymas_model
from models import klientai as klientas_model
from sqlalchemy import join

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
