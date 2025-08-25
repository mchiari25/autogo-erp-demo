# Forzar redeploy limpio
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
    if routers_path.exists():
        for _, module_name, _ in pkgutil.iter_modules([str(routers_path)]):
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)

include_all_routers(app)

# Crear tablas y cargar demo si está vacío
@app.on_event("startup")
def startup():
    # Crear tablas (si no existen)
    Base.metadata.create_all(bind=engine)

    # Asegurar que exista la columna plate en vehicles
    insp = inspect(engine)
    try:
        cols = [c["name"] for c in insp.get_columns("vehicles")]
        if "plate" not in cols:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE vehicles ADD COLUMN plate VARCHAR"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_vehicles_plate ON vehicles(plate)"))
    except Exception as e:
        print("⚠️ Error verificando o modificando tabla vehicles:", e)

    # Cargar datos demo
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

