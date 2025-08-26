import enum
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date,
    ForeignKey, Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum

from autogo_erp.database import Base

# =========================
# Enums
# =========================

class AcquisitionType(str, enum.Enum):
    TRADE_IN = "TRADE_IN"
    DIRECT_SALE = "DIRECT_SALE"

class VehicleStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"

class SaleStatus(str, enum.Enum):
    OPEN = "OPEN"
    PAID = "PAID"

# =========================
# Vehicle
# =========================

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    # Identificación
    vin = Column(String(32), unique=True, index=True, nullable=False)
    plate = Column(String, unique=True, index=True, nullable=True)

    # Datos básicos
    brand = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    year = Column(Integer, nullable=False)

    # Unidad canónica: KILÓMETROS
    odometer_km = Column(Float, nullable=False)

    acquisition_type = Column(SAEnum(AcquisitionType), nullable=False)

    # Datos del vendedor
    seller_name = Column(String(128), nullable=False)
    seller_contact = Column(String(128), nullable=True)
    seller_document = Column(String(64), nullable=True)  # <-- NUEVO
    received_date = Column(Date, nullable=True)          # <-- NUEVO

    # Estado del vehículo
    status = Column(SAEnum(VehicleStatus), nullable=False, default=VehicleStatus.AVAILABLE)

    # Estado del vehículo
    status = Column(SAEnum(VehicleStatus), nullable=False, default=VehicleStatus.AVAILABLE)

    # Relaciones
    photos = relationship(
        "Photo",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )
    sales = relationship(
        "Sale",
        back_populates="vehicle",
        cascade="all, delete-orphan",
    )
    costos = relationship(
        "Costo",
        back_populates="vehiculo",
        cascade="all, delete-orphan",
    )

# =========================
# Photo
# =========================

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(512), nullable=False)
    is_main = Column(Boolean, nullable=False, default=False)

    vehicle = relationship("Vehicle", back_populates="photos")

# =========================
# Sale
# =========================

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)

    sale_date = Column(DateTime, nullable=False, default=func.now())
    sale_price = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False, default=0.0)

    status = Column(SAEnum(SaleStatus), nullable=False, default=SaleStatus.OPEN)
    notes = Column(String(512), nullable=True)

    # Relaciones
    vehicle = relationship("Vehicle", back_populates="sales")
    payments = relationship(
        "Payment",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

# =========================
# Payment
# =========================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)

    amount = Column(Float, nullable=False)
    paid_at = Column(DateTime, nullable=False, default=func.now())
    method = Column(String(64), nullable=True)      # p.ej. "cash", "card", "transfer"
    reference = Column(String(128), nullable=True)

    sale = relationship("Sale", back_populates="payments")

