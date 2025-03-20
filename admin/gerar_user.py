import uuid
import sqlite3
from auth.validacao import validacao
from flask import jsonify


def gerar_aceso(token, dia, mes, ano):
    if token == 'klzindeussupremo':
        chave_token = str(uuid.uuid4())  # Converter UUID para string
        conn = sqlite3.connect('aut.db', check_same_thread=False, timeout=10)
        cursor = conn.cursor()
        
        # Criar a tabela se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            token TEXT UNIQUE,
                            dia INTEGER,
                            mes INTEGER,
                            ano INTEGER
                        )''')

        try:
            # Inserir o novo token
            cursor.execute("INSERT INTO tokens (token, dia, mes, ano) VALUES (?, ?, ?, ?)", (chave_token, dia, mes, ano))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify(erro="Token já existe"), 400
        
        conn.close()
        return jsonify(token=chave_token)
    else:
        return jsonify(erro='Chave Inválida'), 403
