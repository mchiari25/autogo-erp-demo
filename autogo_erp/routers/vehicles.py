from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from autogo_erp import models
from autogo_erp.database import SessionLocal  # ← usamos SessionLocal, no get_db
from autogo_erp.schemas import VehicleRead, VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

# ===== Dependencia DB (local a este router) =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _norm_plate(p: Optional[str]) -> Optional[str]:
    if p is None:
        return None
    p = p.strip().upper()
    return p or None

# Listar
@router.get("/", response_model=List[VehicleRead])
def list_vehicles(db: Session = Depends(get_db)):
    return db.query(models.Vehicle).all()

# Obtener por id
@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return v

# Crear (con validación VIN/PLATE únicos)
@router.post("/", response_model=VehicleRead)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    # VIN
    exists = db.query(models.Vehicle).filter(models.Vehicle.vin == payload.vin).first()
    if exists:
        raise HTTPException(status_code=400, detail=f"VIN '{payload.vin}' already exists")

    # PLATE (si viene)
    plate = _norm_plate(payload.plate)
    if plate:
        exists_p = db.query(models.Vehicle).filter(models.Vehicle.plate == plate).first()
        if exists_p:
            raise HTTPException(status_code=400, detail=f"Plate '{plate}' already exists")

    v = models.Vehicle(
        vin=payload.vin,
        plate=plate,
        brand=payload.brand,
        model=payload.model,
        year=payload.year,
        odometer_km=payload.odometer_km,
        acquisition_type=payload.acquisition_type,
        seller_name=payload.seller_name,
        seller_contact=payload.seller_contact,
        seller_document=payload.seller_document,   # nuevos campos
        received_date=payload.received_date,       # nuevos campos
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

# Actualizar (PATCH)
@router.patch("/{vehicle_id}", response_model=VehicleRead)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db)):
    v = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    data = payload.dict(exclude_unset=True)

    # VIN duplicado
    if "vin" in data:
        dup = db.query(models.Vehicle).filter(
            models.Vehicle.vin == data["vin"],
            models.Vehicle.id != vehicle_id
        ).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"VIN '{data['vin']}' already exists")

    # PLATE duplicada (normalizar primero)
    if "plate" in data:
        plate = _norm_plate(data["plate"])
        data["plate"] = plate
        if plate:
            dup_p = db.query(models.Vehicle).filter(
                models.Vehicle.plate == plate,
                models.Vehicle.id != vehicle_id
            ).first()
            if dup_p:
                raise HTTPException(status_code=400, detail=f"Plate '{plate}' already exists")

    for k, val in data.items():
        setattr(v, k, val)

    db.commit()
    db.refresh(v)
    return v

# Eliminar
@router.delete("/{vehicle_id}", response_model=dict)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(v)
    db.commit()
    return {"ok": True}

