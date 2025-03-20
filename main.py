import logging
from flask import Flask
from flask import request
from flask import jsonify

# Imports de endpoints organizados por categorias
# Endpoints gerais
from endpoints.cpf import consulta_cpf
from endpoints.cpf_email import consulta_email_cpf
from endpoints.email import consulta_email
from endpoints.reco_facial import reconhecimento
from endpoints.telefone import telefone_consulta
from endpoints.poder_social import consulta_podersocial
from endpoints.cpf_basico import cpf_dados_basico
from endpoints.politica import dados_urna_eletronixa
from endpoints.renda import cpf_renda
from endpoints.foto_sp import foto_sp_cpf
from endpoints.foto_ce import consultar_ft_ce
from endpoints.foto_ma import foto_ma_cpf
from endpoints.foto_ro import consultar_ft_ro
from endpoints.renach_ro import consultar_renach_ro


from endpoints.foto_pe import consultar_rg
from endpoints.api_endereco import consulta_moradores


# Endpoints específicos Credlink
from endpoints.cpf_credi import consulta_por_cpf_credi
from endpoints.email_credlink import consulta_email_CREDI
from endpoints.pix import pix_search
from endpoints.credlink_telefoni import telefone_cr

# Endpoints médicos
from endpoints.cpf_medico import consultar_medico

# Endpoints auxiliares
from endpoints.conf.dump import dados_base_dump
from endpoints.cpf2 import consulta_cpf_2
from src.cnh import consulta_cpf_cnh
from src.cnh2 import consulta_cpf_cnh_reds

# Endpoints administrativos
from admin.gerar_user import gerar_aceso

# Configuração do Flask
app = Flask(__name__)

# Configuração de logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Definição das funções dos endpoints
def endpoint_cpf(valor, token):
    return consulta_cpf(valor, token)

def endpoint_email(valor, token):
    return consulta_email(valor, token)

def endpoint_email_cpf(valor, token):
    return consulta_email_cpf(valor, token)

def consultar_medico_cpf(valor, token):
    return consultar_medico(valor, token)

def endpoint_telefone(valor, token):
    return telefone_consulta(valor, token)

def endpoint_cnh(valor, token):
    return consulta_cpf_cnh(valor, token)

def endpoint_cnh2(valor, token):
    return consulta_cpf_cnh_reds(valor, token)

def endpoint_poder_social(valor, token):
    return consulta_podersocial(valor, token)

def endpoint_cpf_basico(valor, token):
    return cpf_dados_basico(valor, token)

def endpoint_cpf_renda(valor, token):
    return cpf_renda(valor, token)

def dados_eleicao(valor, token):
    return dados_urna_eletronixa(valor, token)

def getids(valor):
    return dados_base_dump(valor)

def gerartoken(token, dia, mes, ano):
    return gerar_aceso(token, dia, mes, ano)

def consulta_cpf_22(valor, token):
    return consulta_cpf_2(valor, token)

def reco_face(token):
    return reconhecimento(token)

# Funções específicas Credlink
def cpf_new(valor, token):
    return consulta_por_cpf_credi(valor, token)

def email_new(valor, token):
    return consulta_email_CREDI(valor, token)

def pix_detetive(nome, cpf, token):
    return pix_search(nome, cpf, token)

def tel_credilink(valor, token):
    return telefone_cr(valor, token)


def fotodepe(valor, mae, token):
    return consultar_rg(valor, mae, token)

#funcao db sp
def fotodesp(valor, token):
    return foto_sp_cpf(valor, token)

def fotodece(valor, token):
    return consultar_ft_ce(valor, token)

def fotodema(valor, token):
    return foto_ma_cpf(valor, token)

def fotodero(valor, token):
    return consultar_ft_ro(valor, token)

def renachdero(valor, token):
    return consultar_renach_ro(valor, token)


#########   ENDPOINT POST UNICO ###############
# Rota POST para consulta de moradores por endereço
@app.route('/consulta_endereco', methods=['POST'])
def consulta_endereco():
    dados = request.get_json()
    if not dados or 'token' not in dados:
        return jsonify({'erro': 'Token é obrigatório'}), 400

    token = dados.pop('token')  # Remove o token dos dados antes de passar para a função
    resultado = consulta_moradores(dados, token)
    
    return jsonify(resultado)


# Definição das rotas do Flask
app.route('/token/<token>/cpf/<valor>')(endpoint_cpf) 
app.route('/token/<token>/email/<valor>')(endpoint_email) 
app.route('/token/<token>/email_cpf/<valor>')(endpoint_email_cpf)
app.route('/token/<token>/telefone/<valor>')(endpoint_telefone)
app.route('/token/<token>/cnh/<valor>')(endpoint_cnh)
app.route('/token/<token>/cnh_modulo2/<valor>')(endpoint_cnh2)
app.route('/token/<token>/poder_social/<valor>')(endpoint_poder_social)
app.route('/token/<token>/basiccpf/<valor>')(endpoint_cpf_basico)
app.route('/token/<token>/medico_cpf/<valor>')(consultar_medico_cpf)
app.route('/token/<token>/eleicao/<valor>')(dados_eleicao)
app.route('/token/<token>/renda/<valor>')(endpoint_cpf_renda)
app.route('/token/<token>/cpf2/<valor>')(consulta_cpf_22)

# Rotas específicas Credlink
app.route('/token/<token>/email_credi/<valor>')(email_new)
app.route('/token/<token>/tel_cred/<valor>')(tel_credilink)
app.route('/token/<token>/cpf3/<valor>')(cpf_new)
app.route('/token/<token>/pix/nome/<nome>/cpf/<cpf>')(pix_detetive)

# Rotas Db sp
app.route('/token/<token>/foto_sp/<valor>')(fotodesp)
app.route('/token/<token>/foto_ce/<valor>')(fotodece)
app.route('/token/<token>/foto_ma/<valor>')(fotodema)
app.route('/token/<token>/foto_pe/nome/<valor>/<mae>')(fotodepe)
app.route('/token/<token>/foto_ro/<valor>')(fotodero)
app.route('/token/<token>/renach_ro/<valor>')(renachdero)

# Rotas auxiliares
app.route('/getid/<valor>')(getids)
app.route('/reco_facial/<token>')(reco_face)
app.route('/token/<token>/gerar_token/<int:dia>/<int:mes>/<int:ano>')(gerartoken)

# Execução do servidor Flask
if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", threaded=True, debug=True)
