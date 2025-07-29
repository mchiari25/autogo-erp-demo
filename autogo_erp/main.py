from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AutoGo ERP Demo funcionando desde main.py!"}

