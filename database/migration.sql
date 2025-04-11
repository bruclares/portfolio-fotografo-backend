CREATE DATABASE portifolio_fotografo;

CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    mensagem TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table logs (
    id SERIAL primary key, 
    tipo_log varchar(255),
    data_hora timestamp default CURRENT_TIMESTAMP, 
    ip_usuario varchar(45),
    user_agent varchar(255),
    url varchar(255),
    metodo varchar(10),
    status varchar(50)
);

-- Tabela de administrador (fotógrafo) apenas um registro
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

create table contatos_fotografo (
id SERIAL PRIMARY KEY, 
tipo varchar(255),
contato varchar(255),
criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);