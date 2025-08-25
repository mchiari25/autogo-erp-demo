# Forzar redeploy limpio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import pkgutil, importlib, pathlib

# DB / modelos / seed
from autogo_erp.database import SessionLocal, Base, engine
from autogo_erp.seed import cargar_demo_si_vacio

# 👇 IMPORTS necesarios para la “mini migración” de la columna plate
from sqlalchemy import inspect, text

app = FastAPI(title="AutoGo ERP")

# Plantillas (si usas autos_ui.html en templates/)
templates = Jinja2Templates(directory="templates")

# Incluir routers automáticamente desde autogo_erp/routers/*.py
def include_all_routers(app: FastAPI):
    routers_path = pathlib.Path(__file__).parent / "routers"
    package_name = "autogo_erp.routers"
    if routers_path.exists():
        for _, module_name, _ in pkgutil.iter_modules([str(routers_path)]):
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)

include_all_routers(app)

# --- ensure DB column 'plate' exists in 'vehicles' ---
# (Esto corre al importar main.py; en SQLite es seguro. No borra datos.)
insp = inspect(engine)
cols = [c["name"] for c in insp.get_columns("vehicles")]
if "plate" not in cols:
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE vehicles ADD COLUMN plate VARCHAR"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_vehicles_plate ON vehicles(plate)"))

# Crear tablas y cargar demo si está vacío
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        cargar_demo_si_vacio(db)
    finally:
        db.close()

# Servir estáticos (/static/…)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página simple (si tienes templates/autos_ui.html; si no, deja un texto)
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    # Si tienes templates/autos_ui.html, descomenta la línea de abajo y comenta la de texto
    # return templates.TemplateResponse("autos_ui.html", {"request": request})
    return HTMLResponse("<h1>AutoGo ERP</h1><p>Visita <a href='/docs'>/docs</a></p>")


