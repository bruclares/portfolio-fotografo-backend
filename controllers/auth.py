from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.auth_service import (
    login_usuario,
    cadastrar_fotografo,
    gerar_token_recuperacao,
    email_existe,
    verificar_token_recuperacao,
    registrar_log,
)
from database.database import get_cursor, connection
from services.email_service import enviar_email_recuperacao
import bcrypt

# Define o blueprint de autenticação, agrupando rotas de login e cadastro
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint público para login de fotógrafo.
    Espera um JSON com 'email' e 'senha'.
    """

    # Captura e valida os dados recebidos
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        # Rejeita requisições incompletas
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    resultado = login_usuario(email, senha)

    # Em caso de erro no service (ex: usuário inválido ou senha incorreta)
    if resultado.get("erro"):
        return jsonify({"erro": resultado["erro"]}), resultado["codigo"]

    # Retorna token e dados do usuário autenticado
    return jsonify(resultado), 200


@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    """
    Endpoint público para cadastro do fotógrafo responsável.
    Espera um JSON com 'email' e 'senha'.
    """

    # Captura e valida os dados recebidos
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    resultado = cadastrar_fotografo(email, senha)

    if resultado.get("erro"):
        return jsonify({"erro": resultado["erro"]}), resultado["codigo"]

    return jsonify(resultado), 201


@auth_bp.route("/recuperar-senha", methods=["POST"])
def recuperar_senha():

    data = request.get_json()
    email = data.get("email")

    if not email:
        # Rejeita requisições incompletas
        return jsonify({"erro": "Digite seu email."}), 400

    if email_existe(email):
        token = gerar_token_recuperacao(email)

        if token.get("erro"):
            return jsonify({"erro": token["erro"]}), token["codigo"]

        enviar_email_recuperacao(email, token["token"])

        return jsonify({"sucesso": "E-mail para recuperação de senha enviado!"}), 200

    else:
        return jsonify({"erro": "E-mail não encontrado."}), 404


@auth_bp.route("/resetar-senha", methods=["POST"])
def resetar_senha():
    """
    Endpoint para redefinir senha usando token enviado por email.
    Espera um JSON com 'token' e 'nova_senha".
    """
    data = request.get_json()
    token = data.get("token")
    nova_senha = data.get("nova-senha")
    confirmar_senha = data.get("confirmar-senha")

    if not nova_senha or not confirmar_senha:
        return jsonify({"erro": "Campos de senha são obrigatórios"}), 400

    if not token:
        return jsonify({"erro": "Token é obrigatório"}), 400

    if confirmar_senha != nova_senha:
        return jsonify({"erro": "Campos de senha não podem ser diferentes."}), 400

    try:
        resultado = verificar_token_recuperacao(token)

        if resultado.get("erro"):
            return jsonify({"erro": resultado["erro"]}), resultado["codigo"]

        fotografo_id = resultado["fotografo_id"]

        # gerar o hash da nova senha
        senha_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        # atualizar no banco
        with get_cursor() as cur:
            cur.execute(
                "UPDATE fotografo SET senha_hash = %s WHERE id = %s",
                (senha_hash, fotografo_id),
            )

            cur.execute(
                """
                UPDATE tokens_recuperacao 
                SET usado = TRUE 
                WHERE token = %s
            """,
                (token,),
            )
            cur.connection.commit()
        return (
            jsonify(
                {
                    "sucesso": "Senha redefinida com sucesso. Redirecionando você para o login..."
                }
            ),
            200,
        )

    except Exception as e:
        connection.rollback()
        print(f"Erro: {str(e)}")
        return jsonify({"erro": "Erro ao redefinir a senha"}), 500


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Endpoint para logout seguro.
    Adiciona o token atual à denylist
    """
    try:
        # obtém dados do token atual
        token_data = get_jwt()
        jti = token_data["jti"]
        fotografo_id = token_data["fotografo_id"]

        # adiciona token à denylist
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO tokens_denylist (token_jti, fotografo_id, motivo)
                VALUES (%s, %s, %s)
                """,
                (jti, fotografo_id, "logout"),
            )
            cur.connection.commit()

        # log do logout
        registrar_log("Logout realizado", f"Token {jti[:8]}... invalidado")

        return (
            jsonify(
                {"sucesso": "Logout realizado com sucesso", "codigo": "LOGOUT_SUCESSO"}
            ),
            200,
        )

    except Exception as e:
        registrar_log("Erro no logout", str(e))
        return (
            jsonify({"erro": "Erro interno no servidor", "codigo": "ERRO_LOGOUT"}),
            500,
        )
