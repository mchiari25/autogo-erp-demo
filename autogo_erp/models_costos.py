from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from autogo_erp.database import Base

class Costo(Base):
    __tablename__ = "costos"

    id = Column(Integer, primary_key=True, index=True)

    # Datos del costo
    descripcion = Column(String(150), nullable=False)
    monto = Column(Float, nullable=False)

    # Clasificación del costo
    # valores típicos: "tramite", "compra", "transporte", "reparacion", "otros"
    tipo = Column(String(30), nullable=False)

    # Referencia opcional (nro de trámite, vínculo externo, etc.)
    referencia = Column(String(50), nullable=True)

    # Relación con Vehicle (tabla 'vehicles')
    vehiculo_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    vehiculo = relationship("Vehicle", back_populates="costos")

