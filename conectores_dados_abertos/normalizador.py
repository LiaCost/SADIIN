import re
import logging

logger = logging.getLogger(__name__)

def normalizar_dados_genericos(bruto: dict) -> dict:
    """
    Normalizador universal e defensivo para todos os endpoints do DATASUS.
    Resolve variações de chaves (aliases), limpa espaços, padroniza nulos
    e corrige inconsistências ou variações de digitação comuns.
    """
    if not isinstance(bruto, dict):
        return bruto

    normalizado = {}

    mapeamento_chaves = {
        # CNES
        "coCnes": "cnes",
        "codigo_cnes": "cnes",
        "co_cnes": "cnes",
        
        # Município / IBGE
        "coMunicipioIbge": "municipio_ibge",
        "co_ibge": "municipio_ibge",
        "ibge": "municipio_ibge",
        "municipio": "municipio_ibge",
        
        # UF
        "sgUf": "uf",
        "unidade_federativa": "uf",
        
        # Nome / Razão Social
        "noFantasia": "nome_fantasia",
        "nome_fantasia": "nome_fantasia",
        "noRazaoSocial": "razao_social",
        "nome_razao_social": "razao_social",
        
        # Competência
        "nu_comp": "competencia",
        "competencia": "competencia",
        "competencia_siaps": "competencia"
    }

    for chave_bruta, valor in bruto.items():
        chave_padrao = mapeamento_chaves.get(chave_bruta, _slugify_chave(chave_bruta))
        
        if valor is None:
            normalizado[chave_padrao] = None
        elif isinstance(valor, str):
            valor_limpo = valor.strip()
            if valor_limpo == "" or valor_limpo.lower() in ["none", "null", "nan", "-"]:
                normalizado[chave_padrao] = None
            else:
                valor_corrigido = re.sub(r'\s+', ' ', valor_limpo)
                normalizado[chave_padrao] = valor_corrigido
        elif isinstance(valor, (int, float)):
            normalizado[chave_padrao] = valor
        elif isinstance(valor, bool):
            normalizado[chave_padrao] = valor
        else:
            normalizado[chave_padrao] = str(valor).strip()

    
    if "uf" in normalizado and normalizado["uf"]:
        uf_val = str(normalizado["uf"])
        if "-" in uf_val:
            uf_val = uf_val.split("-")[-1]
        normalizado["uf"] = uf_val.strip().upper()[:2]

    if "municipio_ibge" in normalizado and normalizado["municipio_ibge"]:
        mun_val = str(normalizado["municipio_ibge"])
        if "-" in mun_val:
            mun_val = mun_val.split("-")[0]
        mun_val = mun_val.split(".")[0].strip()
        normalizado["municipio_ibge"] = mun_val

    if "stAtendeSus" in bruto:
        st = bruto.get("stAtendeSus")
        normalizado["vinculo_sus"] = bool(st) if st is not None else None

    return normalizado

def _slugify_chave(chave: str) -> str:
    """Converte chaves em formato misto (camelCase, etc.) para snake_case limpo."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', chave)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace("-", "_")