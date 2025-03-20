import requests
import json
import time
from auth.validacao import validacao
from flask import jsonify, make_response
from config import DB_PATH  # Importa o caminho do banco de config.py



def GetStr(texto, inicio, fim):
    try:
        return texto.split(inicio)[1].split(fim)[0]
    except Exception:
        return "S/N"

def login():
    headers = {
    'accept': 'application/json',
    'Referer': 'https://si-pni.saude.gov.br/',
    'X-Authorization': 'Basic YV9uaW5laEBob3RtYWlsLmNvbTptZTk4NDc5OTk0NQ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
}

    response = requests.post('https://servicos-cloud.saude.gov.br/pni-bff/v1/autenticacao/tokenAcesso', headers=headers).text
    token = GetStr(response, '"accessToken":"', '"')

    
    with open("./token_sipni.txt", 'r+') as f:
        f.truncate(0)
    f = open("./token_sipni.txt", 'a+')
    f.write(f"{token}")
    f.close()
    
def pegar_token():
    lista = open("token_sipni.txt", "r", encoding='utf-8').read().splitlines()
    for i in lista:
          token = i.split('|')[0]
          return token

    
def consulta_cpf_2(cpf, token):

    auth = validacao(token)
    if auth != 1:
        return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})
    
    
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://si-pni.saude.gov.br/',
    'Authorization': 'Bearer '+str(pegar_token()),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
}

    response = requests.get('https://servicos-cloud.saude.gov.br/pni-bff/v1/cidadao/cpf/'+cpf, headers=headers).text
    print(response)
    
    if '"code":200' in response:
        response_data = json.loads(response)
        response_json = jsonify({'dados': response_data, 'mensagem': 'deixa o credito pf'})
        response = make_response(response_json)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print(login())
        response_json = jsonify({'dados': 'consulte novamente, api reiniciou', 'mensagem': 'deixa o credito pf'})
        response = make_response(response_json)
        response.headers['Content-Type'] = 'application/json'
        return response