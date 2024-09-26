from app.predicao.extraction import extrair_reguladores, encontrar_datas, texto_para_minusculo

# Teste para extração de reguladores
def test_extrair_reguladores():
    texto_exemplo = "Quero a nova regulamentação da Anbima em 15/08/2023 sobre fundos de investimento."
    reguladores = extrair_reguladores(texto_exemplo)
    assert reguladores == ["Anbima"], f"Esperava-se ['Anbima'], mas foi retornado {reguladores}"

# Teste para extração de datas
def test_encontrar_datas():
    texto_exemplo = "Quero a nova regulamentação da Anbima em 15/08/2023 sobre fundos de investimento."
    datas = encontrar_datas(texto_exemplo)
    assert datas == ["15/08/2023"], f"Esperava-se ['15/08/2023'], mas foi retornado {datas}"

# Teste para transformar o texto em minúsculo
def test_texto_para_minusculo():
    texto_exemplo = "Quero a nova regulamentação da Anbima em 15/08/2023 sobre fundos de investimento."
    texto_minusculo = texto_para_minusculo(texto_exemplo)
    assert texto_minusculo == texto_exemplo.lower(), f"Esperava-se o texto em minúsculas, mas foi retornado {texto_minusculo}"
