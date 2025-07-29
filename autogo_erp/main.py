from fastapi import FastAPI

app = FastAPI()

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a AutoGo ERP Demo"}

# Endpoint de clientes
@app.get("/clientes")
def get_clientes():
    return [
        {"id": 1, "nombre": "Juan Pérez", "email": "juan@example.com"},
        {"id": 2, "nombre": "Ana Gómez", "email": "ana@example.com"}
    ]

# Endpoint de autos
@app.get("/autos")
def get_autos():
    return [
        {"id": 1, "marca": "Toyota", "modelo": "Corolla", "año": 2022},
        {"id": 2, "marca": "Honda", "modelo": "Civic", "año": 2021}
    ]

# Endpoint de ventas
@app.get("/ventas")
def get_ventas():
    return [
        {"id": 1, "cliente": "Juan Pérez", "auto": "Toyota Corolla", "monto": 15000},
        {"id": 2, "cliente": "Ana Gómez", "auto": "Honda Civic", "monto": 18000}
    ]


