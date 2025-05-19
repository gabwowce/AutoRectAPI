from sqlalchemy import Column, Integer, Date, String, Boolean, ForeignKey
from app.db.base import Base

class Order(Base):
    __tablename__ = "uzsakymai"

    uzsakymo_id = Column(Integer, primary_key=True, index=True)
    kliento_id = Column(Integer, ForeignKey("klientas.id"))
    automobilio_id = Column(Integer, ForeignKey("automobilis.id"))
    darbuotojo_id = Column(Integer, ForeignKey("darbuotojas.id"))
    nuomos_data = Column(Date)
    grazinimo_data = Column(Date)
    paemimo_vietos_id = Column(Integer)
    grazinimo_vietos_id = Column(Integer)
    bendra_kaina = Column(Integer)
    uzsakymo_busena = Column(String)
    turi_papildomas_paslaugas = Column(Boolean)
