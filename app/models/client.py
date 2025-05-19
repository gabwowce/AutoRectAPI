from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class Client(Base):
    __tablename__ = "klientai"

    kliento_id = Column(Integer, primary_key=True, index=True)
    vardas = Column(String)
    pavarde = Column(String)
    el_pastas = Column(String, unique=True, index=True)
    telefono_nr = Column(String)
    gimimo_data = Column(Date)
    registracijos_data = Column(Date)
    bonus_taskai = Column(Integer)
