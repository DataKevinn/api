import sqlite3
from auth.validacao import validacao
from flask import jsonify
from config import DB_PATH  # Importa o caminho do banco de config.py


def consulta_email_cpf(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    if not validacao(token):
        return jsonify({'erro': 'Token invalido, chame @klzinnn para adquirir'})
    
    try:
        c = conn.cursor()
        c.execute("SELECT contatos_id FROM DADOS WHERE cpf = ?", (cpf,))
        contatos_id = c.fetchone()
        if not contatos_id:
            return jsonify({'erro': 'CPF nao encontrado'})
        c.execute("SELECT email FROM EMAIL WHERE contatos_id = ?", (contatos_id[0],))
        resp = c.fetchall()
        
        result_list = []
        for row in resp:
            result_dict = {
                'email': row[0],
                'cpf': cpf
            }
            result_list.append(result_dict)
        
        if not result_list:
            return jsonify({'erro': 'nenhum email com esse cpf encontrado'})
        else:
            return jsonify({'email_cadastrado': result_list})
    
    except sqlite3.Error as e:
        print(e)
        return jsonify({'erro': 'Erro ao consultar o banco de dados'})
    
    finally:
        conn.close()