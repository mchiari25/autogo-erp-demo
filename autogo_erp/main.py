from fastapi import Form, HTTPException
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, Base, engine
from .seed import cargar_demo_si_vacio
from . import models

import pkgutil, importlib, pathlib

app = FastAPI(title="AutoGo ERP")

# Configurar plantillas HTML
templates = Jinja2Templates(directory="templates")

# Incluir todos los routers automáticamente
def include_all_routers(app: FastAPI):
    routers_path = pathlib.Path(__file__).parent / "routers"
    package_name = "autogo_erp.routers"
    if routers_path.exists():
        for _, module_name, _ in pkgutil.iter_modules([str(routers_path)]):
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router)

include_all_routers(app)

@app.on_event("startup")
def startup():
    # Crea tablas y carga demo si está vacío
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        cargar_demo_si_vacio(db)
    finally:
        db.close()

# Ruta para renderizar la vista de autos
@app.get("/ver-autos", response_class=HTMLResponse)
async def ver_autos(request: Request):
    return templates.TemplateResponse("autos_ui.html", {"request": request})

# Servir archivos estáticos (logo, favicon, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página de inicio
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Página para UI de autos (versión con acceso a base de datos)
@app.get("/autos-ui", response_class=HTMLResponse)
def autos_ui(request: Request):
    db = SessionLocal()
    try:
        q = request.query_params.get("q")
        p_str = request.query_params.get("p") or "1"
        try:
            p = int(p_str)
            if p < 1: p = 1
        except:
            p = 1
        page_size = 10
        offset = (p - 1) * page_size

        query = db.query(models.Auto)
        if q:
            query = query.filter(
                (models.Auto.marca.contains(q)) | (models.Auto.vin.contains(q))
            )

        items = query.order_by(models.Auto.id.desc()).offset(offset).limit(page_size + 1).all()
        has_more = len(items) > page_size
        autos = items[:page_size]

        html = templates.get_template("autos_ui.html").render(
            {"request": request, "autos": autos, "p": p, "has_more": has_more}
        )
        return HTMLResponse(content=html, media_type="text/html; charset=utf-8")
    finally:
        db.close()
@app.get("/autos-nuevo", response_class=HTMLResponse)
def autos_nuevo(request: Request):
    return templates.TemplateResponse("new_auto.html", {"request": request})

@app.post("/autos-crear")
async def autos_crear(
    request: Request,
    marca: str = Form(...),
    modelo: str = Form(...),
    vin: str = Form(...),
    color: str = Form(...),
    anio: int = Form(...),
    precio: float = Form(...)
):
    db = SessionLocal()
    try:
        # Validar VIN único
        existe = db.query(models.Auto).filter(models.Auto.vin == vin).first()
        if existe:
            return templates.TemplateResponse(
                "new_auto.html",
                {
                    "request": request,
                    "error": "El VIN ya existe. Ingresa otro.",
                    "form": {
                        "marca": marca,
                        "modelo": modelo,
                        "vin": vin,
                        "color": color,
                        "anio": anio,
                        "precio": precio,
                    },
                },
                status_code=400,
            )

        # Crear registro con color incluido
        auto = models.Auto(
            marca=marca,
            modelo=modelo,
            vin=vin,
            color=color,
            anio=anio,
            precio=precio,
        )
        db.add(auto)
        db.commit()

        # Volver al listado con mensaje
        return RedirectResponse(url="/autos-ui?msg=creado", status_code=303)
    finally:
        db.close()
@app.get("/autos-editar/{auto_id}", response_class=HTMLResponse)
def autos_editar(request: Request, auto_id: int):
    db = SessionLocal()
    try:
        auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
        if not auto:
            raise HTTPException(status_code=404, detail="Auto no encontrado")
        return templates.TemplateResponse("edit_auto.html", {"request": request, "auto": auto})
    finally:
        db.close()


@app.post("/autos-actualizar/{auto_id}")
async def autos_actualizar(
    request: Request,
    auto_id: int,
    marca: str = Form(...),
    modelo: str = Form(...),
    vin: str = Form(...),
    color: str = Form(...),
    anio: int = Form(...),
    precio: float = Form(...)
):
    db = SessionLocal()
    try:
        auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
        if not auto:
            raise HTTPException(status_code=404, detail="Auto no encontrado")

        # VIN único (excluye el propio auto)
        existe = db.query(models.Auto).filter(models.Auto.vin == vin, models.Auto.id != auto_id).first()
        if existe:
            return templates.TemplateResponse(
                "edit_auto.html",
                {
                    "request": request,
                    "auto": auto,
                    "error": "El VIN ya existe. Ingresa otro.",
                    "form": {"marca": marca, "modelo": modelo, "vin": vin, "color": color, "anio": anio, "precio": precio},
                },
                status_code=400,
            )

        auto.marca = marca
        auto.modelo = modelo
        auto.vin = vin
        auto.color = color
        auto.anio = anio
        auto.precio = precio
        db.commit()
        return RedirectResponse(url="/autos-ui?msg=actualizado", status_code=303)
    finally:
        db.close()


@app.post("/autos-eliminar/{auto_id}")
def autos_eliminar(auto_id: int):
    db = SessionLocal()
    try:
        auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
        if auto:
            db.delete(auto)
            db.commit()
        return RedirectResponse(url="/autos-ui?msg=eliminado", status_code=303)
    finally:
        db.close()


