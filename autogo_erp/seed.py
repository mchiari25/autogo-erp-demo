from sqlalchemy.orm import Session
from .models import Auto

DEMO_AUTOS = [
    dict(vin="1HGCM82633A004352", marca="Honda", modelo="Civic",  anio=2020, color="Blanco", precio=13500),
    dict(vin="WBA8E1G5XGNU12345", marca="BMW",   modelo="320i",   anio=2019, color="Negro",  precio=18500),
    dict(vin="3FA6P0H72HR123456", marca="Ford",  modelo="Fusion", anio=2018, color="Gris",   precio=11000),
]

def cargar_demo_si_vacio(db: Session):
    if db.query(Auto).count() == 0:
        for a in DEMO_AUTOS:
            db.add(Auto(**a))
        db.commit()

