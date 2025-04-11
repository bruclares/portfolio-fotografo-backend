from flask_jwt_extended import create_access_token
from datetime import timedelta


def gerar_token_jwt(usuario_id):
    token = create_access_token(identity=usuario_id, expires_delta=timedelta(hours=1))
    return token
