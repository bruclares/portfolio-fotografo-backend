from flask import Blueprint, request, jsonify
from services.auth_service import login_usuario, cadastrar_fotografo


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    resultado = login_usuario(email, senha)

    if resultado.get("erro"):
        return jsonify({"erro": resultado["erro"]}), resultado["codigo"]

    return jsonify(resultado), 200


@auth_bp.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    resultado = cadastrar_fotografo(email, senha)

    if resultado.get("erro"):
        return jsonify({"erro": resultado["erro"]}), resultado["codigo"]

    return jsonify(resultado), 201
