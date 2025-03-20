import sqlite3
from auth.validacao import validacao
from flask import jsonify
from config import DB_PATH  # Importa o caminho do banco de config.py


def consulta_cpf(cpf, token):
    cpf = cpf.replace('-', '').replace('.', '').replace('%20', '')
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)

    auth = validacao(token)

    if auth != 1:
        return jsonify({'mensagem': 'Token inválido, chame @klzinnn para adquirir'})
    
    c = conn.cursor()
    c.execute("SELECT nome, strftime('%d/%m/%Y', nasc), contatos_id, NOME_MAE, NOME_PAI, CBO, RENDA,RG,ORGAO_EMISSOR,UF_EMISSAO, SEXO FROM DADOS WHERE cpf = ?", (cpf,))
    dados_cpf = c.fetchone()

    try:
        contatos_id = dados_cpf[2]
    except:
        return jsonify({'erro': 'CPF não encontrado'})
    c.execute("""SELECT COALESCE(CSBA, 0) FROM SCORE WHERE CONTATOS_ID = ?""", (contatos_id,))
    scoore = c.fetchone()
    c.execute("""SELECT COALESCE(LOGR_NOME, 'S/N'), COALESCE(BAIRRO, 'S/N'), COALESCE(UF, 'S/N'), COALESCE(CEP, 'S/N'), COALESCE(LOGR_NUMERO, 0) FROM ENDERECOS WHERE CONTATOS_ID = ?""", (contatos_id,))
    enderecos = c.fetchall()
    c.execute("""SELECT DDD, TELEFONE, TIPO_TELEFONE FROM TELEFONE WHERE CONTATOS_ID = ?""", (contatos_id,))
    telzinho = c.fetchall()
    c.execute("""SELECT EMAIL FROM EMAIL WHERE CONTATOS_ID = ?""", (contatos_id,))
    email = c.fetchall()
    
    ###################### TESTE #############################
    c.execute("""SELECT nome_vinculo,cpf_vinculo,vinculo from parentes where cpf_completo = ?""", (cpf,))
    parentes = c.fetchall()
    
    parantes_lista = []
    for pare in parentes:
        cpf_str = str(pare[1])
        if cpf_str is None:
            cpf_str = '00000000000'
        if len(cpf_str) < 11:
            cpf_str = cpf_str.zfill(11)
        parentes_dick = {'nome_parente': pare[0],'cpf_parente': cpf_str,'vinculo': pare[2]}
        parantes_lista.append(parentes_dick)
        
    ###################### TESTE #############################
    try:
        dados_base = {'nome': dados_cpf[0],
                        'nascimento': dados_cpf[1],
                        'mae': dados_cpf[3],
                        'pai': dados_cpf[4],
                        'cbo': dados_cpf[5],
                        'renda': dados_cpf[6],
                        'digito_cpf': cpf[8],
                        'score': str(scoore[0]),
                        'rg': str(dados_cpf[7]),
                        'orgao_emissor': str(dados_cpf[8]),
                        'uf_emissao': str(dados_cpf[9]),
                        'sexo': str(dados_cpf[10])}
    except:
        dados_base = {'nome': dados_cpf[0],
                        'nascimento': dados_cpf[1],
                        'mae': dados_cpf[3],
                        'pai': dados_cpf[4],
                        'cbo': dados_cpf[5],
                        'renda': dados_cpf[6],
                        'digito_cpf': cpf[8],
                        'score': 'indefined',
                        'rg': str(dados_cpf[7]),
                        'orgao_emissor': str(dados_cpf[8]),
                        'uf_emissao': str(dados_cpf[9]),
                        'sexo': str(dados_cpf[10])}
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ endereco lista
    enderecos_list = []
    for endereco in enderecos:
        endereco_dict = {
                        'rua': endereco[0],
                        'bairro': endereco[1],
                        'uf': endereco[2],
                        'cep': endereco[3],
                        'numero': endereco[4]
                    }
        enderecos_list.append(endereco_dict)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ telefone lista
    telefones_list = []
    for telefone in telzinho:
            telefone_dict = {
                        'telefone': str(telefone[0])+' '+str(telefone[1]),
                        'tipo_telefone': str(telefone[2])
                    }
            telefones_list.append(telefone_dict)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EMAIL
    email_list = []
    for emails in email:
        emails_dict = {'emails': emails[0]}
        email_list.append(emails_dict)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    c.close()
    dados_full = {'enderecos': enderecos_list, 'dados': dados_base, 'telefones': telefones_list, 'email': email_list, 'parentes': parantes_lista,}

    return jsonify(dados_full)