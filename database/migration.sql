-- migration.sql
-- Script de migração para criação do banco de dados e tabelas do sistema "Portfólio Fotógrafo"
-- Tabelas criadas na ordem correta para respeitar constraints de chave estrangeira

---------------------------------------------------------------------
-- 1. Criação do Banco de Dados Principal
---------------------------------------------------------------------
CREATE DATABASE portifolio_fotografo;

\c portifolio_fotografo;

---------------------------------------------------------------------
-- 2. Tabela: fotografo
---------------------------------------------------------------------
-- Representa o único usuário-administrador do sistema (o fotógrafo).
-- Garantido por constraint que só existirá um registro (id = 1).
CREATE TABLE fotografo (
    id INT PRIMARY KEY CHECK (id = 1),
    nome VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    token_recuperacao VARCHAR(255),
    token_expiracao TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------------------
-- 3. Tabela: tokens_recuperacao
---------------------------------------------------------------------
-- Armazena tokens usados para recuperação de senha do usuário.
CREATE TABLE tokens_recuperacao (
    id SERIAL PRIMARY KEY,
    token VARCHAR(500) UNIQUE NOT NULL,
    fotografo_id INTEGER NOT NULL REFERENCES fotografo(id),
    usado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expira_em TIMESTAMP GENERATED ALWAYS AS (criado_em + INTERVAL '1 hour') STORED
);

-- Índice para buscar tokens não usados por fotógrafo
CREATE INDEX idx_tokens_nao_usados ON tokens_recuperacao(fotografo_id) WHERE usado = FALSE;

---------------------------------------------------------------------
-- 4. Tabela: tokens_denylist
---------------------------------------------------------------------
-- Lista negra de tokens JWT que foram invalidados (por logout, etc.).
CREATE TABLE tokens_denylist (
    id SERIAL PRIMARY KEY,
    token_jti VARCHAR(36) NOT NULL UNIQUE,
    fotografo_id INTEGER NOT NULL REFERENCES fotografo(id),
    data_denylist TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(50) DEFAULT 'logout'
);

-- Índice para busca rápida de tokens JWT revogados
CREATE INDEX idx_tokens_denylist_jti ON tokens_denylist(token_jti);

---------------------------------------------------------------------
-- 5. Tabela: contatos
---------------------------------------------------------------------
-- Armazena as mensagens recebidas via formulário de contato do site.
CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    mensagem TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------------------
-- 6. Tabela: formas_contato
---------------------------------------------------------------------
-- Armazena informações públicas sobre como entrar em contato.
CREATE TABLE formas_contato (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255),
    contato VARCHAR(255),
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------------------
-- 7. Tabela: logs
---------------------------------------------------------------------
-- Armazena registros de acesso e erros para auditoria e depuração.
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    tipo_log VARCHAR(255),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_usuario VARCHAR(45),
    user_agent VARCHAR(255),
    url VARCHAR(255),
    metodo VARCHAR(10),
    status VARCHAR(50)
);