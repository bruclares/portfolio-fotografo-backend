from database.database import connection, get_cursor
from utils.hash import verificar_senha
from utils.token import gerar_token_jwt
from services.logs import registrar_log
import bcrypt


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
            return {"erro": "Usuário não encontrado", "codigo": 404}

        # desempacota a lista usuario nas novas variáveis
        id_fotografo, email_db, senha_hash = usuario.values()
        print(usuario.values())

        if not verificar_senha(senha, senha_hash):
            registrar_log("Login falhou", f"Senha inválida para {email_db}")
            return {"erro": "Senha inválida", "codigo": 401}
        print("passou da senha, sei lá")
        token = gerar_token_jwt(id_fotografo)
        print("qualquer coisa", token)

        registrar_log("Login bem-sucedido", f"Usuário {email_db} logado")
        return {"token": token}

    except Exception as e:
        print(str(e))
        registrar_log("Erro no login", str(e))
        return {"erro": "Erro interno no servidor", "codigo": 500}


def cadastrar_fotografo(email, senha):
    try:
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO fotografo (id, email, senha_hash) VALUES (%s, %s, %s)",
                (1, email, senha_hash),
            )

        registrar_log("Cadastro bem-sucedido", f"Usuário {email} cadastrado")
        return {"mensagem": "Fotógrafo cadastrado com sucesso"}

    except Exception as e:
        print(str(e))
        registrar_log("Erro no cadastro", str(e))
        return {"erro": "Erro ao cadastrar fotógrafo", "codigo": 500}
