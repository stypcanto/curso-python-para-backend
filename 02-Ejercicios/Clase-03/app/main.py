from fastapi import FastAPI

app = FastAPI(
    title="Mi primera API con FastAPI",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "¡Hola, mundo! Helpdesk API funcionando correctamente."}