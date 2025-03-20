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


def consultar_rg(valor, mae, token):
    ...
