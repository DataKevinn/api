import sqlite3
import logging
from auth.validacao import validacao
from config import DB_PATH  # Caminho do banco de dados

# Configuração do Logging com FileHandler e StreamHandler (terminal)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formatação das mensagens de log
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para gravar em arquivo (apenas erros serão registrados no arquivo)
file_handler = logging.FileHandler("error.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler para imprimir no terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Função para buscar moradores de um endereço
def consulta_moradores(dados, token):
    # Cria um dicionário de parâmetros com valores padrão para evitar binding issues
    params = {
        'logr_nome': dados.get('logr_nome', ''),
        'logr_numero': dados.get('logr_numero', ''),
        'bairro': dados.get('bairro', ''),
        'cidade': dados.get('cidade', ''),
        'uf': dados.get('uf', ''),
        'cep': dados.get('cep', '')
    }
    
    with sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10) as conn:
        if not validacao(token):
            msg = "Token inválido usado na requisição."
            logger.error(msg)
            print(msg)
            return {'erro': 'Token inválido, chame @klzinnn para adquirir'}

        try:
            c = conn.cursor()
            query = """
                SELECT DADOS.CPF, DADOS.NOME, DADOS.SEXO, DADOS.NOME_MAE, DADOS.NOME_PAI, DADOS.RG,
                       ENDERECOS.LOGR_TIPO, ENDERECOS.LOGR_NOME, ENDERECOS.LOGR_NUMERO, 
                       ENDERECOS.BAIRRO, ENDERECOS.CIDADE, ENDERECOS.UF, ENDERECOS.CEP
                FROM ENDERECOS
                INNER JOIN DADOS ON ENDERECOS.CONTATOS_ID = DADOS.CONTATOS_ID
                WHERE 
                    (COALESCE(:logr_nome, '') = '' OR ENDERECOS.LOGR_NOME LIKE '' || :logr_nome || '')
                    AND (COALESCE(:logr_numero, '') = '' OR ENDERECOS.LOGR_NUMERO = :logr_numero)
                    AND (COALESCE(:bairro, '') = '' OR ENDERECOS.BAIRRO = :bairro)
                    AND (COALESCE(:cidade, '') = '' OR ENDERECOS.CIDADE = :cidade)
                    AND (COALESCE(:uf, '') = '' OR ENDERECOS.UF = :uf)
                    AND (COALESCE(:cep, '') = '' OR ENDERECOS.CEP = :cep)
            """
            c.execute(query, params)
            rows = c.fetchall()

            if not rows:
                msg = f"Endereço não encontrado: {params}"
                logger.warning(msg)
                print(msg)
                return {'erro': 'Endereço não encontrado'}

            moradores = []
            for row in rows:
                moradores.append({
                    'cpf': row[0],
                    'nome': row[1],
                    'sexo': row[2],
                    'nome_mae': row[3],
                    'nome_pai': row[4],
                    'rg': row[5],
                    'logradouro_tipo': row[6],
                    'logradouro_nome': row[7],
                    'logradouro_numero': row[8],
                    'bairro': row[9],
                    'cidade': row[10],
                    'uf': row[11],
                    'cep': row[12]
                })

            msg = f"Consulta realizada com sucesso: {params}"
            logger.info(msg)
            print(msg)
            return {'moradores': moradores}

        except sqlite3.Error as e:
            msg = f"Erro no banco de dados: {e}"
            logger.error(msg)
            print(msg)
            return {'erro': f'Erro ao consultar o banco de dados: {str(e)}'}
