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
    Autentica o fotógrafo com e-mail e senha.

    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "fotografo@example.com"
            senha:
              type: string
              example: "minhasenha123"
    responses:
      200:
        description: Login bem-sucedido. Retorna token JWT e dados do usuário.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token JWT válido por 30 minutos
            id:
              type: integer
              description: ID do fotógrafo
            email:
              type: string
      400:
        description: Campos obrigatórios ausentes
        examples:
          {"erro": "Email e senha são obrigatórios"}
      401:
        description: Credenciais inválidas
        examples:
          {"erro": "E-mail ou senha incorretos"}
    """

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
    """
    Cadastra um novo fotógrafo (único no sistema).

    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "novo_fotografo@example.com"
            senha:
              type: string
              example: "minhasenha123"
    responses:
      201:
        description: Fotógrafo cadastrado com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
            email:
              type: string
      400:
        description: Campos obrigatórios ausentes
        examples:
          {"erro": "Email e senha são obrigatórios"}
      409:
        description: E-mail já cadastrado
        examples:
          {"erro": "E-mail já cadastrado"}
    """

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
    """
    Envia um e-mail com link/token para recuperação de senha.

    ---
    tags:
      - Recuperação de Senha
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "fotografo@example.com"
    responses:
      200:
        description: E-mail de recuperação enviado
        examples:
          {"sucesso": "E-mail para recuperação de senha enviado!"}
      400:
        description: E-mail ausente
        examples:
          {"erro": "Digite seu email."}
      404:
        description: E-mail não encontrado
        examples:
          {"erro": "E-mail não encontrado."}
    """

    data = request.get_json()
    email = data.get("email")

    if not email:
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
    Redefine a senha do usuário com base no token recebido via e-mail.

    ---
    tags:
      - Recuperação de Senha
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            token:
              type: string
              example: "abc123xyz"
            nova_senha:
              type: string
              example: "nova_senha_segura"
            confirmar_senha:
              type: string
              example: "nova_senha_segura"
    responses:
      200:
        description: Senha redefinida com sucesso
        examples:
          {"sucesso": "Senha redefinida com sucesso..."}
      400:
        description: Erros de validação
        examples:
          {"erro": "Campos de senha são obrigatórios"}
          {"erro": "Campos de senha não podem ser diferentes."}
          {"erro": "Token é obrigatório"}
      500:
        description: Erro interno ao processar a redefinição
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
        senha_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

        with get_cursor() as cur:
            cur.execute(
                "UPDATE fotografo SET senha_hash = %s WHERE id = %s",
                (senha_hash, fotografo_id),
            )
            cur.execute(
                "UPDATE tokens_recuperacao SET usado = TRUE WHERE token = %s",
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
    Invalida o token atual adicionando-o à lista negra (denylist).

    ---
    tags:
      - Autenticação
    parameters:
        - name: Authorization
          in: header
          description: Token JWT no formato `Bearer <token>`
          required: true
          type: string
    responses:
      200:
        description: Logout realizado com sucesso
        examples:
          {"sucesso": "Logout realizado com sucesso"}
      500:
        description: Erro interno ao processar o logout
    """

    try:
        token_data = get_jwt()
        jti = token_data["jti"]
        fotografo_id = token_data["fotografo_id"]

        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO tokens_denylist (token_jti, fotografo_id, motivo) VALUES (%s, %s, %s)",
                (jti, fotografo_id, "logout"),
            )
            cur.connection.commit()

        registrar_log("Logout realizado", f"Token {jti[:8]}... invalidado")
        return jsonify({"sucesso": "Logout realizado com sucesso"}), 200

    except Exception as e:
        registrar_log("Erro no logout", str(e))
        return jsonify({"erro": "Erro interno no servidor"}), 500
