## Portfólio para Fotógrafos com Integração de Conteúdo

### Descrição do Projeto

O **Portfólio para Fotógrafos** é uma aplicação web Full Stack desenvolvida para fotógrafos exibirem seus portfólios de forma profissional e interativa. Este repositório contém o código do **back-end**, responsável por gerenciar a lógica de negócios, integrar o armazenamento de imagens via Cloudinary e processar contatos de clientes. A API foi desenvolvida com **Flask** e utiliza **PostgreSQL** para persistência de dados, oferecendo uma solução escalável para fotógrafos como Aurora Espinosa.

O back-end suporta o front-end ao permitir o recebimento de mensagens de contato, a recuperação de fotos do Cloudinary e o registro de logs para auditoria.

**Status do Projeto**: Este projeto está em desenvolvimento ativo. Algumas funcionalidades, como os endpoints de contatos e integração com Cloudinary, estão implementadas, mas outras (como autenticação) estão pendentes. Estamos trabalhando para finalizar as próximas etapas antes do lançamento final.

---

## Funcionalidades

### Back-end

- **API**: Gerencia requisições do front-end:
  - Recebimento e armazenamento de mensagens de contato.
  - Recuperação de fotos do Cloudinary com paginação.
  - Verificação de status da API.
- **Banco de Dados**: Armazena mensagens de contato e logs em PostgreSQL.
- **Integração com Cloudinary**: Recupera imagens dinamicamente para exibição no front-end.
- **Segurança e Logs**: Registra todas as requisições para monitoramento e protege credenciais via variáveis de ambiente.

### Front-end (Relacionado)

- **Interface**: Exibe fotos e envia contatos, consumindo a API do back-end.

### Banco de Dados (Relacionado)

- **Estrutura**: Tabelas `contatos` e `logs` para dados persistentes.

---

## Tecnologias Utilizadas

- **Back-end**: Python (Flask)
- **Banco de Dados**: PostgreSQL
- **Armazenamento de Imagens**: Cloudinary
- **Ferramentas**: Psycopg (driver PostgreSQL), Flask-CORS, Dotenv
- **Hospedagem**: Vercel
- **Controle de Versão**: Git, GitHub

---

## Status de Desenvolvimento

- **Etapas Concluídas**:

  - Configuração da API Flask com Blueprints (AC1).
  - Endpoint para gerenciamento de contatos (`POST /api/contatos/`) com validações e logs (AC1).
  - Integração com Cloudinary para recuperação de fotos (`POST /api/cloudinary/fotos`) com paginação (parcialmente AC2).
  - Conexão com PostgreSQL e tabelas `contatos` e `logs` (AC1 e AC2).

- **Próximas Etapas**:

  - **AC2 (06/04)**:
    - Ajustar `/api/cloudinary/fotos` para usar `GET` com query parameters (`pasta`, `next_cursor`).
    - Suportar páginas específicas do front-end (Projetos, Retratos, Colabs) via filtragem de pastas.
  - **AC3 (04/05)**:
    - Implementar autenticação para login do fotógrafo (ex.: `POST /api/auth/login`).
    - Criar endpoint para gerenciamento de dados do fotógrafo (`POST/PUT /api/fotografo`).
    - Adicionar suporte a "esqueci minha senha" (ex.: `POST /api/auth/reset-password`).
  - **Entrega Final (08/06)**:
    - Adicionar endpoint para carrossel de imagens (ex.: `GET /api/cloudinary/destaques`).
    - Suportar filtros por metadados (ex.: `GET /api/cloudinary/fotos?pasta=projetos&tag=xyz`).
    - Finalizar testes de performance e segurança.

- **Riscos Conhecidos**:
  - Uso de `POST` para leitura em `/api/cloudinary/fotos`, o que não segue REST puro.
  - Possíveis falhas na integração com Cloudinary em cargas altas.

---

## Estrutura do Projeto

```
portfolio-fotografo-backend/
├── controllers/
│   ├── contatos.py
│   ├── cloudinaryapi.py
├── database/
│   ├── database.py
│   ├── migration.sql
├── services/
│   ├── logs.py
├── .env
├── .gitignore
├── requirements.txt
├── app.py
├── vercel.json
├── README.md
```

- **`controllers/`**: Lógica de roteamento para contatos e Cloudinary.
- **`database/`**: Conexão com PostgreSQL e scripts de migração.
- **`services/`**: Registro de logs.
- **`app.py`**: Ponto de entrada da API Flask.
- **`vercel.json`**: Configuração para deploy.

---

## Como Executar Localmente

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/bruclares/portfolio-fotografo-backend.git
   cd portfolio-fotografo-backend
   ```

2. **Pré-requisitos**:

   - Python 3.8+ e PostgreSQL instalados.

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:

   Crie um arquivo `.env` na raiz com:

   ```
   DATABASE_URL=postgresql://usuario:senha@host:porta/banco
   CLOUD_NAME=seu_cloud_name
   API_KEY=sua_api_key
   API_SECRET=sua_api_secret
   ```

   Certifique-se de que o `.env` está no `.gitignore`.

5. **Configure o banco de dados**:

   Execute o script de migração:

   ```bash
   psql -U usuario -d banco -f database/migration.sql
   ```

6. **Execute o servidor**:

   ```bash
   flask run
   ```

7. **Acesse a API**:
   - Disponível em `http://localhost:5000`.

---

## Links

- **GitHub Project**: [Link do Projeto](https://github.com/users/bruclares/projects/3)
- **Repositório Front-end**: [portfolio-fotografo-frontend](https://github.com/bruclares/portfolio-fotografo-frontend)
- **Repositório Back-end**: [portfolio-fotografo-backend](https://github.com/bruclares/portfolio-fotografo-backend)
- **Hospedagem na Vercel**: [Portfólio Fotógrafo](https://portfolio-fotografo.vercel.app/)
- **Design no Canva**: [Link do Design](https://www.canva.com/design/DAGdA_GiiT4/Cwp1Fd92u-JSd0oN7unAgg/view?utm_content=DAGdA_GiiT4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h0d9a7d5038)
- **Vídeo de Apresentação**: [Link do Vídeo](https://www.youtube.com/watch?v=LxZCA7SuQ8Y)

---

## Diferenciais do Projeto

1. **Integração com Cloudinary**: Recuperação dinâmica de fotos para o front-end.
2. **Escalabilidade**: Uso de Flask e PostgreSQL para suportar crescimento.
3. **Monitoramento**: Registro de logs para auditoria.
4. **Boas Práticas**: Commits semânticos, modularidade com Blueprints e versionamento no GitHub.
