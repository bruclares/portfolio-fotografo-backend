# Portfólio para Fotógrafos - Back-end

## Descrição do Projeto

O **Portfólio para Fotógrafos** é uma aplicação web Full Stack desenvolvida para fotógrafos exibirem seus portfólios de forma profissional e interativa. Este repositório contém o código do **back-end**, responsável por gerenciar a lógica de negócios, integrações com APIs externas (como o Google Fotos) e a comunicação com o banco de dados.

O back-end foi desenvolvido utilizando **Flask** (framework Python) e é responsável por:
- Gerenciar as requisições do front-end.
- Armazenar e recuperar dados no banco de dados PostgreSQL.
- Integrar-se com a API do Google Fotos para carregar as imagens dinamicamente.

## Funcionalidades do Back-end

### API RESTful
- **Formulário de Contato**: Endpoint para receber e armazenar mensagens enviadas pelos visitantes.
- **Integração com Google Fotos**: Endpoints para buscar e gerenciar fotos do portfólio a partir da API do Google Fotos.
- **Paginação de Imagens**: Endpoint para fornecer imagens com paginação, facilitando a exibição no front-end.

### Banco de Dados
- **Armazenamento de Dados**: Utiliza PostgreSQL para salvar:
  - Dados de contato dos clientes/visistantes.
  - Mensagens de contato.
  - Metadados das fotos (título, descrição, tags).
  - Informações do fotógrafo (nome, biografia, redes sociais).

### Autenticação e Gerenciamento
- **Página de Login**: Sistema de autenticação para o fotógrafo acessar a área de gerenciamento.
- **Gerenciamento de Dados**: Endpoints para atualizar informações dos visistantes/clientes, do fotógrafo e gerenciar galerias de fotos.

## Tecnologias Utilizadas

- **Back-end**: Python (Flask).
- **Banco de Dados**: PostgreSQL.
- **Integração com APIs**: Google Fotos API.
- **Hospedagem**: Vercel.
- **Ferramentas de Desenvolvimento**: Git, GitHub, VS Code.

## Entregas por AC

### AC1 (09/03)
- **API RESTful**: Desenvolvimento dos endpoints para gerenciar as requisições do formulário de contato.
- **Conexão com Banco de Dados**: Configuração do PostgreSQL e conexão com o back-end.
- **Board do Projeto**: Criação do board no GitHub Projects com as tarefas planejadas.

### AC2 (06/04)
- **Integração com Google Fotos**: Desenvolvimento da integração com a API do Google Fotos para carregar as imagens dinamicamente.
- **Paginação de Imagens**: Criação de um endpoint para fornecer imagens com paginação.
- **Banco de Dados**: Criação das tabelas `galerias` e `imagens` e armazenamento dos metadados das fotos.

### AC3 (04/05)
- **Autenticação**: Implementação do sistema de autenticação para login do fotógrafo.
- **Gerenciamento de Dados**: Endpoints para atualizar informações do fotógrafo e gerenciar galerias de fotos.

### Entrega Final (08/06)
- **Deploy**: Hospedagem do back-end na Vercel.
- **Documentação**: Criação de um README detalhado no GitHub.
- **Diagramas**: Diagrama de caso de uso e diagrama de classe.
- **Nova Funcionalidade**: Filtro de fotos por metadados.

## Diferenciais do Projeto

1. **Integração com API Externa**: Uso da API do Google Fotos para carregar as fotos dinamicamente.
2. **Deploy Contínuo**: Utilização da Vercel para garantir que o back-end esteja sempre atualizado.
3. **Boas Práticas**: Uso de commits semânticos, versionamento no GitHub.

## Links

- **GitHub Project**: [Link do Board](https://github.com/users/bruclares/projects/3)
- **Repositório Front-end**: [portfolio-fotografo-frontend](https://github.com/bruclares/portfolio-fotografo-frontend)
- **Repositório Back-end**: [portfolio-fotografo-backend](https://github.com/bruclares/portfolio-fotografo-backend)
- **Hospedagem na Vercel**: [Portfólio Fotógrafo](https://portfolio-fotografo.vercel.app/)
- **Design no Canva**: [Link do Design](https://www.canva.com/design/DAGdA_GiiT4/Cwp1Fd92u-JSd0oN7unAgg/view?utm_content=DAGdA_GiiT4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h0d9a7d5038)
- **Vídeo de Apresentação**: [Link do Vídeo]

## Como Executar o Projeto Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/bruclares/portfolio-fotografo-backend.git
   cd portfolio-fotografo-backend
   ```

2. **Crie um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor**:
   ```bash
   flask run
   ```

5. **Acesse a API**:
   A API estará disponível em `http://localhost:5000`.

