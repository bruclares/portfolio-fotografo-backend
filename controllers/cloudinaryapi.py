from flask import Blueprint, jsonify, request
import cloudinary
import cloudinary.api
import cloudinary.uploader
import os
from dotenv import load_dotenv  # Para carregar as variáveis de ambiente

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

cloudinary_bp = Blueprint('cloudinaryapi', __name__)

@cloudinary_bp.route('/fotos', methods=['POST'])
def get_fotos():
    try:
        # Obtém o corpo da requisição
        dados_requisicao = request.get_json()
        next_cursor = dados_requisicao.get('next_cursor') if dados_requisicao else None
        pasta = dados_requisicao.get('pasta') if dados_requisicao else None
        
        # Verifica se a pasta foi fornecida
        if not pasta:
            return jsonify({"erro": "O parâmetro 'pasta' é obrigatório"}), 400
        
        # Configuração do Cloudinary com valores do .env
        cloudinary.config(
            cloud_name = os.getenv("CLOUD_NAME"),
            api_key=os.getenv("API_KEY"),
            api_secret=os.getenv("API_SECRET")
        )
        
        # Opções para a API do Cloudinary - Corpo da requisição ao Cloudinary
        options = {
            "asset_folder": pasta, # Usa a pasta recebida do frontend
            "max_results": 6
        }
        
        # Adiciona o cursor à próxima página, se disponível
        if next_cursor:
            options['next_cursor'] = next_cursor
            
        # Faz a requisição ao Cloudinary
        response = cloudinary.api.resources_by_asset_folder(**options)
        
        # Prepara a resposta
        resposta = {
            "fotos": [],
            "proxima_pagina": response.get('next_cursor')
        }
        
        # Processa as fotos retornadas
        for resource in response.get('resources', []):
            foto = {
                'url': resource['url'],
                'nome': resource['public_id'],
            }
            resposta['fotos'].append(foto)
            
        return jsonify(resposta)
        
    except Exception as e:
        print(f"Erro ao buscar fotos: {str(e)}")
        return jsonify({"erro": str(e)}), 500