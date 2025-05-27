from flask_jwt_extended import create_access_token
import uuid
from datetime import timedelta


def gerar_token_jwt(fotografo_id):
    """
    Gera token JWT com JTI único para controle de denylist
    """
    # gera um identificador único para este token
    jti = str(uuid.uuid4())

    # claims adicionais pra o token
    additional_claims = {"jti": jti, "fotografo_id": str(fotografo_id)}

    # token expira em 24 horas
    expires = timedelta(hours=24)

    token = create_access_token(
        identity=str(fotografo_id),
        additional_claims=additional_claims,
        expires_delta=expires,
    )

    return token
