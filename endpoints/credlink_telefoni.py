import sqlite3
from auth.validacao import validacao
from flask import jsonify
import random
from config import DB_PATH  # Importa o caminho do banco de config.py


conn = sqlite3.connect('credilink.db', check_same_thread=False, timeout=10)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

def telefone_cr(telefone, token):
    telefone = telefone.replace('-', '').replace('.', '').replace('%20', '')
    try:
        numero_aleatorio = random.randint(0, 99)

        auth = validacao(token)
        if auth != 1:
            return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})

        c = conn.cursor()
        c.execute("""
            SELECT 
                dp.CPF,
                dp.NOME,
                dp.SEXO,
                dp.RENDA_PRESUMIDA,
                dp.DT_NASCIMENTO,
                dp.NOME_MAE
            FROM 
                credilink_basic dp
            JOIN 
                telefone t 
            ON 
                dp.CPF = t.CPF
            WHERE 
                t.TELEFONES = ?
        """, (telefone,))
        result = c.fetchone()
        if not result:
            return jsonify({'erro': 'Dados não encontrados para o telefone fornecido'})

        dados_base = {
            'nome': result['NOME'],
            'cpf': result['CPF'],
            'sexo': result['SEXO'],
            'renda': 'R$ '+result['RENDA_PRESUMIDA']+ f'.{numero_aleatorio}',
            'nascimento': result['DT_NASCIMENTO'],
            'mae': result['NOME_MAE']
        }

        return jsonify(dados_base)
    
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao processar a requisição: {str(e)}'})
