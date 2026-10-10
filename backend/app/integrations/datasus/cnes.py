from app.integrations.datasus.client import DatasusClient

class CnesConnector:
    def __init__(self):
        self.client = DatasusClient()
        self.ENDPOINTS = {
            "servicos": "assistencia-a-saude/cnes-servicos-especializados",
            "equipamentos": "assistencia-a-saude/cnes-equipamentos",
            "leitos": "assistencia-a-saude/cnes-leitos"
        }

    async def _normalizar_resposta(self, dados_brutos) -> list:
        if isinstance(dados_brutos, dict):
            for valor in dados_brutos.values():
                if isinstance(valor, list):
                    return valor
        return dados_brutos if isinstance(dados_brutos, list) else []

    async def buscar_equipamentos(self, cnes: str) -> list:
        dados = await self.client.get(self.ENDPOINTS["equipamentos"], {"co_cnes": cnes})
        lista = await self._normalizar_resposta(dados)
        filtrados = [eq for eq in lista if str(eq.get("co_cnes")) == str(cnes)]
        if filtrados:
            ultima_comp = max([eq.get("nu_comp", 0) for eq in filtrados])
            filtrados = [eq for eq in filtrados if eq.get("nu_comp") == ultima_comp]
        return filtrados

    async def buscar_leitos(self, cnes: str) -> list:
        dados = await self.client.get(self.ENDPOINTS["leitos"], {"co_cnes": cnes})
        lista = await self._normalizar_resposta(dados)
        filtrados = [l for l in lista if str(l.get("co_cnes")) == str(cnes)]
        if filtrados:
            ultima_comp = max([l.get("nu_comp", 0) for l in filtrados])
            filtrados = [l for l in filtrados if l.get("nu_comp") == ultima_comp]
        return filtrados

    async def buscar_servicos(self, cnes: str) -> list:
        dados = await self.client.get(self.ENDPOINTS["servicos"], {"co_cnes": cnes})
        lista = await self._normalizar_resposta(dados)
        return [s for s in lista if str(s.get("co_cnes")) == str(cnes)]