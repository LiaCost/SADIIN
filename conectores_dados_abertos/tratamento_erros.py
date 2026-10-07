from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def tratar_erro_requisicao(status_code: int, detalhes_extras: str = ""):
    """Mapeia os códigos de erro HTTP conforme os requisitos do projeto."""
    if status_code == 404:
        logger.warning(f"Recurso não encontrado na API aberta. {detalhes_extras}")
        raise HTTPException(status_code=404, detail="Recurso ou identificador não encontrado na base do DATASUS.")
    elif status_code == 429:
        logger.error(f"Rate limit excedido no DATASUS. {detalhes_extras}")
        raise HTTPException(status_code=429, detail="Limite de requisições excedido na API do DATASUS.")
    elif status_code >= 500:
        logger.error(f"Erro no servidor DATASUS (502/504). {detalhes_extras}")
        raise HTTPException(status_code=502, detail="Erro de gateway ou indisponibilidade temporária na API do DATASUS.")
    else:
        raise HTTPException(status_code=status_code, detail=f"Erro inesperado na API externa: {detalhes_extras}")