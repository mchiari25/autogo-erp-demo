


from fastapi import FastAPI

from fastapi import FastAPI

app = FastAPI()

# Ruta de prueba: listar autos
@app.get("/autos")
def listar_autos():
    return [
        {"marca": "Toyota", "modelo": "Corolla", "año": 2022, "precio": 18000},
        {"marca": "Ford", "modelo": "Bronco", "año": 2024, "precio": 35000},
        {"marca": "Honda", "modelo": "Civic", "año": 2021, "precio": 17000}
    ]
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AutoGo ERP Demo funcionando desde main.py!"}

@app.get("/clientes")
def get_clientes():
    return [
        {"id": 1, "nombre": "Cliente A", "email": "clienteA@autogo.com"},
        {"id": 2, "nombre": "Cliente B", "email": "clienteB@autogo.com"}
    ]


