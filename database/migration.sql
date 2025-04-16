-- Criação do banco de dados principal
CREATE DATABASE portifolio_fotografo;

-- Tabela de mensagens enviadas pelo formulário de contato do site
CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,                         -- Identificador único da mensagem
    nome VARCHAR(50) NOT NULL,                     -- Nome da pessoa que enviou a mensagem
    telefone VARCHAR(20),                          -- Telefone para retorno (opcional)
    email VARCHAR(100),                            -- E-mail para contato (opcional)
    mensagem TEXT NOT NULL,                        -- Conteúdo da mensagem
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data/hora do envio (gerada automaticamente)
);

-- Tabela de logs de requisições HTTP para auditoria e debug
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,                         -- Identificador único do log
    tipo_log VARCHAR(255),                         -- Tipo do log (ex: Erro, Sucesso, Validação, etc.)
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp do evento logado
    ip_usuario VARCHAR(45),                        -- IP de origem da requisição
    user_agent VARCHAR(255),                       -- Navegador/dispositivo usado
    url VARCHAR(255),                              -- URL requisitada
    metodo VARCHAR(10),                            -- Método HTTP (GET, POST, etc.)
    status VARCHAR(50)                             -- Status da requisição (200, 400, 500, etc.)
);

-- Tabela que representa o administrador do sistema (fotógrafo) - somente 1 registro permitido
CREATE TABLE fotografo (
    id INT PRIMARY KEY CHECK (id = 1),              -- Identificador fixo (permite apenas 1 fotógrafo no sistema)
    nome VARCHAR(255),                              -- Nome do fotógrafo
    email VARCHAR(255) NOT NULL,                    -- E-mail de acesso
    senha_hash VARCHAR(255) NOT NULL,               -- Hash da senha (armazenamento seguro)
    token_recuperacao VARCHAR(255),                 -- Token gerado para recuperação de senha
    token_expiracao TIMESTAMP,                      -- Validade do token de recuperação
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Registro da data de criação
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Registro da última atualização
);

-- Tabela de formas de contato públicas do fotógrafo
CREATE TABLE formas_contato (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255),                                -- Ex: Instagram, E-mail, Telefone
    contato VARCHAR(255),                             -- Ex: @aurora_espinosa, contato@aurora.com.br
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
