## Portfólio para Fotógrafos com Integração de Conteúdo

### Descrição do Projeto

O **Portfólio para Fotógrafos** é uma aplicação web Full Stack desenvolvida para fotógrafos exibirem seus portfólios de forma profissional e interativa. Este repositório contém o código do **back-end**, responsável por gerenciar a lógica de negócios, integrar o armazenamento de imagens via Cloudinary e processar contatos de clientes. A API foi desenvolvida com **Flask** e utiliza **PostgreSQL** para persistência de dados.

O back-end suporta o front-end ao permitir o recebimento de mensagens de contato, a recuperação de fotos do Cloudinary e o registro de logs para auditoria.

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**
- **Flask-JWT-Extended**
- **Flask-Mail**
- **PostgreSQL**
- **Cloudinary**
- **dotenv**
- **psycopg (PostgreSQL Driver)**

### Frontend

- HTML5 + CSS3
- JavaScript Puro (Vanilla JS)
- Consumo de API REST
- Deploy na Vercel

### Backend

- Python 3.12 com Flask
- Blueprints, Controllers, Services e Utils
- Flask-JWT-Extended (autenticação JWT)
- Flask-Mail (recuperação de senha)
- **psycopg 3** (conexão direta com PostgreSQL)
- Integração com Cloudinary para upload de imagens
- Banco de Dados: PostgreSQL (Neon)
- Deploy na Vercel

---

## Funcionalidades

- Autenticação com e-mail e senha (JWT)
- Cadastro inicial do fotógrafo (usuário único)
- Recuperação de senha por e-mail com token temporário
- Envio de mensagens de contato
- CRUD de formas de contato (WhatsApp, Instagram, etc.)
- Upload de imagens via Cloudinary
- Log de requisições para auditoria

---

## Estrutura de Pastas

```bash
.
├── app.py                  # Ponto de entrada da aplicação
├── config.py               # Configurações por ambiente
├── controllers/            # Blueprints organizados por funcionalidade
│   ├── auth.py
│   ├── contatos.py
│   ├── formas_contato.py
│   └── cloudinaryapi.py
├── services/               # Regras de negócio (auth, email, log)
│   ├── auth_service.py
│   ├── email_service.py
│   └── log_service.py
├── database/
│   └── database.py         # Conexão com PostgreSQL
├── .env                    # Variáveis de ambiente (não subir!)
├── README.md               # Documentação do projeto
└── requirements.txt        # Lista de dependências
```

---

## Como Rodar Localmente

### 1. Clone o repositório:

```
git clone https://github.com/seu-usuario/portfolio-fotografo-backend.git
cd portfolio-fotografo-backend
```

### 2. Crie e ative o ambiente virtual:

```
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências:

```
pip install -r requirements.txt
```

---

## Variáveis de Ambiente (.env)

```
FLASK_SECRET_KEY=sua-chave-flask
JWT_SECRET_KEY=sua-chave-jwt

DATABASE_URL=postgresql://usuario:senha@localhost:5432/portifolio_fotografo

MAIL_SERVER=smtp.seudominio.com
MAIL_PORT=587
MAIL_USERNAME=seuemail@exemplo.com
MAIL_PASSWORD=suasenha
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER=seuemail@exemplo.com
MAIL_SALT=sua-salt-para-token

CLOUD_NAME=nome-do-cloudinary
API_KEY=sua-api-key
API_SECRET=sua-api-secret
ENVIRONMENT=development
```

## Testes Manuais

Você pode testar os endpoints com ferramentas como Postman ou Insomnia.

### Autenticação

POST /api/auth/cadastro → Cria fotógrafo

POST /api/auth/login → Login com JWT

POST /api/auth/recuperar-senha → Envia e-mail com token

POST /api/auth/resetar-senha → Reseta senha com token

### Contato

POST /api/contatos → Envia mensagem de contato

GET /api/formas-contato → Lista formas de contato

POST /api/formas-contato → Cria nova forma de contato

PUT /api/formas-contato/:id → Edita

---

## Banco de Dados

O banco usa PostgreSQL com as seguintes tabelas:

- fotografo

- formas_contato

- contatos

- tokens_recuperacao

- logs

A versão inicial das tabelas está disponível em scripts SQL (migration).

---

## Boas Práticas

- Organização por camadas: controllers, services, database

- Uso de Blueprints para modularização

- Tokens JWT com tempo de expiração

- Recuperação de senha segura com token único

- Integração com Cloudinary para uploads de imagem

- Armazenamento de logs para auditoria

- Separação de configurações por ambiente

---

## Links

- **GitHub Project**: [Link do Projeto](https://github.com/users/bruclares/projects/3)
- **Repositório Front-end**: [portfolio-fotografo-frontend](https://github.com/bruclares/portfolio-fotografo-frontend)
- **Repositório Back-end**: [portfolio-fotografo-backend](https://github.com/bruclares/portfolio-fotografo-backend)
- **Hospedagem na Vercel**: [Portfólio Fotógrafo](https://portfolio-fotografo.vercel.app/)

---
