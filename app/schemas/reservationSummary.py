class ReservationSummary(BaseModel):
    rezervacijos_id: int
    rezervacijos_pradzia: date
    rezervacijos_pabaiga: date
    marke: str
    modelis: str
    vardas: str
    pavarde: str
    links: List[Dict]

    class Config:
        orm_mode = True
