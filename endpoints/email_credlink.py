import sqlite3
from auth.validacao import validacao
from flask import jsonify
import random
from config import DB_PATH  # Importa o caminho do banco de config.py



conn = sqlite3.connect('credilink.db', check_same_thread=False, timeout=10)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

def consulta_email_CREDI(email, token):
    try:
        auth = validacao(token)
        if auth != 1:
            return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})

        c = conn.cursor()
        c.execute("""
            SELECT 
                CPF, 
                NOME, 
                SEXO, 
                CBO, 
                QT_VEICULOS, 
                FAIXA_RENDA 
            FROM 
                credilink_basic 
            WHERE 
                EMAIL = ?
        """, (email,))
        result = c.fetchone()
        if not result:
            return jsonify({'erro': 'Nenhum dado encontrado para o CPF fornecido'})

        dados = {key: result[key] for key in result.keys()}
        return jsonify(dados)
    
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao processar a requisição: {str(e)}'})