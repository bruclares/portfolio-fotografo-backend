from flask import Blueprint, jsonify, request
from database.database import connection, get_cursor
import psycopg
from services.logs import registrar_log
from flask_jwt_extended import jwt_required

formas_contato_bp = Blueprint("formas_contato", __name__)


# Rota pública - sem autenticação
@formas_contato_bp.route("", methods=["GET"])
def listar_formas_contato_publico():
    """
    Retorna informações públicas sobre formas de contato do fotógrafo.

    ---
    tags:
      - Formas de Contato (Público)
    responses:
      200:
        description: Lista de formas de contato pública retornada com sucesso
        schema:
          type: object
          properties:
            redesocial_nome:
              type: string
              description: Nome da rede social (ex: Instagram)
            redesocial_perfil:
              type: string
              description: Link do perfil
            email:
              type: string
              description: E-mail público do fotógrafo
            telefone:
              type: string
              description: Telefone de contato
      500:
        description: Erro ao buscar dados
        examples:
          {"erro": "Erro ao buscar formas de contato"}
    """

    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT redesocial_nome, redesocial_perfil, email, telefone
                FROM formas_contato
            """
            )
            resultados = cur.fetchone()

        registrar_log(
            "Formas de Contato Públicas Listadas", "Consulta realizada com sucesso"
        )
        return jsonify(resultados), 200

    except psycopg.DatabaseError as e:
        connection.rollback()
        registrar_log("Erro ao Listar Formas de Contato Públicas", str(e))
        return jsonify({"erro": "Erro ao buscar formas de contato"}), 500


# Rota privada - com autenticação obrigatória
@formas_contato_bp.route("/admin", methods=["GET"])
@jwt_required()
def listar_formas_contato_admin():
    """
    Retorna todas as formas de contato com dados completos (requer autenticação).

    ---
    tags:
      - Formas de Contato (Admin)
    security:
      - JWT: []
    responses:
      200:
        description: Dados completos das formas de contato retornados com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            redesocial_nome:
              type: string
            redesocial_perfil:
              type: string
            telefone:
              type: string
            email:
              type: string
            criado_em:
              type: string
              format: date-time
            atualizado_em:
              type: string
              format: date-time
      500:
        description: Erro ao buscar dados
        examples:
          {"erro": "Erro ao buscar formas de contato"}
    """

    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM formas_contato")
            resultados = cur.fetchone()

        registrar_log(
            "Formas de Contato Admin Listadas", "Consulta realizada com sucesso"
        )
        return jsonify(resultados), 200

    except psycopg.DatabaseError as e:
        connection.rollback()
        registrar_log("Erro ao Listar Formas de Contato Admin", str(e))
        return jsonify({"erro": "Erro ao buscar formas de contato"}), 500


@formas_contato_bp.route("/<int:id>", methods=["POST"])
@jwt_required()
def atualizar_forma_contato(id):
    """
    Atualiza os dados de uma forma de contato específica pelo ID.

    ---
    tags:
      - Formas de Contato (Admin)
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da forma de contato a ser atualizada
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            redesocial_nome:
              type: string
              example: "Instagram"
            redesocial_perfil:
              type: string
              example: "https://instagram.com/fotografo "
            telefone:
              type: string
              example: "(11) 98765-4321"
            email:
              type: string
              example: "fotografo@example.com"
    security:
      - JWT: []
    responses:
      200:
        description: Forma de contato atualizada com sucesso
        examples:
          {"sucesso": "Forma de contato alterada com sucesso!"}
      400:
        description: Erro de validação nos campos
        examples:
          {"erro": "Todos os campos são obrigatórios"}
      500:
        description: Erro ao salvar alterações
        examples:
          {"erro": "Erro ao salvar sua alteração, tente novamente."}
    """

    dados = request.get_json()

    if any(valor in ("", None) for valor in dados.values()):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE
                formas_contato SET redesocial_nome = %s,
                redesocial_perfil = %s,
                telefone = %s,
                email = %s,
                atualizado_em = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    dados.get("redesocial_nome"),
                    dados.get("redesocial_perfil"),
                    dados.get("telefone"),
                    dados.get("email"),
                    id,
                ),
            )

            connection.commit()

        registrar_log("Forma de contato", f"ID {id} alterada com sucesso!")

        return jsonify({"sucesso": "Forma de contato alterada com sucesso!"}), 200

    except psycopg.DatabaseError as e:
        connection.rollback()
        registrar_log("Erro ao salvar a alteração", str(e))

        return jsonify({"erro": "Erro ao salvar sua alteração, tente novamente."}), 500
