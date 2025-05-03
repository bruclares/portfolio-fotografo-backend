-- Criação do banco de dados principal
CREATE DATABASE portifolio_fotografo;

-- Tabela de mensagens enviadas pelo formulário de contato do site
CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,                        
    nome VARCHAR(50) NOT NULL,                     
    telefone VARCHAR(20),                          
    email VARCHAR(100),                            
    mensagem TEXT NOT NULL,                        
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Tabela de logs de requisições HTTP para auditoria e debug
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

-- Tabela que representa o administrador do sistema (fotógrafo) - somente 1 registro permitido
CREATE TABLE fotografo (
    id INT PRIMARY KEY CHECK (id = 1),              
    nome VARCHAR(255),                              
    email VARCHAR(255) NOT NULL,                    
    senha_hash VARCHAR(255) NOT NULL,               
    token_recuperacao VARCHAR(255),                 
    token_expiracao TIMESTAMP,                      
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- Tabela de formas de contato públicas do fotógrafo
CREATE TABLE formas_contato (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255),                                
    contato VARCHAR(255),                             
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tokens_recuperacao (
    id SERIAL PRIMARY KEY,
    token VARCHAR(500) UNIQUE NOT NULL,
    fotografo_id INTEGER NOT NULL REFERENCES fotografo(id),
    usado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expira_em TIMESTAMP GENERATED ALWAYS AS (criado_em + INTERVAL '1 hour') STORED
);

CREATE INDEX idx_tokens_nao_usados ON tokens_recuperacao(fotografo_id) WHERE usado = FALSE;