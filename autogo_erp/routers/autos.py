from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, models

router = APIRouter(prefix="/autos", tags=["Autos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.AutoOut])
def listar_autos(db: Session = Depends(get_db)):
    return db.query(models.Auto).order_by(models.Auto.id.desc()).all()

@router.post("/", response_model=schemas.AutoOut, status_code=status.HTTP_201_CREATED)
def crear_auto(payload: schemas.AutoCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Auto).filter(models.Auto.vin == payload.vin.upper()).first()
    if existe:
        raise HTTPException(status_code=400, detail="El VIN ya existe en el sistema.")
    auto = models.Auto(
        vin=payload.vin.upper().strip(),
        marca=payload.marca.strip(),
        modelo=payload.modelo.strip(),
        anio=payload.anio,
        color=payload.color.strip(),
        precio=payload.precio,
    )
    db.add(auto)
    db.commit()
    db.refresh(auto)
    return auto

@router.get("/{auto_id}", response_model=schemas.AutoOut)
def obtener_auto(auto_id: int, db: Session = Depends(get_db)):
    auto = db.query(models.Auto).get(auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado.")
    return auto

@router.put("/{auto_id}", response_model=schemas.AutoOut)
def editar_auto(auto_id: int, payload: schemas.AutoCreate, db: Session = Depends(get_db)):
    auto = db.query(models.Auto).get(auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado.")

    nuevo_vin = payload.vin.upper().strip()
    existe_otro = db.query(models.Auto).filter(
        models.Auto.vin == nuevo_vin,
        models.Auto.id != auto_id
    ).first()
    if existe_otro:
        raise HTTPException(status_code=400, detail="El VIN ya existe en el sistema.")

    auto.vin = nuevo_vin
    auto.marca = payload.marca.strip()
    auto.modelo = payload.modelo.strip()
    auto.anio = payload.anio
    auto.color = payload.color.strip()
    auto.precio = payload.precio

    db.commit()
    db.refresh(auto)
    return auto

@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_auto(auto_id: int, db: Session = Depends(get_db)):
    auto = db.query(models.Auto).get(auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado.")
    db.delete(auto)
    db.commit()
    return None

