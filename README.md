# 📝 Documentação da API - Guia para Iniciantes 🚀

Bem-vindo! Esta documentação interativa vai te ajudar a usar a nossa API de forma fácil e rápida! 😎🔄

## ✨ Como funciona?
Nossa API permite acessar diversas informações usando requisições HTTP GET.

### 🔑 Autenticação
Todas as requisições precisam de um **token**. Ele deve ser passado na URL conforme os exemplos abaixo.

## 🛠️ Endpoints Disponíveis

### 👨‍👩‍👦 Consulta por CPF
**Rota:**
```
GET /token/{token}/cpf/{valor}
```
**Uso:** Recupera informações associadas a um CPF.

### 📧 Consulta por Email
**Rota:**
```
GET /token/{token}/email/{valor}
```
**Uso:** Busca dados relacionados a um email.

### 📞 Consulta por Telefone
**Rota:**
```
GET /token/{token}/telefone/{valor}
```
**Uso:** Recupera informações de um telefone.

### 🔖 Consulta por CNH
**Rota:**
```
GET /token/{token}/cnh/{valor}
```
**Uso:** Obtém dados de uma CNH.

### 📈 Consulta de Poder Social
**Rota:**
```
GET /token/{token}/poder_social/{valor}
```
**Uso:** Verifica informações de poder social.

### 👨‍⚕️ Consulta Médico por CPF
**Rota:**
```
GET /token/{token}/medico_cpf/{valor}
```
**Uso:** Busca dados médicos pelo CPF.

### 🗳️ Consulta Eleitoral
**Rota:**
```
GET /token/{token}/eleicao/{valor}
```
**Uso:** Exibe informações sobre registros eleitorais.

### 💰 Consulta de Renda
**Rota:**
```
GET /token/{token}/renda/{valor}
```
**Uso:** Mostra estimativas de renda associadas ao CPF.

## 💻 Rotas Específicas Credlink

### 📧 Consulta de Email Credi
**Rota:**
```
GET /token/{token}/email_credi/{valor}
```
**Uso:** Verifica informações de email vinculadas ao Credlink.

### 👨‍�‍� Consulta CPF 3
**Rota:**
```
GET /token/{token}/cpf3/{valor}
```
**Uso:** Outra forma de buscar informações por CPF.

### 🌐 Consulta Pix Detetive
**Rota:**
```
GET /token/{token}/pix/nome/{nome}/cpf/{cpf}
```
**Uso:** Obtém informações de um Pix vinculado ao CPF e nome.

## 🏘️ Banco de Dados SP

### 🎬 Foto SP
**Rota:**
```
GET /token/{token}/foto_sp/{valor}
```
**Uso:** Busca imagens relacionadas a um CPF no banco de dados de SP.

### 📺 Foto CE
**Rota:**
```
GET /token/{token}/foto_ce/{valor}
```
**Uso:** Busca imagens no banco de dados do CE.

### 📸 Foto MA
**Rota:**
```
GET /token/{token}/foto_ma/{valor}
```
**Uso:** Busca imagens no banco de dados do MA.

## 🛠️ Outras Rotas Auxiliares

### 👤 Obter ID
**Rota:**
```
GET /getid/{valor}
```
**Uso:** Retorna o ID correspondente ao valor informado.

### 🧑‍🎭 Reconhecimento Facial
**Rota:**
```
GET /reco_facial/{token}
```
**Uso:** Executa reconhecimento facial com base no token fornecido.

### 🔑 Gerar Token
**Rota:**
```
GET /token/{token}/gerar_token/{dia}/{mes}/{ano}
```
**Uso:** Gera um novo token com base na data informada.

---

### 💡 Dicas Finais
✅ Substitua `{token}` pelo seu token de acesso.
✅ Substitua `{valor}` pelo dado que deseja consultar.
✅ Use **https://** para fazer as requisições corretamente.

**Agora é só testar e aproveitar a API!** 🚀🛠️

