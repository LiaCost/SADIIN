from fastapi import FastAPI
from app.api.routers import ubs, catalogo, dashboard, busca

app = FastAPI(title="BRchain API - Backend", version="1.0.0")

app.include_router(ubs.router)
app.include_router(catalogo.router)
app.include_router(dashboard.router)
app.include_router(busca.router)

@app.get("/")
async def root():
    return {"status": "online", "modulo": "Conector CNES e Endpoints do Protótipo - Lucas & Marina"}