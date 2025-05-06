from flask import Blueprint, jsonify, request
from database.database import connection, get_cursor
import psycopg
from services.logs import registrar_log
from flask_jwt_extended import jwt_required
from datetime import datetime
import re

contatos_bp = Blueprint("contatos", __name__)


@contatos_bp.route("", methods=["POST"])
def inserir_contato():
    """
    Endpoint público para inserção de um novo contato via formulário.
    Valida os campos obrigatórios antes de persistir os dados no banco.
    """

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
        # padroniza o nome (primeira letra maiúscula, resto minúscula)
        nome_padronizado = novo_contato.get("nome", "").strip().title()

        # Remove formatação do telefone e valida
        telefone = (
            novo_contato.get("telefone", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )
        if telefone and len(telefone) < 10:
            return jsonify({"erro": "Telefone inválido"}), 400

        # padroniza email em minúsculas
        email = novo_contato.get("email", "").strip().lower()

        # Persistência dos dados no banco
        with get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO contatos (nome, telefone, email, mensagem)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    nome_padronizado,
                    telefone if telefone else None,
                    email if email else None,
                    novo_contato.get("mensagem", "").strip(),
                ),
            )

            contato_id = cur.fetchone()["id"]

        connection.commit()

        registrar_log("Contato Criado", f"ID {contato_id} registrado com sucesso")

        return jsonify({"sucesso": "Sua mensagem foi enviada com sucesso!"}), 201

    except psycopg.DatabaseError as e:
        connection.rollback()
        registrar_log("Erro ao Salvar Contato", str(e))

        return (
            jsonify(
                {"erro": "Sua mensagem não foi entregue, tente novamente, por favor!"}
            ),
            500,
        )


@contatos_bp.route("", methods=["GET"])
@jwt_required()
def listar_contatos():
    """
    Endpoint protegido para listagem de todos os contatos cadastrados.
    Requer autenticação via token JWT.
    Parâmetros:
    - pagina: Número da página (padrão: 1)
    - por_pagina: Itens por página (padrão: 5)
    Retorna a data formatada em dois formatos:
    - data_envio: Mantém o formato original (para compatibilidade)
    - data_formatada: Formato legível (DD/MM/AAAA HH:MM)
    """

    pagina = request.args.get("pagina", default=1, type=int)
    por_pagina = request.args.get("por_pagina", default=5, type=int)

    if pagina < 1:
        pagina = 1
    if por_pagina < 1 or por_pagina > 100:
        por_pagina = 5

    lista_contatos = []
    total_contatos = 0

    try:
        with get_cursor() as cur:
            # primeiro, contar o total de registros
            cur.execute("SELECT COUNT(*) as total FROM contatos")
            total_contatos = cur.fetchone()["total"]

            # calcular quantos registros pular
            offset = (pagina - 1) * por_pagina

            # buscar só os registros da pagina atual
            cur.execute(
                """ SELECT *FROM contatos
                        ORDER BY data_envio DESC
                        LIMIT %s OFFSET %s
                        """,
                (por_pagina, offset),
            )

            contatos = cur.fetchall()

            for contato in contatos:
                # formata a data para exibição amigável
                data_original = contato["data_envio"]

                # se a data já for string (gmt), converta para datetime primeiro
                if isinstance(data_original, str):
                    data_obj = datetime.strptime(
                        data_original, "%a, %d %b %Y %H:%M:%S GMT"
                    )
                else:
                    data_obj = data_original

                data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")

                lista_contatos.append(
                    {
                        "id": contato["id"],
                        "nome": contato["nome"],
                        "data_envio": contato["data_envio"],
                        "data_formatada": data_formatada,
                        "telefone": contato["telefone"],
                        "email": contato["email"],
                        "mensagem": contato["mensagem"],
                    }
                )

        registrar_log("Contatos Listados", f"Página {pagina} com {por_pagina} itens")

        # retornar dados paginados + metadados
        return (
            jsonify(
                {
                    "dados": lista_contatos,
                    "pagina": pagina,
                    "por_pagina": por_pagina,
                    "total": total_contatos,
                    "total_paginas": (total_contatos + por_pagina - 1) // por_pagina,
                }
            ),
            200,
        )

    except psycopg.DatabaseError as e:
        registrar_log("Erro ao Listar Contatos", str(e))
        return jsonify({"erro": "Erro ao buscar contatos"}), 500
