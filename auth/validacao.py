import sqlite3
from datetime import datetime
from flask import request


def validacao(token):
    data_formatada = '%d/%m/%Y'

    with sqlite3.connect('aut.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT validade FROM acesso WHERE key = :token LIMIT 1", {'token': token})
        acesso_data = cursor.fetchone()
        if not acesso_data:
            return False

        ultimo_id = request.remote_addr
        cursor.execute("UPDATE acesso SET ultimo_id = :ultimo_id WHERE key = :token", {'ultimo_id': ultimo_id, 'token': token})

    try:
        data = datetime.strptime(acesso_data[0], data_formatada)
    except ValueError:
        return False

    return data >= datetime.today()