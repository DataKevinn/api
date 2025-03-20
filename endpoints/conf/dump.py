import sqlite3
from auth.validacao import validacao
from flask import jsonify

def dados_base_dump(cpf):
    cpf = cpf.replace('-', '').replace('.', '')
    with sqlite3.connect('../../../SERASA.db', check_same_thread=False, timeout=10) as conn:
        try:
            c = conn.cursor()
            c.execute("SELECT cpf, nome, sexo, strftime('%d/%m/%Y', nasc), contatos_id FROM DADOS WHERE cpf = ?", (cpf,))
            row = c.fetchone()
            if not row:
                return jsonify({'erro': 'CPF nao encontrado'})
            
            dados_base = {'nome': row[1], 'sexo': row[2], 'nasc': row[3], 'ctts_id': row[4]}
            return dados_base
        except sqlite3.Error as e:
            return jsonify({'erro': 'Erro ao consultar o banco de dados'})