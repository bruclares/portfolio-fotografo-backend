from flask_jwt_extended import create_access_token
import uuid
from datetime import timedelta


def gerar_token_jwt(fotografo_id):
    """
    Gera um token JWT seguro com identificador único (JTI) para controle de denylist.

    O token contém claims adicionais com:
        - jti: Identificador único do token (usado na lista negra)
        - fotografo_id: ID do usuário autenticado

    Args:
        fotografo_id (int): ID do fotógrafo autenticado que será incluído no token.

    Returns:
        str: Token JWT assinado e codificado pronto para uso nas requisições protegidas.

    Raises:
        Exception: Se ocorrer erro na geração do token (geralmente não é lançado diretamente aqui,
                   mas pode ser causado por problemas nas configurações do Flask-JWT).
    """
    # Gera um identificador único (JTI) para este token
    jti = str(uuid.uuid4())

    # Claims adicionais para o token JWT
    additional_claims = {"jti": jti, "fotografo_id": str(fotografo_id)}

    # Define tempo de expiração do token (24 horas)
    expires = timedelta(hours=24)

    # Gera o token JWT com as configurações definidas
    token = create_access_token(
        identity=str(fotografo_id),
        additional_claims=additional_claims,
        expires_delta=expires,
    )

    return token
