from pydantic import BaseModel, Field, validator

class AutoBase(BaseModel):
    vin: str = Field(..., description="VIN del vehículo")
    marca: str
    modelo: str
    anio: int = Field(..., description="Año entre 1980 y 2026")
    color: str
    precio: float = Field(..., gt=0, description="Precio de venta estimado en USD (>0)")

    @validator("vin")
    def validar_vin(cls, v):
        v = v.strip().upper()
        if not (11 <= len(v) <= 17):
            raise ValueError("El VIN debe tener entre 11 y 17 caracteres.")
        return v

    @validator("anio")
    def validar_anio(cls, v):
        if v < 1980 or v > 2026:
            raise ValueError("El año debe estar entre 1980 y 2026.")
        return v

class AutoCreate(AutoBase):
    pass

class AutoOut(AutoBase):
    id: int
    class Config:
        orm_mode = True

