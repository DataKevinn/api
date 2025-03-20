import sqlite3
from flask import jsonify
from config import DB_CRED  # Caminho do banco de dados
from auth.validacao import validacao

def consulta_endereco(cep, logradouro, numero, bairro, cidade, uf, token):
    try:
        # Validação de entrada
        if any(val is None or val == "" for val in [cep, logradouro, numero, bairro, cidade, uf, token]):
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
        
        # Autenticação do token
        if validacao(token) != 1:
            return jsonify({'mensagem': 'Token inválido'}), 401
        
        # Converte todos os parâmetros para maiúsculas
        cep = cep.upper()
        logradouro = logradouro.upper()
        numero = numero.upper()
        bairro = bairro.upper()
        cidade = cidade.upper()
        uf = uf.upper()

        # Conexão com o banco de dados
        conn = sqlite3.connect(DB_CRED, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Query otimizada com UPPER()
        query = """
            SELECT CPF, LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, ESTADO, UF, CEP
FROM credilink_basic
WHERE (LOGRADOURO = '?' AND BAIRRO = '?' AND CIDADE = '?' AND UF = 'MA' AND CEP = '65615000' AND NUMERO = '0')
        """
        params = [logradouro, bairro, cidade, uf, cep, numero]

        # Debugging opcional (remova em produção)
        print("Query:", query)
        print("Params:", params)

        # Execução da consulta
        c.execute(query, params)
        resultados = c.fetchall()

        # Verificação de resultados
        if not resultados:
            return jsonify({'mensagem': 'Nenhum morador encontrado para este endereço'}), 404

        # Retorno dos dados em formato JSON
        moradores = [dict(row) for row in resultados]
        return jsonify({'moradores': moradores}), 200

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro: {str(e)}'}), 500
    
    finally:
        if 'conn' in locals():
            conn.close()
