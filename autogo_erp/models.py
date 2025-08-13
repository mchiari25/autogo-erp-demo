from sqlalchemy import Column, Integer, String, Float, CheckConstraint, UniqueConstraint
from .database import Base  # Usamos el Base definido en database.py

class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(17), nullable=False, index=True)      # 17 chars típicamente
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)                    # validación 1980–2026
    color = Column(String(30), nullable=False)
    precio = Column(Float, nullable=False)                    # <-- requerido por tu DB

    __table_args__ = (
        UniqueConstraint("vin", name="uq_autos_vin"),
        CheckConstraint("anio >= 1980 AND anio <= 2026", name="ck_autos_anio_rango"),
        CheckConstraint("precio > 0", name="ck_autos_precio_pos"),
    )

