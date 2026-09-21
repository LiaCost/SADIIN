# Conector CNES - Dados Abertos DATASUS

Este módulo extrai, normaliza e exporta dados de estabelecimentos de saúde da API pública do DATASUS.

## O que este conector faz?
1. Consulta a rota `GET /cnes/estabelecimentos`.
2. Trata a paginação automática usando `limit` e `offset`.
3. Normaliza os nomes das variáveis (snake_case para camelCase) e converte indicadores do SUS (`1`/`0` e `'SIM'`) para booleanos padrão (`True`/`False`).
4. Exporta o resultado para um arquivo `dados_normalizados_cnes.json` para facilitar o *seed* no banco de dados da aplicação.

## Como rodar
Instale as dependências:
```bash
pip install -r requirements.txt