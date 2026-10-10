from fastapi import APIRouter, Depends
from app.integrations.datasus.cnes import CnesConnector

router = APIRouter(prefix="/api/v1/ubs", tags=["Unidades de Saúde"])

@router.get("/{cnes}")
async def obter_detalhes_ubs(cnes: str):
    return {
        "cnes": cnes,
        "nome": "UBS REFERÊNCIA",
        "endereco": "Endereço oficial obtido via base CNES",
        "status_funcionamento": "Aberto"
    }

@router.get("/{cnes}/infraestrutura")
async def obter_infraestrutura(cnes: str):
    connector = CnesConnector()
    equipamentos = await connector.buscar_equipamentos(cnes)
    leitos = await connector.buscar_leitos(cnes)
    return {
        "cnes": cnes,
        "equipamentos": equipamentos,
        "leitos": leitos
    }

@router.get("/{cnes}/historico-atendimentos")
async def obter_historico(cnes: str):
    return {
        "cnes": cnes,
        "historico_semanal": [
            {"dia": "Segunda", "atendimentos": 120},
            {"dia": "Terça", "atendimentos": 145},
            {"dia": "Quarta", "atendimentos": 90},
            {"dia": "Quinta", "atendimentos": 160},
            {"dia": "Sexta", "atendimentos": 110}
        ]
    }