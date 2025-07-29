"""Database models for AutoGo ERP.

This module defines the ``Car`` model representing the inventory of
automobiles in the system.  Each car record includes fields for
brand, model, year, VIN (Vehicle Identification Number), color,
price, status, and the date the vehicle was added to inventory.

The SQLAlchemy ORM maps this model to the ``cars`` table in the
database.  We use simple data types appropriate for a lightweight
application.  Additional tables and relationships can be defined in
future phases of the ERP project.
"""

from datetime import date
from typing import Optional

from . import db


class Car(db.Model):
    """Represents a car in the AutoGo inventory.

    Attributes:
        id: Primary key identifier for the record.
        brand: Manufacturer of the car (e.g., Toyota, Ford).
        model: Model name or designation (e.g., Corolla, Mustang).
        year: Year the car was manufactured.
        vin: Vehicle Identification Number; unique for each car.
        color: Color of the car's exterior.
        price: Asking price for the car in USD.
        status: Inventory status (e.g., "Disponible", "Vendido").
        entry_date: Date the car entered the inventory.
    """

    __tablename__ = 'cars'

    id: int = db.Column(db.Integer, primary_key=True)
    brand: str = db.Column(db.String(50), nullable=False)
    model: str = db.Column(db.String(50), nullable=False)
    year: int = db.Column(db.Integer, nullable=False)
    vin: str = db.Column(db.String(50), unique=True, nullable=False)
    color: str = db.Column(db.String(30), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    status: str = db.Column(db.String(30), nullable=False, default="Disponible")
    entry_date: date = db.Column(db.Date, nullable=False, default=date.today)

    def __repr__(self) -> str:
        return f"<Car {self.id} {self.brand} {self.model} ({self.year})>"

    def to_dict(self) -> dict[str, object]:
        """Serialize the car to a dictionary for JSON responses."""
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "vin": self.vin,
            "color": self.color,
            "price": self.price,
            "status": self.status,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
        }