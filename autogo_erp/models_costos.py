from sqlalchemy import Column, Integer, String, Numeric, Date, Text, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from .database import Base

class Costo(Base):
    __tablename__ = "costos"

    id = Column(Integer, primary_key=True, index=True)
    auto_id = Column(Integer, ForeignKey("autos.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = Column(String(30), nullable=False)         # compra, tramite, transporte, reparacion, otros
    monto = Column(Numeric(12, 2), nullable=False)    # >= 0
    fecha = Column(Date, nullable=False)
    notas = Column(Text)

    auto = relationship("Auto", back_populates="costos")

    __table_args__ = (
        CheckConstraint("monto >= 0", name="ck_costo_monto_nonneg"),
        Index("ix_costos_auto_tipo", "auto_id", "tipo"),
    )

