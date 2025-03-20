import sqlite3
from auth.validacao import validacao
from flask import jsonify
from    config import DB_PATH  # Importa o caminho do banco de config.py


def cpf_dados_basico(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    with sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10) as conn:
        if not validacao(token):
            return jsonify({'erro': 'Token invalido, chame @klzinnn para adquirir'})
#=======================================================================================================
        try:
            c = conn.cursor()
            c.execute("SELECT cpf, nome, sexo, strftime('%d/%m/%Y', nasc), rg FROM DADOS WHERE cpf = ?", (cpf,))
            row = c.fetchone()
            if not row:
                return jsonify({'erro': 'CPF nao encontrado'})
            
            dados_base = {'nome': row[1], 'sexo': row[2], 'nasc': row[3], 'rg': row[4]}  # Use integer indices to access row elements
            return dados_base
        except sqlite3.Error as e:
            return jsonify({'erro': 'Erro ao consultar o banco de dados'})