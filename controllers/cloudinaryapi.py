from flask import Blueprint, jsonify, request, current_app
import cloudinary
import cloudinary.api
from dotenv import load_dotenv
from services.logs import registrar_log

load_dotenv()

cloudinary_bp = Blueprint("cloudinaryapi", __name__)


@cloudinary_bp.route("/fotos", methods=["POST"])
def get_fotos():
    """
    Recupera uma lista de fotos de uma pasta específica no Cloudinary.

    ---
    tags:
      - Galeria de Fotos (Cloudinary)
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            pasta:
              type: string
              description: Nome da pasta no Cloudinary
              example: "galeria/fotos"
            next_cursor:
              type: string
              description: Cursor para paginação (opcional)
              example: "1234567890ABCDEF"
        required:
          - pasta
    responses:
      200:
        description: Lista de fotos recuperada com sucesso
        schema:
          type: object
          properties:
            fotos:
              type: array
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: URL pública da imagem
                  nome:
                    type: string
                    description: Identificador único da imagem
            proxima_pagina:
              type: string
              description: Cursor para próxima página (se houver)
      400:
        description: Parâmetro obrigatório ausente
        examples:
          {"erro": "O parâmetro 'pasta' é obrigatório"}
      500:
        description: Erro interno ao buscar fotos
        examples:
          {"erro": "Erro ao buscar fotos, tente novamente mais tarde!"}
    """

    try:
        dados_requisicao = request.get_json()
        next_cursor = dados_requisicao.get("next_cursor") if dados_requisicao else None
        pasta = dados_requisicao.get("pasta") if dados_requisicao else None

        if not pasta:
            registrar_log("Erro de Validação", "O parâmetro 'pasta' não foi informado")
            return jsonify({"erro": "O parâmetro 'pasta' é obrigatório"}), 400

        registrar_log(
            "Requisição de Galeria", f"Usuário solicitou fotos da pasta '{pasta}'"
        )

        # Configura credenciais da API do Cloudinary via variáveis de ambiente
        cloudinary.config(
            cloud_name=current_app.config["CLOUD_NAME"],
            api_key=current_app.config["API_KEY"],
            api_secret=current_app.config["API_SECRET"],
            secure=current_app.config.get("CLOUDINARY_SECURE", True),
        )

        # Monta os parâmetros da requisição
        options = {
            "asset_folder": pasta,
            "max_results": 18,  # Limita a quantidade de fotos retornadas
        }

        # Adiciona paginação se o cursor estiver presente
        if next_cursor:
            options["next_cursor"] = next_cursor

        # Faz a requisição à API do Cloudinary
        response = cloudinary.api.resources_by_asset_folder(**options)

        # Monta o payload da resposta com as fotos formatadas
        resposta = {"fotos": [], "proxima_pagina": response.get("next_cursor")}

        for resource in response.get("resources", []):
            url = resource["url"]
            if url.startswith("http://"):
                url = url.replace("http://", "https://", 1)

            foto = {
                "url": url,
                "nome": resource["public_id"],
            }
            resposta["fotos"].append(foto)

        registrar_log(
            "Galeria Recuperada",
            f"{len(resposta['fotos'])} fotos retornadas da pasta '{pasta}'",
        )

        return jsonify(resposta)

    except Exception as e:
        registrar_log("Erro ao Buscar Fotos", str(e))
        return (
            jsonify({"erro": "Erro ao buscar fotos, tente novamente mais tarde!"}),
            500,
        )
