import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from conectores_dados_abertos.normalizador import normalizar_dados_genericos
from conectores_dados_abertos.tratamento_erros import tratar_erro_requisicao
import logging

logger = logging.getLogger(__name__)

class ConectorDadosAbertosSUS:
    ENDPOINTS_PERMITIDOS = {
        "cnes_equipamentos": "assistencia-a-saude/cnes-equipamentos",
        "cnes_leitos": "assistencia-a-saude/cnes-leitos",
        "cnes_profissionais": "assistencia-a-saude/cnes-profissionais",
        "cnes_servicos": "assistencia-a-saude/cnes-servicos-especializados",
        "hospitais_leitos": "assistencia-a-saude/hospitais-e-leitos",
        "sia_ambulatorial": "assistencia-a-saude/sia-procedimentos-ambulatoriais",
        "sih_hospitalar": "assistencia-a-saude/sih-procedimentos-hospitalares",
        "unidade_basica_saude": "assistencia-a-saude/unidade-basicas-de-saude",
        "estabelecimentos": "cnes/estabelecimentos",
        "estado_nutricional": "sisvan/estado-nutricional",
        "siaps_atendimento_individual": "atencao-primaria/siaps-atendimento-individual",
        "siaps_cadastro_individual": "atencao-primaria/siaps-cadastro-individual"
    }

    def __init__(self, base_url: str = "https://apidadosabertos.saude.gov.br"):
        self.base_url = base_url.split("#")[0].rstrip("/")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException))
    )
    async def consumir_api_selecionada(self, chave_endpoint: str, parametros: dict = None) -> list | dict:
        if chave_endpoint not in self.ENDPOINTS_PERMITIDOS:
            raise ValueError(f"Endpoint '{chave_endpoint}' não faz parte do escopo definido.")

        caminho = self.ENDPOINTS_PERMITIDOS[chave_endpoint].lstrip("/")
        url = f"{self.base_url}/{caminho}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=parametros)
                
                if response.status_code != 200:
                    tratar_erro_requisicao(response.status_code, f"API: {chave_endpoint}")
                
                dados_brutos = response.json()
                
                if isinstance(dados_brutos, list):
                    lista_itens = dados_brutos
                elif isinstance(dados_brutos, dict):
                    lista_itens = None
                    for chave_possivel in ["resultado", "dados", chave_endpoint, list(dados_brutos.keys())[0]]:
                        if chave_possivel in dados_brutos and isinstance(dados_brutos[chave_possivel], list):
                            lista_itens = dados_brutos[chave_possivel]
                            break
                    
                    if lista_itens is None:
                        for v in dados_brutos.values():
                            if isinstance(v, list):
                                lista_itens = v
                                break
                    
                    if lista_itens is None:
                        lista_itens = [dados_brutos] 
                else:
                    lista_itens = [dados_brutos]

                return [normalizar_dados_genericos(item) if isinstance(item, dict) else item for item in lista_itens]
                
            except httpx.TimeoutException:
                logger.error(f"Timeout de 30s esgotado ao aceder à API: {chave_endpoint}")
                tratar_erro_requisicao(504, "Timeout na requisição externa")
            except httpx.NetworkError:
                logger.error(f"Falha de rede ao tentar conectar ao DATASUS na API: {chave_endpoint}")
                raise