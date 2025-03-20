import sqlite3
from auth.validacao import validacao
from flask import jsonify
from config import DB_PATH  # Importa o caminho do banco de config.py


def consulta_email(email, token):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    # Usando row_factory para acessar as colunas por nome
    conn.row_factory = sqlite3.Row  
    auth = validacao(token)

    if auth != 1:
        return jsonify({'erro': 'Token inválido, chame @klzinnn para adquirir'})

    try:
        c = conn.cursor()
        # Primeiro, busca o contatos_id na tabela EMAIL com base no email informado
        c.execute("SELECT contatos_id FROM EMAIL WHERE email = ?", (email,))
        row = c.fetchone()
        if not row:
            return jsonify({'erro': 'Email não encontrado'})
        contatos_id = row['contatos_id']

        # Em seguida, busca os dados do contato na tabela DADOS usando o contatos_id
        c.execute("""
            SELECT CPF, NOME, SEXO, RENDA, NASC, NOME_MAE, RG, 
                   ORGAO_EMISSOR, UF_EMISSAO, ESTCIV, NACIONALID, 
                   CD_SIT_CAD, DT_SIT_CAD, DT_INFORMACAO, 
                   FAIXA_RENDA_ID, TITULO_ELEITOR, CD_MOSAIC_NOVO
            FROM DADOS 
            WHERE contatos_id = ?
            LIMIT 1;
        """, (contatos_id,))
        dados = c.fetchone()
        if not dados:
            return jsonify({'erro': 'Dados não encontrados para o contato'})

        # Monta a resposta com informações detalhadas
        resposta = {
            'cpf': dados['CPF'],
            'nome': dados['NOME'],
            'sexo': dados['SEXO'],
            'renda': f"R$ {dados['RENDA']}",
            'nascimento': dados['NASC'],
            'nome_mae': dados['NOME_MAE'],
            'rg': dados['RG'],
            'orgao_emissor': dados['ORGAO_EMISSOR'],
            'uf_emissao': dados['UF_EMISSAO'],
            'estado_civil': dados['ESTCIV'],
            'nacionalidade': dados['NACIONALID'],
            'situacao_cadastral': dados['CD_SIT_CAD'],
            'data_situacao_cadastral': dados['DT_SIT_CAD'],
            'data_cadastro': dados['DT_INFORMACAO'],
            'faixa_renda': dados['FAIXA_RENDA_ID'],
            'titulo_eleitor': dados['TITULO_ELEITOR'],
            'codigo_mosaic': dados['CD_MOSAIC_NOVO']
        }

        return jsonify({'dados_contato': resposta})
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro: {str(e)}'})
    finally:
        conn.close()