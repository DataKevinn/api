# API Documentation 📝

This API provides various routes for processing and handling different data types, including CPF, email, telephone, CNH, and other specific data points. The API is designed for educational purposes 🎓, and the database used in this project is entirely fake and for learning purposes only 🚫.

## Routes Overview 🌐

### General Routes 🔄

- **`/token/<token>/cpf/<valor>`**  
  Retrieves CPF-related data based on the provided token and value.  
  **Handler**: `endpoint_cpf` 📑

- **`/token/<token>/email/<valor>`**  
  Retrieves email-related data based on the provided token and value.  
  **Handler**: `endpoint_email` 📧

- **`/token/<token>/email_cpf/<valor>`**  
  Retrieves both email and CPF-related data.  
  **Handler**: `endpoint_email_cpf` 📧📑

- **`/token/<token>/telefone/<valor>`**  
  Retrieves telephone-related data based on the provided token and value.  
  **Handler**: `endpoint_telefone` 📞

- **`/token/<token>/cnh/<valor>`**  
  Retrieves CNH (National Driver's License) information based on the provided token and value.  
  **Handler**: `endpoint_cnh` 🚗

- **`/token/<token>/cnh_modulo2/<valor>`**  
  Retrieves CNH (Module 2) data based on the provided token and value.  
  **Handler**: `endpoint_cnh2` 🚙

- **`/token/<token>/poder_social/<valor>`**  
  Retrieves Social Power data based on the provided token and value.  
  **Handler**: `endpoint_poder_social` 💪

- **`/token/<token>/basiccpf/<valor>`**  
  Retrieves basic CPF-related data.  
  **Handler**: `endpoint_cpf_basico` 📑

- **`/token/<token>/medico_cpf/<valor>`**  
  Retrieves medical information associated with CPF.  
  **Handler**: `consultar_medico_cpf` 🏥

- **`/token/<token>/eleicao/<valor>`**  
  Retrieves election-related data.  
  **Handler**: `dados_eleicao` 🗳️

- **`/token/<token>/renda/<valor>`**  
  Retrieves income-related data based on CPF.  
  **Handler**: `endpoint_cpf_renda` 💵

- **`/token/<token>/cpf2/<valor>`**  
  Retrieves additional CPF-related information.  
  **Handler**: `consulta_cpf_22` 📑

### Specific Routes for Credlink 💳

- **`/token/<token>/email_credi/<valor>`**  
  Retrieves data related to the Credlink email.  
  **Handler**: `email_new` 📧

- **`/token/<token>/tel_cred/<valor>`**  
  Retrieves data related to the Credlink telephone.  
  **Handler**: `tel_credilink` 📞

- **`/token/<token>/cpf3/<valor>`**  
  Retrieves additional CPF-related data from Credlink.  
  **Handler**: `cpf_new` 📑

- **`/token/<token>/pix/nome/<nome>/cpf/<cpf>`**  
  Retrieves Pix data associated with a given name and CPF.  
  **Handler**: `pix_detetive` 💸

### DB SP Routes 🗃️

- **`/token/<token>/foto_sp/<valor>`**  
  Retrieves a photo related to SP data.  
  **Handler**: `fotodesp` 📸

- **`/token/<token>/foto_ce/<valor>`**  
  Retrieves a photo related to CE data.  
  **Handler**: `fotodece` 📸

- **`/token/<token>/foto_ma/<valor>`**  
  Retrieves a photo related to MA data.  
  **Handler**: `fotodema` 📸

- **`/token/<token>/foto_pe/nome/<valor>/<mae>`**  
  Retrieves a photo related to PE data and includes the name and mother's name.  
  **Handler**: `fotodepe` 📸

- **`/token/<token>/foto_ro/<valor>`**  
  Retrieves a photo related to RO data.  
  **Handler**: `fotodero` 📸

- **`/token/<token>/renach_ro/<valor>`**  
  Retrieves RENACH (National Driver’s License Registry) data related to RO.  
  **Handler**: `renachdero` 🚗

### Auxiliary Routes 🔧

- **`/getid/<valor>`**  
  Retrieves an ID based on the provided value.  
  **Handler**: `getids` 🆔

- **`/reco_facial/<token>`**  
  Performs facial recognition based on the provided token.  
  **Handler**: `reco_face` 🤳

- **`/token/<token>/gerar_token/<int:dia>/<int:mes>/<int:ano>`**  
  Generates a new token with a specified day, month, and year.  
  **Handler**: `gerartoken` 🔑

## Important Notes ⚠️

- **Educational Purpose**: The data used in this API is for learning and educational purposes only 🎓. The database is fake, and no real-world sensitive information is involved 🚫.
- **Authentication**: The routes require a valid `token` to access the endpoints 🔑, ensuring the safety of data retrieval 🔒.

## Getting Started 🚀

1. **Install Dependencies**:  
   Ensure you have Flask installed. You can install it using:
   ```bash
   pip install flask
