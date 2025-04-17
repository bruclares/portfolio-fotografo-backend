from flask import Blueprint, request, jsonify
from services.auth_service import login_usuario, cadastrar_fotografo

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
