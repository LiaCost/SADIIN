import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from conectores_dados_abertos.conector_base import ConectorDadosAbertosSUS

@pytest.mark.asyncio
async def test_consumir_api_sih_sucesso():
    conector = ConectorDadosAbertosSUS()
    mock_resposta = [
        {"coCnes": "1234567", "dsProcedimento": "INTERNACAO CLINICA", "qtSus": 10}
    ]
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_resposta
        
        resultado = await conector.consumir_api("assistencia-a-saude/sih-procedimentos-hospitalares")
        
        assert isinstance(resultado, list)
        assert resultado[0]["coCnes"] == "1234567"
        assert resultado[0]["qtSus"] == 10

@pytest.mark.asyncio
async def test_consumir_api_erro_502():
    conector = ConectorDadosAbertosSUS()
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 502
        
        with pytest.raises(HTTPException) as exc_info:
            await conector.consumir_api("assistencia-a-saude/cnes-leitos")
            
        assert exc_info.value.status_code == 502