from flask import Blueprint, request, jsonify, current_app
from itsdangerous import (
    URLSafeTimedSerializer as Serializer,
    SignatureExpired,
    BadSignature,
)
from services.auth_service import (
    login_usuario,
    cadastrar_fotografo,
    gerar_token_recuperacao,
    email_existe,
)
from database.database import get_cursor
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

    # Caso haja falha de validação ou conflito (ex: email já usado)
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
        enviar_email_recuperacao(email, token)
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
    nova_senha = data.get("nova_senha")

    if not token or not nova_senha:
        return jsonify({"erro": "Token e nova senha são obrigatórios"}), 400

    with get_cursor() as cur:
        try:
            s = Serializer(current_app.config["SECRET_KEY"], salt="recover-key")
            # tenta decodificar o token e pegar o email original
            dados = s.loads(token, max_age=3600)  # 1 hora de validade

            # verifica se token já foi usado
            if dados.get("used", True):  # assume True como padrão por segurança
                return jsonify({"erro": "Token já utilizado"}), 400

            email = dados["email"]

        except SignatureExpired:
            return jsonify({"erro": "Token expirado"}), 400
        except BadSignature:
            return jsonify({"erro": "Token inválido"}), 400
        except Exception as e:
            print(str(e))
            return jsonify({"erro": "Erro ao redefinir a senha"}), 500

        try:
            # gerar o hash da nova senha
            senha_hash = bcrypt.hashpw(
                nova_senha.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            # atualizar no banco
            cur.execute(
                "UPDATE fotografo SET senha_hash = %s WHERE email = %s",
                (senha_hash, email),
            )

            cur.connection.commit()
            return jsonify({"mensagem": "Senha redefinida com sucesso"}), 200

        except SignatureExpired:
            return jsonify({"erro": "Token expirado"}), 400
        except BadSignature:
            return jsonify({"erro": "Token inválido"}), 400
        except Exception as e:
            cur.connection.rollback()
            print(f"Erro: {str(e)}")
            return jsonify({"erro": "Erro ao redefinir a senha"}), 500
