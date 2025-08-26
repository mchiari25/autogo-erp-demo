# Forzar redeploy limpio
from sqlalchemy import inspect, text
from autogo_erp.database import SessionLocal, Base, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pkgutil, importlib, pathlib

# DB / modelos / seed
from autogo_erp.database import SessionLocal, Base, engine
from autogo_erp.seed import cargar_demo_si_vacio

from sqlalchemy import inspect, text

app = FastAPI(title="AutoGo ERP")

# Plantillas (si usas autos_ui.html en templates/)
templates = Jinja2Templates(directory="templates")

# Incluir routers automáticamente desde autogo_erp/routers/*.py
def include_all_routers(app: FastAPI):
    routers_path = pathlib.Path(__file__).parent / "routers"
    package_name = "autogo_erp.routers"

    # Ignorar routers legados que dependían del viejo schemas.py
    skip = {"imports", "gallery", "photos", "sales", "autos"}

    if routers_path.exists():
        for _, module_name, _ in pkgutil.iter_modules([str(routers_path)]):
            if module_name in skip:
                continue
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)

include_all_routers(app)

# Crear tablas y cargar demo si está vacío
@app.on_event("startup")
def startup():
    # 1) Crear tablas base
    Base.metadata.create_all(bind=engine)

    # 2) Mini-migración: agregar columnas que falten en 'vehicles'
    insp = inspect(engine)
    cols = [c["name"] for c in insp.get_columns("vehicles")]
    with engine.begin() as conn:
        if "plate" not in cols:
            conn.execute(text("ALTER TABLE vehicles ADD COLUMN plate VARCHAR"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_vehicles_plate ON vehicles(plate)"))
        if "seller_document" not in cols:
            conn.execute(text("ALTER TABLE vehicles ADD COLUMN seller_document VARCHAR(64)"))
        if "received_date" not in cols:
            conn.execute(text("ALTER TABLE vehicles ADD COLUMN received_date DATE"))

    # 3) Cargar demo (import diferido para evitar ciclos)
    from autogo_erp.seed import cargar_demo_si_vacio
    db = SessionLocal()
    try:
        cargar_demo_si_vacio(db)
    finally:
        db.close()

# Servir archivos estáticos (/static/…)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página de inicio
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return HTMLResponse("<h1>AutoGo ERP</h1><p>Visita <a href='/docs'>/docs</a></p>")

# Healthcheck simple
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

