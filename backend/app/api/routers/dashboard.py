from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboards Regionais"])

@router.get("/indicadores")
async def indicadores_regionais(estado: str, cidade: str = None):
    return {
        "localidade": f"{cidade or 'Geral'} - {estado}",
        "kpis": [
            {"titulo": "Variação de Casos", "valor": "-18.4%", "tendencia": "queda"}
        ]
    }