import sqlite3
from auth.validacao import validacao
from flask import jsonify
from config import DB_RO

def consultar_ft_ro(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    if not validacao(token):
        return jsonify({'erro': 'Token inválido, chame @klzinnn para adquirir'})
    
    try:
        with sqlite3.connect(DB_RO, check_same_thread=False, timeout=10) as conexao:
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            consulta = '''
                SELECT CPF, NOME, RENACH, NUMERO_REGISTRO, DATA_VALIDADE,
                       CATEGORIA, PONTOS, LOGRADOURO, BAIRRO, NUMERO_CASA, TELEFONE, FOTO
                  FROM FOTO_RO
                 WHERE CPF = ?
            '''
            cursor.execute(consulta, (cpf,))
            registros = cursor.fetchall()
            if not registros:
                return jsonify({'erro': 'Dados não encontrados'})
            
            fotos = []
            for registro in registros:
                fotos.append({
                    'CPF': registro['CPF'],
                    'NOME': registro['NOME'],
                    'RENACH': registro['RENACH'],
                    'NUMERO_REGISTRO': registro['NUMERO_REGISTRO'],
                    'DATA_VALIDADE': registro['DATA_VALIDADE'],
                    'CATEGORIA': registro['CATEGORIA'],
                    'PONTOS': registro['PONTOS'],
                    'LOGRADOURO': registro['LOGRADOURO'],
                    'BAIRRO': registro['BAIRRO'],
                    'NUMERO_CASA': registro['NUMERO_CASA'],
                    'TELEFONE': registro['TELEFONE'],
                    'FOTO': registro['FOTO']
                })
            
            return jsonify(fotos)
    
    except sqlite3.Error:
        return jsonify({'erro': 'Erro ao consultar o banco de dados'})