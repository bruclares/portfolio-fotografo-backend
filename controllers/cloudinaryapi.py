from flask import Blueprint, jsonify, request, current_app
import cloudinary
import cloudinary.api
from dotenv import load_dotenv
from services.logs import registrar_log

# Carrega variáveis de ambiente do .env
load_dotenv()

# Define o blueprint da API relacionada ao Cloudinary
cloudinary_bp = Blueprint("cloudinaryapi", __name__)


@cloudinary_bp.route("/fotos", methods=["POST"])
def get_fotos():
    """
    Endpoint para recuperar imagens armazenadas em uma pasta específica no Cloudinary.
    Espera um JSON com:
        - 'pasta': nome da pasta no Cloudinary (obrigatório)
        - 'next_cursor': cursor opcional para paginação
    Retorna:
        - Lista de imagens (url e nome)
        - Cursor da próxima página (caso exista)
    """

    try:
        # Extrai os dados da requisição JSON
        dados_requisicao = request.get_json()
        next_cursor = dados_requisicao.get("next_cursor") if dados_requisicao else None
        pasta = dados_requisicao.get("pasta") if dados_requisicao else None

        # Valida presença da pasta
        if not pasta:
            registrar_log("Erro de Validação", "O parâmetro 'pasta' não foi informado")
            return jsonify({"erro": "O parâmetro 'pasta' é obrigatório"}), 400

        # Registra intenção da requisição
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

        # Log de sucesso com quantidade de fotos
        registrar_log(
            "Galeria Recuperada",
            f"{len(resposta['fotos'])} fotos retornadas da pasta '{pasta}'",
        )

        # Retorna os dados para o frontend
        return jsonify(resposta)

    except Exception as e:
        # Captura erros não previstos e registra log detalhado
        registrar_log("Erro ao Buscar Fotos", str(e))
        return (
            jsonify({"erro": "Erro ao buscar fotos, tente novamente mais tarde!"}),
            500,
        )
