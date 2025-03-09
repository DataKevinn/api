# Documentação das Endpoints

Este repositório contém a documentação das endpoints do sistema Flask. As rotas estão organizadas em categorias para facilitar a consulta.

---

## Rotas Gerais
- **`/token/<token>/cpf/<valor>`**  
  _Desativada._

- **`/token/<token>/email/<valor>`**  
  _Desativada._

- **`/token/<token>/email_cpf/<valor>`**  
  Processa informações combinadas de email e CPF.

- **`/token/<token>/telefone/<valor>`**  
  Consulta ou manipula informações relacionadas a um número de telefone.

- **`/token/<token>/cnh/<valor>`**  
  Processa dados relacionados a CNHs (Carteiras Nacionais de Habilitação).

- **`/token/<token>/cnh_modulo2/<valor>`**  
  Função específica para manipulação do módulo 2 de CNHs.

- **`/token/<token>/poder_social/<valor>`**  
  Endpoint para dados de influência ou poder social.

- **`/token/<token>/basiccpf/<valor>`**  
  Processamento básico com CPF.

- **`/token/<token>/medico_cpf/<valor>`**  
  Consulta dados médicos associados a um CPF.

- **`/token/<token>/eleicao/<valor>`**  
  Obtém informações relacionadas a dados de eleição.

- **`/token/<token>/renda/<valor>`**  
  Consultas ou estimativas de renda com base no CPF.

- **`/token/<token>/cpf2/<valor>`**  
  Consulta complementar ou adicional para CPF.

---

## Rotas Específicas Credlink
- **`/token/<token>/email_credi/<valor>`**  
  Processa informações específicas de emails do Credlink.

- **`/token/<token>/tel_cred/<valor>`**  
  Dados telefônicos específicos do Credlink.

- **`/token/<token>/cpf3/<valor>`**  
  Terceiro nível de processamento de CPF.

- **`/token/<token>/pix/nome/<nome>/cpf/<cpf>`**  
  Consultas relacionadas ao Pix combinando nome e CPF.

---

## Rotas Db SP
- **`/token/<token>/foto_sp/<valor>`**  
  Dados de fotos para o banco de SP.

- **`/token/<token>/foto_ce/<valor>`**  
  Processamento de fotos para o banco do CE.

- **`/token/<token>/foto_ma/<valor>`**  
  Dados de fotos para o banco do MA.

---

## Rotas Auxiliares
- **`/getid/<valor>`**  
  Obtém IDs com base no valor fornecido.

- **`/reco_facial/<token>`**  
  Realiza reconhecimento facial com o token.

- **`/token/<token>/gerar_token/<int:dia>/<int:mes>/<int:ano>`**  
  Gera um novo token baseado em uma data específica.

---

### **Como Usar**
Para cada endpoint, substitua os parâmetros `<token>`, `<valor>`, `<nome>`, `<cpf>`, `<dia>`, `<mes>` e `<ano>` pelos valores apropriados ao seu caso de uso.

---

Fique à vontade para adaptar ou adicionar mais informações! 🚀
