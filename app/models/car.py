from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DECIMAL, Date
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.models.location import Location

class Car(Base):
    __tablename__ = "Automobiliai"

    automobilio_id = Column(Integer, primary_key=True, index=True)
    marke = Column(String, nullable=False)
    modelis = Column(String, nullable=False)
    metai = Column(Integer, nullable=False)
    numeris = Column(String, unique=True, nullable=False)
    vin_kodas = Column(String(17), unique=True, nullable=False)
    spalva = Column(String, nullable=False)
    kebulo_tipas = Column(String, nullable=False)
    pavarų_deze = Column(String, nullable=False)
    variklio_turis = Column(DECIMAL(3,1), nullable=False)
    galia_kw = Column(Integer, nullable=False)
    kuro_tipas = Column(String, nullable=False)
    rida = Column(Integer, nullable=False)
    sedimos_vietos = Column(Integer, nullable=False)
    klimato_kontrole = Column(Boolean, nullable=False, default=False)
    navigacija = Column(Boolean, nullable=False, default=False)
    kaina_parai = Column(DECIMAL(10,2), nullable=False)
    automobilio_statusas = Column(String, nullable=False)
    technikines_galiojimas = Column(Date, nullable=False)
    dabartine_vieta_id = Column(Integer, ForeignKey("pristatymo_vietos.vietos_id"))
    pastabos = Column(String)

    lokacija = relationship(Location, backref="automobiliai")