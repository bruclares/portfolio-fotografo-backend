from database.database import get_cursor
from utils.token import gerar_token_jwt
from services.logs import registrar_log
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import bcrypt
from datetime import datetime


def login_usuario(email, senha):
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT id, email, senha_hash FROM fotografo WHERE email = %s",
                (email,),
            )
            usuario = cur.fetchone()

        if not usuario:
            registrar_log("Login falhou", "Usuário não encontrado")
            return {"erro": "Dados incorretos", "codigo": 404}

        fotografo_id, email_db, senha_hash = usuario.values()

        # Verifica a senha com hash
        if not verificar_senha(senha, senha_hash):
            registrar_log("Login falhou", f"Senha inválida para {email_db}")
            return {"erro": "Dados incorretos", "codigo": 401}

        # Geração de token JWT contendo o ID do fotógrafo — usado para autenticação nas rotas protegidas
        token = gerar_token_jwt(fotografo_id)

        registrar_log("Login bem-sucedido", f"Usuário {email_db} logado")
        return {"token": token}

    except Exception as e:
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
        registrar_log("Erro no cadastro", str(e))
        return {"erro": "Erro ao cadastrar fotógrafo", "codigo": 500}


def gerar_token_recuperacao(email):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT id FROM fotografo WHERE email = %s", (email,))
            fotografo_id = cur.fetchone()["id"]

        # gera o tken
        s = Serializer(current_app.config["SECRET_KEY"], salt="recover-key")
        token = s.dumps({"fid": fotografo_id, "timestamp": datetime.now().timestamp()})

        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO tokens_recuperacao (token, fotografo_id) VALUES (%s, %s)
                """,
                (token, fotografo_id),
            )
            cur.connection.commit()
        return {"token": token}

    except Exception as e:
        cur.connection.rollback()
        print(str(e))
        return {
            "erro": "Não foi possível gerar o token, tente novamente.",
            "codigo": 500,
        }


def verificar_token_recuperacao(token):
    try:
        mensagem = None

        with get_cursor() as cur:
            cur.execute(
                """
                SELECT fotografo_id, usado, expira_em FROM tokens_recuperacao 
                WHERE token = %s 
                FOR UPDATE  -- Bloqueia o registro para evitar race condition
            """,
                (token,),
            )

            resultado = cur.fetchone()

            print(resultado)

            if not (resultado):
                mensagem = "Token inválido. Redirecionando para uma nova solicitação..."
            elif resultado["usado"] is True:
                mensagem = "Token já foi utilizado. Redirecionando para uma nova solicitação..."
            elif resultado["expira_em"] < datetime.now():
                mensagem = "Token expirado. Redirecionando para uma nova solicitação..."

            if mensagem is not None:
                return {"erro": mensagem, "codigo": 400}

            return resultado

    except Exception as e:
        registrar_log("Token inválido", str(e))
        return {"erro": "Não foi possível recuperar o token", "codigo": 500}


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
