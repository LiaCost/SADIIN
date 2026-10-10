from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/catalogo", tags=["Catálogo e Doenças"])

@router.get("/medicamentos/{id_medicamento}")
async def detalhes_medicamento(id_medicamento: int):
    return {
        "id": id_medicamento,
        "nome": "Medicamento Exemplo",
        "bula": "Informações completas de indicação e posologia extraídas do catálogo."
    }

@router.get("/doencas/{cid}")
async def detalhes_doenca(cid: str):
    return {
        "cid": cid.upper(),
        "nome": "Patologia de Exemplo",
        "sintomas": ["Sintoma 1", "Sintoma 2"],
        "tratamento": "Orientações oficiais de prevenção e tratamento."
    }