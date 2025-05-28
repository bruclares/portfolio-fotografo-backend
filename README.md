# Portfólio Fotógrafo – Backend

> Sistema backend para gerenciamento de contatos, formas de contato e autenticação de fotógrafo. Desenvolvido com Flask, Python, PostgreSQL e Cloudinary.

Este é o backend de um sistema simples para um portfólio de fotógrafo. Ele permite:

- Login seguro com JWT
- Recuperação de senha via e-mail
- Upload de imagens no Cloudinary
- Gerenciamento de contatos recebidos pelo site
- Configuração de formas de contato públicas

---

## Funcionalidades

- Autenticação com JWT (login, logout, recuperação de senha)
- Envio de e-mails com Flask-Mail
- Upload e listagem de imagens via Cloudinary
- Configuração única de usuário-administrador
- Registro de mensagens de contato
- Armazenamento seguro no PostgreSQL
- Logs de acesso e erros
- Token de recuperação com expiração e denylist

---

## Requisitos

Antes de rodar a aplicação, certifique-se de ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)
- [Pipenv ou virtualenv](https://pipenv.pypa.io/) (opcional, mas recomendado)

---

## Tecnologias Utilizadas

- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Autenticação**: Flask-JWT-Extended
- **E-mail**: Flask-Mail
- **Banco de Dados**: PostgreSQL / Neon
- **Armazenamento de Imagens**: [Cloudinary](https://cloudinary.com)
- **Logs e Auditoria**: Banco de dados + service de logs
- **Segurança**: Bcrypt (hash de senhas), tokens únicos e revogáveis

---

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/portfolio-fotografo-backend.git
   cd portfolio-fotografo-backend

   ```

2. **(Opcional) Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows

   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt

   ```

4. **Configure as variáveis de ambiente:**

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

# Flask

FLASK_SECRET_KEY=chave-secreta-flask
FLASK_DEBUG=True

# JWT

JWT_SECRET_KEY=chave-jwt-secreta

# Banco de Dados

DATABASE_URL=postgres://seu_usuario:senha@localhost:5432/portifolio_fotografo

# E-mail

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=seuemail@gmail.com
MAIL_PASSWORD=sua_senha_de_app_ou_token
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=seuemail@gmail.com
MAIL_SALT=recover-key

# Cloudinary

CLOUD_NAME=sua-cloud-name
API_KEY=sua-api-key
API_SECRET=sua-api-secret

# Ambiente

ENVIRONMENT=development

---

5. **Rode o script de migração no banco de dados:**

   ```bash
   psql -U seu_usuario -d seu_banco -f migration.sql

   ```

6. **Inicie o servidor localmente:**
   ```bash
   python app.py
   ```

Acesse a API em http://localhost:5000

---

## Como Executar

1. **Ative o ambiente virtual:**
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate # Windows

2. **Execute a aplicação:**
   python app.py

3. **Acesse a API:**
   http://localhost:5000

---

## Segurança

- Tokens JWT com JTI único e denylist (tokens_denylist)
- Senhas armazenadas com bcrypt
- Tokens de recuperação com expiração (1 hora)
- E-mails enviados com template HTML seguro
- Todos os endpoints protegidos exigem token válido

---

## Banco de Dados

O projeto usa PostgreSQL com as seguintes tabelas:

- fotografo: Usuário administrador (único)
- tokens_recuperacao: Tokens para redefinir senha
- tokens_denylist: Tokens JWT inválidos
- contatos: Mensagens recebidas via formulário
- formas_contato: Meios de contato públicos
- logs: Registros de acesso e erros

---

## Deploy

Você pode fazer deploy no Vercel , Render , Heroku ou qualquer serviço compatível com Python + Flask + PostgreSQL.

## Estrutura do Projeto

```
portfolio-fotografo-backend
├─ app.py
├─ config.py
├─ controllers
│  ├─ auth.py
│  ├─ cloudinaryapi.py
│  ├─ contatos.py
│  └─ formas_contato.py
├─ database
│  ├─ database.py
│  └─ migration.sql
├─ README.md
├─ requirements.txt
├─ services
│  ├─ auth_service.py
│  ├─ email_service.py
│  └─ logs.py
├─ utils
│  └─ token.py
└─ vercel.json

```
