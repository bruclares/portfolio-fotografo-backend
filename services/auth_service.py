from database.database import get_cursor
from utils.token import gerar_token_jwt
from services.logs import registrar_log
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import bcrypt
from datetime import datetime


def login_usuario(email, senha):
    try:
        # Utiliza um cursor com context manager para garantir que seja fechado corretamente após o uso
        with get_cursor() as cur:
            # Busca o usuário pelo e-mail (usuário é único e fixo no sistema)
            cur.execute(
                "SELECT id, email, senha_hash FROM fotografo WHERE email = %s",
                (email,),
            )
            usuario = cur.fetchone()

        if not usuario:
            # Garante rastreabilidade do erro via logs
            registrar_log("Login falhou", "Usuário não encontrado")
            return {"erro": "Usuário não encontrado", "codigo": 404}

        # Desestrutura os dados retornados para facilitar leitura e uso
        id_fotografo, email_db, senha_hash = usuario.values()

        # Verifica a senha com hash usando função utilitária (mantém a responsabilidade separada)
        if not verificar_senha(senha, senha_hash):
            registrar_log("Login falhou", f"Senha inválida para {email_db}")
            return {"erro": "Senha inválida", "codigo": 401}

        # Geração de token JWT contendo o ID do fotógrafo — usado para autenticação nas rotas protegidas
        token = gerar_token_jwt(id_fotografo)

        registrar_log("Login bem-sucedido", f"Usuário {email_db} logado")
        return {"token": token}

    except Exception as e:
        # Falha genérica no backend
        print(str(e))
        registrar_log("Erro no login", str(e))
        return {"erro": "Erro interno no servidor", "codigo": 500}


def cadastrar_fotografo(email, senha):
    try:
        # Gera hash seguro para a senha com bcrypt (salt incluso por padrão)
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        with get_cursor() as cur:
            # Inserção fixa com ID = 1, pois o sistema permite apenas um fotógrafo
            cur.execute(
                "INSERT INTO fotografo (id, email, senha_hash) VALUES (%s, %s, %s)",
                (1, email, senha_hash),
            )

        registrar_log("Cadastro bem-sucedido", f"Usuário {email} cadastrado")
        return {"mensagem": "Fotógrafo cadastrado com sucesso"}

    except Exception as e:
        # Falha durante o cadastro — logamos o erro para auditoria e suporte
        registrar_log("Erro no cadastro", str(e))
        return {"erro": "Erro ao cadastrar fotógrafo", "codigo": 500}


def gerar_token_recuperacao(email):
    # cria um serializador com a chave secreta do Flask
    s = Serializer(
        current_app.config["SECRET_KEY"], salt="recover-key"
    )  # salt é um identificador único
    # token = s.dumps({"email": email})
    return s.dumps(
        {"email": email, "used": False, "timestamp": datetime.now().timestamp()}
    )


def verificar_token_recuperacao(token):
    try:
        s = Serializer(current_app.config["SECRET_KEY"], salt="recover-key")
        data = s.loads(token, max_age=3600)
        return data["email"]
    except Exception as e:
        registrar_log("Token inválido", str(e))
        return None


def verificar_senha(senha_digitada, senha_hash):
    try:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8"), senha_hash.encode("utf-8")
        )
    except Exception as e:
        registrar_log("Erro na verificação de senha", str(e))
        return False


def email_existe(email):

    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT email FROM fotografo WHERE email = %s",
                (email,),
            )
            usuario = cur.fetchone()

        return usuario is not None

    except Exception as e:
        registrar_log("Erro ao verificar email", str(e))
        return {"erro": "Não foi possível verificar email", "codigo": 500}
