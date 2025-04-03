from flask import Blueprint, jsonify, request
import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv
import os
from services.logs import registrar_log

load_dotenv()

cloudinary_bp = Blueprint("cloudinaryapi", __name__)


@cloudinary_bp.route("/fotos", methods=["POST"])
def get_fotos():
    try:
        # Obtém o corpo da requisição
        dados_requisicao = request.get_json()
        next_cursor = dados_requisicao.get("next_cursor") if dados_requisicao else None
        pasta = dados_requisicao.get("pasta") if dados_requisicao else None

        # Verifica se a pasta foi fornecida
        if not pasta:
            # já registra a intenção do usuário em acessar determinada pasta
            registrar_log("Erro de Validação", "O parâmetro 'pasta' não foi informado")
            return jsonify({"erro": "O parâmetro 'pasta' é obrigatório"}), 400

        registrar_log(
            "Requisição de Galeria", f"Usuário solicitou fotos da pasta '{pasta}'"
        )

        # Configuração do Cloudinary com valores do .env
        cloudinary.config(
            cloud_name=os.getenv("CLOUD_NAME"),
            api_key=os.getenv("API_KEY"),
            api_secret=os.getenv("API_SECRET"),
        )

        # Opções para a API do Cloudinary - Corpo da requisição ao Cloudinary
        options = {
            "asset_folder": pasta,  # Usa a pasta recebida do frontend
            "max_results": 18,
        }

        # Adiciona o cursor à próxima página, se disponível
        if next_cursor:
            options["next_cursor"] = next_cursor

        # Faz a requisição ao Cloudinary
        response = cloudinary.api.resources_by_asset_folder(**options)

        # Prepara a resposta
        resposta = {"fotos": [], "proxima_pagina": response.get("next_cursor")}

        # Processa as fotos retornadas
        for resource in response.get("resources", []):
            foto = {
                "url": resource["url"],
                "nome": resource["public_id"],
            }
            resposta["fotos"].append(foto)

        # log de sucesso
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
