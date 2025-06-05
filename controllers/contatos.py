from flask import Blueprint, jsonify, request
from database.database import connection, get_cursor
import psycopg
from services.logs import registrar_log
from flask_jwt_extended import jwt_required
from datetime import datetime

contatos_bp = Blueprint("contatos", __name__)


@contatos_bp.route("", methods=["POST"])
def inserir_contato():
    """
    Cria um novo contato via formulário.

    ---
    tags:
      - Contatos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome completo do remetente
              example: "João da Silva"
            telefone:
              type: string
              description: Telefone do remetente (opcional)
              example: "(11) 98765-4321"
            email:
              type: string
              description: E-mail do remetente (opcional)
              example: "joao@email.com"
            mensagem:
              type: string
              description: Mensagem enviada pelo usuário
              example: "Olá, gostaria de saber mais sobre seus serviços."
    responses:
      201:
        description: Contato criado com sucesso
        examples:
          {"sucesso": "Sua mensagem foi enviada com sucesso!"}
      400:
        description: Erro de validação nos campos obrigatórios
        examples:
          {"erro": "O nome é obrigatório"}
          {"erro": "Telefone inválido"}
          {"erro": "Ao menos um contato é obrigatório"}
      500:
        description: Erro interno ao salvar o contato
        examples:
          {"erro": "Sua mensagem não foi entregue, tente novamente, por favor!"}
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
    Lista todos os contatos cadastrados (requer autenticação).

    ---
    tags:
      - Contatos
    parameters:
      - name: pagina
        in: query
        type: integer
        default: 1
        description: Número da página de resultados
      - name: por_pagina
        in: query
        type: integer
        default: 5
        description: Quantidade de registros por página (máximo 100)
    security:
      - JWT: []
    responses:
      200:
        description: Lista paginada de contatos
        schema:
          type: object
          properties:
            dados:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  nome:
                    type: string
                  data_envio:
                    type: string
                    format: date-time
                  data_formatada:
                    type: string
                    format: date
                  telefone:
                    type: string
                  email:
                    type: string
                  mensagem:
                    type: string
            pagina:
              type: integer
            por_pagina:
              type: integer
            total:
              type: integer
            total_paginas:
              type: integer
      500:
        description: Erro ao buscar contatos
        examples:
          {"erro": "Erro ao buscar contatos"}
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
                """ SELECT * FROM contatos
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
