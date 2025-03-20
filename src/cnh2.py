import requests
import json
import time
from auth.validacao import validacao
from flask import jsonify, make_response


def GetStr(texto, inicio, fim):
    try:
        return texto.split(inicio)[1].split(fim)[0]
    except Exception:
        return "S/N"
    
    
def consulta_cpf_cnh_reds(cpf, token):
    
    inicio = time.time()
    auth = validacao(token)
    if auth != 1:
        return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})
    
    
    url = "https://websids-reds.policiamilitar.mg.gov.br//webscraper/v1/condutor"
    payload = {
        "login": "pm1659374",
        "senha": "G517348@",
        "tipoPesquisa": "CPF",
        "tipoCNH": None,
        "cnh": None,
        "ufCNH": None,
        "cpf": cpf
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.0 Safari/537.36 Edg/105.0.1300.0"
    }

    response = requests.post(url, json=payload, headers=headers).text

    
    fim = time.time()
    tempo_total = fim - inicio
    tempo_total2 = str(tempo_total)
    if 'NENHUM REGISTRO LOCALIZADO NA BINCO NEM NO IMPEDIMENTO' in response:
        return jsonify({'erro': 'esse cpf nao possui cnh'})
    if 'Falha ao efetuar login no sistema REDS' in response:
        return jsonify({'erro': 'Retestar o servidor nao testou'})
    if 'Verifique novamente o nome de usuário e a senha e tente novamente' in response:
        return jsonify({'erro': 'CONTATAR ADMIN URGENTE   CONTATAR ADMIN URGENTE    CONTATAR ADMIN URGENTE   CONTATAR ADMIN URGENTE    CONTATAR ADMIN URGENTE   CONTATAR ADMIN URGENTE'})
    if 'nome" : "' in response:
        response_data = json.loads(response)
        response_json = jsonify({'dados': response_data, 'mensagem': 'Esse modulo e muito lento!','tempo': tempo_total2[:4] })
        response = make_response(response_json)
        response.headers['Content-Type'] = 'application/json'
        return response