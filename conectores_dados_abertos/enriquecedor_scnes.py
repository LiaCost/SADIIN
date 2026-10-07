import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class EnriquecedorSCNES:
    def __init__(self, caminho_xls: str = "SCNES_DOMINIOS.XLS"):
        self.caminho_xls = Path(caminho_xls)
        self.dominios = {}
        
        if self.caminho_xls.exists():
            self._carregar_todas_planilhas()
        else:
            logger.warning(f"Ficheiro de domínios {caminho_xls} não encontrado na raiz. O enriquecimento será ignorado.")

    def _carregar_todas_planilhas(self):
        """Lê todas as abas do Excel de domínios do SCNES dinamicamente."""
        try:
            xls = pd.ExcelFile(self.caminho_xls)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                chave_dominio = sheet_name.strip().lower().replace(" ", "_")
                
                colunas = [str(c).strip() for c in df.columns]
                if len(colunas) >= 2:
                    col_codigo = colunas[0]
                    col_descricao = colunas[1]
                    
                    mapa = {}
                    for _, row in df.iterrows():
                        cod = str(row[col_codigo]).strip()
                        desc = str(row[col_descricao]).strip()
                        if cod and cod.lower() != 'nan':
                            mapa[cod] = desc
                            
                    self.dominios[chave_dominio] = mapa
                    logger.info(f"Domínio carregado: '{chave_dominio}' com {len(mapa)} registos.")
        except Exception as e:
            logger.error(f"Erro ao carregar o ficheiro SCNES_DOMINIOS.XLS: {e}")

    def enriquecer_registro(self, registro: dict) -> dict:
        """
        Cruza dinamicamente os códigos de qualquer campo do registro 
        com os dicionários carregados de todas as abas do SCNES.
        """
        reg_enriquecido = registro.copy()
        
        for campo, valor in list(registro.items()):
            if valor is not None and str(valor).strip() != "":
                valor_str = str(valor).strip()
                
                for nome_dominio, mapa_valores in self.dominios.items():
                    partes_dominio = nome_dominio.split("_")
                    if any(parte in campo.lower() for parte in partes_dominio):
                        if valor_str in mapa_valores:
                            reg_enriquecido[f"{campo}_descricao"] = mapa_valores[valor_str]
                            break
                            
        return reg_enriquecido