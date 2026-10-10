from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/busca", tags=["Busca Global e IA"])

class ConsultaBusca(BaseModel):
    termo: str

@router.post("/")
async def busca_global(consulta: ConsultaBusca):
    confianca_ia = 0.90
    if confianca_ia < 0.85:
        raise HTTPException(
            status_code=400, 
            detail="Sintomas complexos. Procure uma unidade de saúde."
        )
    return {
        "termo_pesquisado": consulta.termo,
        "resultados": []
    }