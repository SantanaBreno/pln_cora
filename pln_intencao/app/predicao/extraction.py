# Arquivo para extração de informações
import re

# Função para extrair reguladores
def extrair_reguladores(tokens):
    dicionario = {"anbima", "nuclea", "bacen", "cvm", "b3", "selic", "banco do brasil", "anpd", "bsm", "febraban", "apimec", "abbc", "coaf"}
    padrao = r'\b(?:' + '|'.join(re.escape(palavra) for palavra in dicionario) + r')\b'

    if isinstance(tokens, str):
        tokens = tokens.split()

    reguladores_encontrados = [token for token in tokens if re.search(padrao, token.lower())]

    return reguladores_encontrados

# Função para encontrar datas
def encontrar_datas(texto):
    padrao_data = r'\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b'
    datas = re.findall(padrao_data, texto)
    return datas

# Função para transformar texto em minúsculo
def texto_para_minusculo(texto):
    return texto.lower()
