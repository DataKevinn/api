import sqlite3
from auth.validacao import validacao
from flask import jsonify
import random

from config import DB_PATH  # Importa o caminho do banco de config.py


conn = sqlite3.connect('credilink.db', check_same_thread=False, timeout=10)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

def consulta_por_cpf_credi(cpf, token):
    try:
        auth = validacao(token)
        if auth != 1:
            return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})

        c = conn.cursor()
        c.execute("""
            SELECT 
                CPF, 
                NOME, 
                TIPO_ENDERECO, 
                LOGRADOURO, 
                NUMERO, 
                COMPLEMENTO, 
                BAIRRO, 
                CIDADE, 
                ESTADO, 
                UF, 
                CEP, 
                DT_NASCIMENTO, 
                NOME_MAE, 
                SEXO, 
                EMAIL, 
                FLAG_OBITO, 
                DT_OBITO, 
                STATUS_RECEITA_FEDERAL, 
                PCT_CARGO_SOCIETARIO, 
                CBO, 
                QT_VEICULOS, 
                MARCA_VEICULO1, 
                MODELO_VEICULO1, 
                ANO_VEICULO1, 
                MARCA_VEICULO2, 
                MODELO_VEICULO2, 
                ANO_VEICULO2, 
                MARCA_VEICULO3, 
                MODELO_VEICULO3, 
                ANO_VEICULO3, 
                MARCA_VEICULO4, 
                MODELO_VEICULO4, 
                ANO_VEICULO4, 
                MARCA_VEICULO5, 
                MODELO_VEICULO5, 
                ANO_VEICULO5, 
                RENDA_PRESUMIDA, 
                FAIXA_RENDA 
            FROM 
                credilink_basic 
            WHERE 
                CPF = ?
        """, (cpf,))
        result = c.fetchone()
        if not result:
            return jsonify({'erro': 'Nenhum dado encontrado para o CPF fornecido'})

        dados = {key: result[key] for key in result.keys()}
        return jsonify(dados)
    
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao processar a requisição: {str(e)}'})