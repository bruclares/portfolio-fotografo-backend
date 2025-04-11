from flask_jwt_extended import create_access_token
from datetime import timedelta


def gerar_token_jwt(usuario_id):
    """
    Gera um token JWT válido por 1 hora para o usuário autenticado.

    Parâmetros:
        - usuario_id (int ou str): Identificador único do usuário.

    Retorna:
        - token (str): Token JWT que pode ser utilizado para autenticação em rotas protegidas.
    """
    token = create_access_token(identity=usuario_id, expires_delta=timedelta(hours=1))
    return token
