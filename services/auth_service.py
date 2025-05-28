from database.database import get_cursor
from utils.token import gerar_token_jwt
from services.logs import registrar_log
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import bcrypt
from datetime import datetime


def login_usuario(email, senha):
    """
    Autentica um fotógrafo com base no e-mail e senha fornecidos.

    Realiza uma busca no banco de dados pelo e-mail, verifica se a senha está correta,
    e gera um token JWT caso a autenticação seja bem-sucedida.

    Args:
        email (str): E-mail do usuário.
        senha (str): Senha fornecida pelo usuário.

    Returns:
        dict: Com 'token' em caso de sucesso ou mensagem de erro em caso de falha.
            Exemplos:
                {'token': '...'}  # Login bem-sucedido
                {'erro': 'Dados incorretos', 'codigo': 401}  # Credenciais inválidas
                {'erro': 'Erro interno no servidor', 'codigo': 500}  # Erro inesperado

    Raises:
        Exception: Se ocorrer qualquer erro durante a execução da função.
    """
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
    """
    Cadastra um novo fotógrafo no sistema com e-mail e senha criptografada.

    Apenas um fotógrafo pode ser cadastrado no sistema (ID fixo = 1).
    Caso já exista um cadastro, retorna erro.

    Args:
        email (str): E-mail do fotógrafo.
        senha (str): Senha informada pelo usuário (será hashada).

    Returns:
        dict: Mensagem de sucesso ou erro.
            Exemplos:
                {'mensagem': 'Fotógrafo cadastrado com sucesso'}
                {'erro': 'Erro ao cadastrar fotógrafo', 'codigo': 500}

    Raises:
        Exception: Se ocorrer qualquer erro durante a execução da função.
    """
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
    """
    Gera e armazena um token seguro para recuperação de senha.

    O token tem validade de 1 hora e só pode ser usado uma vez.
    Usado para criar links seguros de redefinição de senha via e-mail.

    Args:
        email (str): E-mail do usuário que solicitou recuperação de senha.

    Returns:
        dict: Contém o token gerado ou mensagem de erro.
            Exemplos:
                {'token': 'abc123xyz'}
                {'erro': 'Não foi possível gerar o token...', 'codigo': 500}

    Raises:
        Exception: Se ocorrer qualquer erro durante a execução da função.
    """
    try:
        with get_cursor() as cur:
            cur.execute("SELECT id FROM fotografo WHERE email = %s", (email,))
            fotografo_id = cur.fetchone()["id"]

        # Gera o token
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
    """
    Valida um token de recuperação de senha.

    Verifica se o token existe, ainda é válido e não foi usado anteriormente.

    Args:
        token (str): Token recebido via e-mail.

    Returns:
        dict: Com os dados do token (fotografo_id) se for válido.
            Ou mensagem de erro caso contrário.
            Exemplo:
                {'fotografo_id': 1, 'usado': False, 'expira_em': ...}
                {'erro': 'Token já foi utilizado...', 'codigo': 400}

    Raises:
        Exception: Se ocorrer qualquer erro durante a execução da função.
    """
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
    """
    Compara uma senha fornecida com seu hash armazenado.

    Usa bcrypt para verificar a integridade da senha.

    Args:
        senha_digitada (str): Senha informada pelo usuário.
        senha_hash (str): Hash armazenado no banco de dados.

    Returns:
        bool: True se as senhas coincidem, False caso contrário.
    """
    try:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8"), senha_hash.encode("utf-8")
        )
    except Exception as e:
        registrar_log("Erro na verificação de senha", str(e))
        return False


def email_existe(email):
    """
    Verifica se um e-mail já está cadastrado no sistema.

    Args:
        email (str): E-mail a ser verificado.

    Returns:
        bool: True se o e-mail já estiver cadastrado, False caso contrário.
    """
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
