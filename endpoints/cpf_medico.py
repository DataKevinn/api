import sqlite3
import requests
from auth.validacao import validacao
from flask import jsonify
from config import DB_PATH  # Importa o caminho do banco de config.py




def get_string(texto, inicio, fim):
    try:
        return texto.split(inicio)[1].split(fim)[0]
    except Exception:
        return "S/N"

def consultar_medico(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    if not validacao(token):
        return jsonify({'erro': 'Token invalido, chame @klzinnn para adquirir'})


    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'TS0142589a=0121427f93649e8441c675ec131e2c39c7d4ae856343d743fba7e9f824c12a12dc2f5c35cc8e9972f689b776be01a9e98c58b74f3f',
    'DNT': '1',
    'Referer': 'https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}
    params = {
            'cpf': ''+cpf+'',
        }

    response = requests.get('https://cnes.datasus.gov.br/services/profissionais', params=params,headers=headers).text
    if '"id":"' in response:
        id = get_string(response, '"id":"', '"')
        nome = get_string(response, 'nome":"', '"')
        response1 = requests.get('https://cnes.datasus.gov.br/services/profissionais/'+id+'', headers=headers).text
        if '"vinculos"' in response1:
            cbo = get_string(response1, 'cbo":"', '"')
            dsCbo = get_string(response1, 'dsCbo":"', '"')
            noFant = get_string(response1, 'noFant":"', '"')
            estado = get_string(response1, 'estado":"', '"')
            cns = get_string(response1, 'cnsMaster":"', '"')
            cns_normal = get_string(response1, 'cns":"', '"')
            print(response1)
            return jsonify({'mensagem': 'o cpf pertence a um medico, que esta na ativa', 'nome': nome, 'cns': cns_normal, 'cns_master': cns, 'dsCbo': dsCbo, 'noFant': noFant, 'estado': estado})
        else:
            return jsonify({'mensagem': 'o cpf pertence a um medico mais nao possui vinculo a nenhum hospital'})
    elif '[]' in response:
        return jsonify({'mensagem': 'cpf nao pertence a nenhum medico'})
    else:
        return jsonify({'mensagem': 'resposta nao indentificada'})