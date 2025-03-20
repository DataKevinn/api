import sqlite3
from auth.validacao import validacao
from flask import jsonify
from config import DB_CEARA  # Importa o caminho do banco de config.py



def consultar_ft_ce(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '')
    if not validacao(token):
        return jsonify({'erro': 'Token inválido, chame @klzinnn para adquirir'})
    
    try:
        with sqlite3.connect(DB_CEARA, check_same_thread=False, timeout=10) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            query = '''
                SELECT * FROM pessoas WHERE CPF = ?
            '''
            c.execute(query, (cpf,))
            rows = c.fetchall()
            if not rows:
                return jsonify({'erro': 'Dados não encontrados'})
            
            # Separando os dados em dois JSONs
            fotos = []
            for row in rows:
                fotos.append({
                    'id': row['id'],
                    'numero_pedido': row['orderNumber'],
                    'nome': row['name'],
                    'mae': row['mother'],
                    'pai': row['father'],
                    'data_nascimento': row['birthDate'],
                    'cidade_estado_pais_nascimento': row['birthCityStateCountry'],
                    'nacionalidade': row['nationality'],
                    'estado_civil': row['maritalStatus'],
                    'sexo': row['sex'],
                    'grau_educacao': row['educationDegree'],
                    'ocupacao': row['occupation'],
                    'tipo_pedido': row['orderType'],
                    'estacao': row['station'],
                    'rg': row['rg'],
                    'data_identidade': row['identityDate'],
                    'cpf': row['cpf'],
                    'altura': row['height'],
                    'cor_pele': row['skinColor'],
                    'cor_olhos': row['eyeColor'],
                    'tipo_olhos': row['eyeType'],
                    'tipo_cabelo': row['hairType'],
                    'cor_cabelo': row['hairColor'],
                    'foto': row['picture']
                })
            
            return jsonify(fotos)
    
    except sqlite3.Error as e:
        return jsonify({'erro': 'Erro ao consultar o banco de dados'})
