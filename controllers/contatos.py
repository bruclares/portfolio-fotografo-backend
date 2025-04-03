from flask import Blueprint, jsonify, request
from database.database import connection, get_cursor
import psycopg
from services.logs import registrar_log

contatos_bp = Blueprint("contatos", __name__)


@contatos_bp.route("/", methods=["POST"])
def inserir_contato():
    novo_contato = request.get_json()

    if not novo_contato:
        registrar_log("Erro de Validação", "Nenhum dado recebido")
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    if not novo_contato.get("nome"):
        registrar_log("Erro de Validação", "Nome obrigatório ausente")
        return jsonify({"erro": "O nome é obrigatório"}), 400

    if not novo_contato.get("mensagem"):
        registrar_log("Erro de Validação", "Mensagem obrigatória ausente")
        return jsonify({"erro": "A mensagem é obrigatória"}), 400

    if not novo_contato.get("telefone") and not novo_contato.get("email"):
        registrar_log("Erro de Validação", "Nenhum meio de contato fornecido")
        return jsonify({"erro": "Ao menos um contato é obrigatório"}), 400

    try:
        with get_cursor() as cur:
            cur.execute(
                """INSERT INTO contatos (nome,
                telefone, email, mensagem)
                VALUES(%s, %s, %s, %s) RETURNING id
                """,
                (
                    novo_contato.get("nome"),
                    novo_contato.get("telefone"),
                    novo_contato.get("email"),
                    novo_contato.get("mensagem"),
                ),
            )

            contato_id = cur.fetchone()["id"]

        connection.commit()

        registrar_log("Contato Criado", f"ID {contato_id} registrado com sucesso")

        return jsonify({"sucesso": "Sua mensagem foi enviado com sucesso!"}), 201

    except psycopg.DatabaseError as e:
        connection.rollback()

        registrar_log("Erro ao Salvar Contato", str(e))

        return (
            jsonify(
                {"erro": "Sua mensagem não foi entregue, tente novamente, por favor!"}
            ),
            500,
        )
