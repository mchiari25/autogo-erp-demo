from fastapi import FastAPI

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

