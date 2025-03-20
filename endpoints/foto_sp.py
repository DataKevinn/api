import sqlite3
from auth.validacao import validacao
from flask import jsonify

from config import DB_PATH  # Importa o caminho do banco de config.py


def foto_sp_cpf(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    if not validacao(token):
        return jsonify({'erro': 'Token inválido, chame @klzinnn para adquirir'})
    
    try:
        with sqlite3.connect('D:/central_fotosp.db', check_same_thread=False, timeout=10) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            query = '''
                SELECT * FROM FOTOSP WHERE cpf = ?
            '''
            c.execute(query, (cpf,))
            rows = c.fetchall()
            if not rows:
                return jsonify({'erro': 'Dados não encontrados'})
            
            # Separando os dados em dois JSONs
            fotos = []
            for row in rows:
                fotos.append({
                    'cpf': row['cpf'],
                    'origem': row['ORIGEM'],
                    'fotob64': row['FOTOB64']
                })
            
            return jsonify(fotos)
    
    except sqlite3.Error as e:
        return jsonify({'erro': 'Erro ao consultar o banco de dados'})
