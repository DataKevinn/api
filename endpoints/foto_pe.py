import requests
import base64
from auth.validacao import validacao
from bs4 import BeautifulSoup
from flask import jsonify

# Configurações gerais
COOKIES = {
    'JSESSIONID': '5BFDA385DB90B5F9CCACE2D1962C8E1E',
    'cod': '1',
    'csd': '2',
}

HEADERS = {
    'Host': 'servicos.sds.pe.gov.br',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://servicos.sds.pe.gov.br',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'https://servicos.sds.pe.gov.br/relatorioscivil/formularioCadastroCivil.sds?codigo=CONCADCIVIL',
}

def consultar_rg(valor, mae, token):
    # Validação do token
    if not token or token != "cerollindo":
        return jsonify({'erro': 'Token inválido'})

    # Permitir que o campo mae seja vazio
    mae = mae if mae else ''

    # Parâmetros da requisição
    payload = {
        'rg': '',
        'nome': valor,
        'nomeQueContenha': 'false',
        'nomeMae': mae,
        'nomeMaeQueContenha': 'false',
    }

    # Fazer a requisição
    response = requests.post('https://servicos.sds.pe.gov.br/relatorioscivil/consultaCadastroCivil.sds', cookies=COOKIES, headers=HEADERS, data=payload)

    # Verificar se a resposta contém 'Nome'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table', {"width": "760px"})

        if not tabela:
            # Tentativa de detectar mensagens de erro no HTML
            mensagem_erro = soup.find('div', class_='mensagem-erro')  # Exemplo de classe fictícia
            if mensagem_erro:
                return jsonify({'erro': mensagem_erro.text.strip()})

            return jsonify({'erro': 'Tabela não encontrada na resposta. Verifique os parâmetros fornecidos.'})

        linhas = tabela.find_all('tr', {"onmousemove": "marcar(this);"})
        resultados = []

        for linha in linhas:
            colunas = linha.find_all('td')
            link_ficha = colunas[1].find('a')['href'] if colunas[1].find('a') else ""
            ficha_id = link_ficha.split('ficha=')[-1] if "ficha=" in link_ficha else ""

            if ficha_id:
                ficha = consultar_ficha(ficha_id)
                resultados.append(ficha)

        return jsonify(resultados)
    else:
        return jsonify({'erro': 'Nenhum resultado encontrado ou erro na consulta.'})



def consultar_ficha(ficha_id):
    url_ficha = f"https://servicos.sds.pe.gov.br/relatorioscivil/consultaRegistroCadastroCivil.sds?ficha={ficha_id}"
    response = requests.get(url_ficha, cookies=COOKIES, headers=HEADERS)

    if response.status_code == 200:
        return processar_ficha(response.text, ficha_id)
    else:
        return {'erro': f"Erro ao consultar ficha (status {response.status_code})."}

def processar_ficha(html, ficha_id):
    soup = BeautifulSoup(html, 'html.parser')
    dados = {}

    def extrair_valor_por_label(soup, label):
        campo = soup.find('td', string=label)
        if campo:
            input_tag = campo.find_next_sibling('td').find('input')
            if input_tag:
                return input_tag.get('value', '').strip()
        return None

    # Labels a serem extraídas
    labels = [
        "UNIDADE:", "POSTO:", "SERIE:", "CEDULA:", "NUM. RG:", "VIA:", "FICHA:", 
        "NOME:", "NOME ANTERIOR:", "NOME PAI:", "NOME MÃE:", "DATA DE NASCIMENTO:", 
        "NATURALIDADE:", "UF:", "NACIONALIDADE:", "CPF:", "PIS/PASEP:", 
        "GRAU DE INSTRUÇÃO:", "PROFISSÃO:", "ESTADO CIVIL:", "ALTURA:", 
        "SEXO:", "OLHOS:", "CUTIS:", "COR DO CABELO:", "TIPO DO CABELO:", 
        "LOGRADOURO:", "TELEFONE:", "DATA IDENTIFICAÇÃO:", "DATA EMISSÃO:", 
        "DATA ATENDIMENTO:"
    ]

    for label in labels:
        dados[label.strip(':')] = extrair_valor_por_label(soup, label)

    # Extraindo observação
    observacao_tag = soup.find('td', string="OBSERVAÇÃO:")
    if observacao_tag:
        textarea_tag = observacao_tag.find_next_sibling('td').find('textarea')
        if textarea_tag:
            dados['Observação'] = textarea_tag.text.strip()

    # Obtendo a imagem
    dados['Imagem'] = obter_imagem(ficha_id)

    return dados


def obter_imagem(ficha_id):
    headers = HEADERS.copy()
    headers['Referer'] = f"https://servicos.sds.pe.gov.br/relatorioscivil/consultaRegistroCadastroCivil.sds?ficha={ficha_id}"
    url = "https://servicos.sds.pe.gov.br/relatorioscivil/mostrarImagem"
    response = requests.get(url, cookies=COOKIES, headers=headers)

    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        return f"Erro ao obter a imagem: {response.status_code}"