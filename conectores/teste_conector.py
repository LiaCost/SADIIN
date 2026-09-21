from conector_cnes import normalizar_lista_cnes

def test_deve_converter_valores_do_sus_para_booleanos():
    dado_simulado = {
        "estabelecimentos": [
            {
                "codigo_cnes": 1234567,
                "nome_fantasia": "POSTO DE TESTE",
                "estabelecimento_faz_atendimento_ambulatorial_sus": "SIM",
                "estabelecimento_possui_centro_cirurgico": 1,
                "estabelecimento_possui_centro_neonatal": 0
            }
        ]
    }
    
    resultado = normalizar_lista_cnes(dado_simulado)
    hospital = resultado[0]
    
    # Verificação (Assert)
    assert hospital["cnes"] == 1234567
    assert hospital["atendeSus"] is True
    assert hospital["possuiCentroCirurgico"] is True
    assert hospital["possuiCentroNeonatal"] is False

def test_deve_usar_razao_social_quando_nao_houver_nome_fantasia():
    dado_simulado = {
        "estabelecimentos": [
            {
                "codigo_cnes": 9999,
                "nome_fantasia": None,
                "nome_razao_social": "PREFEITURA MUNICIPAL DE TESTE"
            }
        ]
    }
    resultado = normalizar_lista_cnes(dado_simulado)
    
    assert resultado[0]["nomeFantasia"] == "PREFEITURA MUNICIPAL DE TESTE"