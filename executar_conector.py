import asyncio
import json
import logging
from pathlib import Path
from conectores_dados_abertos.conector_base import ConectorDadosAbertosSUS
from conectores_dados_abertos.enriquecedor_scnes import EnriquecedorSCNES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

async def main():
    print("[*] A iniciar varredura completa de todos os endpoints permitidos...")
    conector = ConectorDadosAbertosSUS()
    enriquecedor = EnriquecedorSCNES("SCNES_DOMINIOS.XLS")
    
    pasta_saida = Path("dados_salvos")
    pasta_saida.mkdir(exist_ok=True)

    for chave in conector.ENDPOINTS_PERMITIDOS.keys():
        print(f"\n[->] A consultar endpoint: {chave}")
        try:
            dados = await conector.consumir_api_selecionada(chave, parametros={"offset": 0, "limit": 5})
            
            if isinstance(dados, str):
                try:
                    dados = json.loads(dados.replace("'", '"'))
                except:
                    pass

            if isinstance(dados, list):
                dados_processados = [enriquecedor.enriquecer_registro(item) if isinstance(item, dict) else item for item in dados]
            elif isinstance(dados, dict):
                dados_processados = {}
                for k, v in dados.items():
                    if isinstance(v, str) and v.startswith("["):
                        try:
                            v = json.loads(v.replace("'", '"'))
                        except:
                            pass
                    if isinstance(v, list):
                        dados_processados[k] = [enriquecedor.enriquecer_registro(item) if isinstance(item, dict) else item for item in v]
                    else:
                        dados_processados[k] = enriquecedor.enriquecer_registro(v) if isinstance(v, dict) else v
            else:
                dados_processados = enriquecedor.enriquecer_registro(dados)

            caminho_arquivo = pasta_saida / f"{chave}.json"
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados_processados, f, ensure_ascii=False, indent=4)

            print(f"[+] Sucesso! Dados salvos e estruturados em: {caminho_arquivo}")
        except Exception as e:
            print(f"[-] Falha ao processar o endpoint '{chave}': {e}")

if __name__ == "__main__":
    asyncio.run(main())