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


def consulta_cpf_cnh(cpf, token):
    ...
