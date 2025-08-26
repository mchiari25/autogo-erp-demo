from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from autogo_erp.database import SessionLocal
from ..models_costos import Costo

router = APIRouter(prefix="/tramites", tags=["Trámites"])

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas ---
class TramiteItemIn(BaseModel):
    descripcion: str = Field(..., max_length=150)
    monto: float

class TramiteIn(BaseModel):
    referencia: Optional[str] = Field(None, max_length=50)  # opcional: vincular con vehículo
    items: List[TramiteItemIn]

class TramiteOut(BaseModel):
    id: int
    tipo: str
    descripcion: str
    monto: float
    referencia: Optional[str]

    class Config:
        from_attributes = True

# --- Endpoints ---
@router.get("/", response_model=List[TramiteOut], summary="Listar trámites")
def listar_tramites(db: Session = Depends(get_db)):
    return db.query(Costo).filter(Costo.tipo == "tramite").all()

@router.post("/", summary="Crear trámite")
def crear_tramite(payload: TramiteIn, db: Session = Depends(get_db)):
    total = 0.0
    creados = []
    for item in payload.items:
        c = Costo(
            tipo="tramite",
            descripcion=item.descripcion,
            monto=item.monto,
            referencia=payload.referencia
        )
        db.add(c)
        creados.append(c)
        total += item.monto
    db.commit()
    for c in creados:
        db.refresh(c)
    return {
        "ok": True,
        "referencia": payload.referencia,
        "total": total,
        "items_creados": [c.id for c in creados]
    }

@router.get("/{id}", response_model=TramiteOut, summary="Obtener trámite por id")
def obtener_tramite(id: int, db: Session = Depends(get_db)):
    c = db.query(Costo).filter(Costo.id == id, Costo.tipo == "tramite").first()
    if not c:
        raise HTTPException(status_code=404, detail="Trámite no encontrado")
    return c

