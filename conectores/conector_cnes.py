import requests
import json

def listar_estabelecimentos_cnes(limite=20, offset=0):
    url = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos"
    headers = {"Accept": "application/json"}
    parametros = {"limit": limite, "offset": offset}
    
    resposta = requests.get(url, headers=headers, params=parametros, timeout=15)
    resposta.raise_for_status() 
    return resposta.json()

def normalizar_lista_cnes(dado_bruto_api):
    lista_limpa = []
    lista_hospitais = dado_bruto_api.get('estabelecimentos', [])
    
    for dado in lista_hospitais:
        dado_limpo = {
            "cnes": dado.get("codigo_cnes"),
            "razaoSocial": dado.get("nome_razao_social"),
            "nomeFantasia": dado.get("nome_fantasia") or dado.get("nome_razao_social"),
            "tipoGestao": dado.get("tipo_gestao"),
            "tipoUnidadeId": dado.get("codigo_tipo_unidade"),
            "codigoEstabelecimentoSaude": dado.get("codigo_estabelecimento_saude"),
            "cep": dado.get("codigo_cep_estabelecimento"),
            "endereco": dado.get("endereco_estabelecimento"),
            "numero": dado.get("numero_estabelecimento"),
            "bairro": dado.get("bairro_estabelecimento"),
            "municipioId": dado.get("codigo_municipio"),
            "ufId": dado.get("codigo_uf"),
            "latitude": dado.get("latitude_estabelecimento_decimo_grau"),
            "longitude": dado.get("longitude_estabelecimento_decimo_grau"),
            "telefone": dado.get("numero_telefone_estabelecimento"),
            "turnoAtendimento": dado.get("descricao_turno_atendimento"),
            "atendeSus": True if dado.get("estabelecimento_faz_atendimento_ambulatorial_sus") == 'SIM' else False,
            
            # Indicadores
            "possuiCentroCirurgico": bool(dado.get("estabelecimento_possui_centro_cirurgico")),
            "possuiCentroObstetrico": bool(dado.get("estabelecimento_possui_centro_obstetrico")),
            "possuiCentroNeonatal": bool(dado.get("estabelecimento_possui_centro_neonatal")),
            "possuiAtendimentoHospitalar": bool(dado.get("estabelecimento_possui_atendimento_hospitalar")),
            "possuiServicoApoio": bool(dado.get("estabelecimento_possui_servico_apoio")),
            "possuiAtendimentoAmbulatorial": bool(dado.get("estabelecimento_possui_atendimento_ambulatorial")),
            
            "dataAtualizacao": dado.get("data_atualizacao")
        }
        lista_limpa.append(dado_limpo)
        
    return lista_limpa

#EXECUÇÃO
if __name__ == "__main__":
    todos_dados = []
    limite_por_pagina = 20
    offset = 0
    paginas_para_puxar = 3 # Puxando 3 páginas (60 postos) para teste rápido
    
    print("Iniciando extração do CNES (Datasus)...")
    
    try:
        for pagina in range(paginas_para_puxar):
            print(f"-> Buscando página {pagina + 1} (Offset: {offset})...")
            
            dados_brutos = listar_estabelecimentos_cnes(limite=limite_por_pagina, offset=offset)
            hospitais = dados_brutos.get('estabelecimentos', [])
            
            if not hospitais:
                print("Fim dos dados alcançado.")
                break
                
            dados_limpos = normalizar_lista_cnes(dados_brutos)
            todos_dados.extend(dados_limpos)
            
            offset += limite_por_pagina
            
        #EXPORTAÇÃO JSON
        nome_arquivo = 'dados_normalizados_cnes.json'
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(todos_dados, arquivo, indent=4, ensure_ascii=False)
            
        print(f"\nSucesso! {len(todos_dados)} estabelecimentos foram salvos no arquivo '{nome_arquivo}'.")

    except Exception as erro:
        print(f"Ocorreu um erro durante a extração: {erro}")