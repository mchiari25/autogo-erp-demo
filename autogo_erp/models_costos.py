from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from autogo_erp.database import Base

class Costo(Base):
    __tablename__ = "costos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(150), nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(String(30), nullable=False)          # compra, tramite, transporte, reparacion, otros
    referencia = Column(String(50), nullable=True)     # opcional: vincular con vehículo, nro, etc.

    # Relación con vehículos
    vehiculo_id = Column(Integer, ForeignKey("autos.id"), nullable=True)
    vehiculo = relationship("Auto", back_populates="costos")

