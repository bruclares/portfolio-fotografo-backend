from flask import Blueprint, jsonify, request
from database.database import connection, get_cursor
import psycopg
from services.logs import registrar_log
from flask_jwt_extended import jwt_required

formas_contato_bp = Blueprint("formas_contato", __name__)


@formas_contato_bp.route("", methods=["GET"])
def listar_formas_contato():
    """
    Lista todas as formas de contato públicas do fotógrafo
    """

    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM formas_contato")
            resultados = cur.fetchone()
            # print(resultados)

            # lista = {
            #         "id": resultados["id"],
            #         "redesocial_nome": resultados["redesocial_nome"],
            #         "redesocial_perfil": resultados["redesocial_perfil"],
            #         "email": resultados["email"],
            #         "telefone": resultados["telefone"],
            #     }

        registrar_log("Formas de Contato Listadas", "Consulta realizada com sucesso")

        return jsonify(resultados), 200

    except psycopg.DatabaseError as e:
        connection.rollback()
        registrar_log("Erro ao Listar Formas de Contato", str(e))
        return jsonify({"erro": "Erro ao buscar formas de contato"}), 500


@formas_contato_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_forma_contato(id):
    """
    Atualiza uma forma de contao do fotográfo por id
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
