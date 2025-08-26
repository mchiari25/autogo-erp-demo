from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel
from autogo_erp.models import AcquisitionType, VehicleStatus

# ===== Vehicles =====

class VehicleBase(BaseModel):
    vin: str
    plate: Optional[str] = None
    brand: str
    model: str
    year: int
    odometer_km: float
    acquisition_type: AcquisitionType
    seller_name: str
    seller_contact: Optional[str] = None
    # 👇 nuevos
    seller_document: Optional[str] = None
    received_date: Optional[date] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    vin: Optional[str] = None
    plate: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    odometer_km: Optional[float] = None
    acquisition_type: Optional[AcquisitionType] = None
    seller_name: Optional[str] = None
    seller_contact: Optional[str] = None
    # 👇 nuevos
    seller_document: Optional[str] = None
    received_date: Optional[date] = None
    status: Optional[VehicleStatus] = None

class PhotoRead(BaseModel):
    id: int
    vehicle_id: int
    url: str
    is_main: bool

    class Config:
        from_attributes = True

class VehicleRead(VehicleBase):
    id: int
    status: VehicleStatus
    photos: List[PhotoRead] = []

    class Config:
        from_attributes = True

