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