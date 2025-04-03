# Portfólio para Fotógrafos - Back-end

## Descrição do Projeto

O **Portfólio para Fotógrafos** é uma aplicação web Full Stack projetada para fotógrafos exibirem seus portfólios de maneira profissional e interativa. Este repositório contém o código do **back-end**, responsável por gerenciar a lógica de negócios, integrar armazenamento de imagens via Cloudinary e processar contatos de clientes. A API foi desenvolvida com **Flask** e utiliza **PostgreSQL** para o banco de dados, oferecendo uma solução escalável para fotógrafos como Aurora Espinosa.

O back-end permite:

- Receber e armazenar mensagens de contato de visitantes.
- Gerenciar e recuperar fotos armazenadas no Cloudinary.
- Fornecer paginação e filtragem de imagens para o front-end.

**Status do Projeto**: Este projeto está em desenvolvimento ativo. Algumas funcionalidades estão completas, mas podem haver bugs ou mudanças frequentes. Estou trabalhando para finalizar a autenticação, otimizar a integração com Cloudinary e realizar testes de performance antes do lançamento final.

---

## Funcionalidades

- **API REST**:

  - Endpoint para envio e armazenamento de contatos (nome, email, mensagem).
  - Endpoint para recuperar fotos do Cloudinary com paginação e filtragem.
  - Rota de status para verificar se a API está online.

- **Banco de Dados**:

  - Armazenamento de dados de contato, logs e metadados de fotos no PostgreSQL.
  - Tabelas para contatos, logs e configurações do fotógrafo.

- **Integração com Cloudinary**:

  - Upload e recuperação dinâmica de imagens para galerias de portfólio.

- **Segurança e Logs**:
  - Registro de todas as requisições para auditoria.
  - Uso de variáveis de ambiente para proteger credenciais sensíveis.

---

## Tecnologias Utilizadas

- **Back-end**: Python (Flask)
- **Banco de Dados**: PostgreSQL
- **Armazenamento de Imagens**: Cloudinary
- **Ferramentas**: Psycopg (driver PostgreSQL), Flask-CORS, Dotenv
- **Deploy**: Vercel
- **Controle de Versão**: Git, GitHub

---

## Status de Desenvolvimento

- **Etapas Concluídas**:

  - Desenvolvimento dos endpoints de contatos e integração com Cloudinary.
  - Configuração do banco de dados PostgreSQL e criação das tabelas principais.
  - Deploy inicial na Vercel.

- **Próximas Etapas**:

  - Implementação de autenticação para o fotógrafo.
  - Adição de filtros avançados para fotos (por tags, datas, etc.).
  - Testes de performance e segurança.
  - Documentação completa da API (Swagger ou similar).

- **Riscos Conhecidos**:

  - Possíveis bugs na integração com Cloudinary em cargas altas.
  - Falta de tratamento de erros detalhado em alguns endpoints.

- **Cronograma Estimado**:
  - Entrega Final: 08/06 (sujeito a alterações).

---

## Estrutura do Projeto

```
projeto/
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
```

---

## Como Executar Localmente

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/bruclares/portfolio-fotografo-backend.git
   cd portfolio-fotografo-backend
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**:

   Crie um arquivo `.env` na raiz do projeto com:

   ```
   DATABASE_URL=postgresql://usuario:senha@host:porta/banco
   CLOUD_NAME=seu_cloud_name
   API_KEY=sua_api_key
   API_SECRET=sua_api_secret
   ```

   Certifique-se de que o `.env` está no `.gitignore`.

4. **Configure o banco de dados**:

   Execute o script de migração:

   ```bash
   psql -U usuario -d banco -f database/migration.sql
   ```

5. **Execute o servidor**:

   ```bash
   flask run
   ```

6. **Acesse a API**:

   A API estará disponível em `http://localhost:5000`.

---

## Links Úteis

- **Repositório Front-end**: [portfolio-fotografo-frontend](https://github.com/bruclares/portfolio-fotografo-frontend)
- **Board do Projeto**: [GitHub Projects](https://github.com/users/bruclares/projects/3)
- **Deploy na Vercel**: [Portfólio Fotógrafo](https://portfolio-fotografo.vercel.app/)
- **Design**: [Canva](https://www.canva.com/design/DAGdA_GiiT4/Cwp1Fd92u-JSd0oN7unAgg/view?utm_content=DAGdA_GiiT4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h0d9a7d5038)
- **Vídeo de Apresentação**: [YouTube](https://www.youtube.com/watch?v=LxZCA7SuQ8Y)
