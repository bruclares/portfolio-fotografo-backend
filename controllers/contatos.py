from flask import Blueprint, jsonify, request
from database import get_db
import psycopg

contatos_bp = Blueprint("contatos", __name__)

@contatos_bp.route("/", methods=["POST"])
def inserir_contato():
    novo_contato = request.get_json()

    if not novo_contato:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    if not novo_contato.get("nome"):
        return jsonify({"erro": "O nome é obrigatório"}), 400
    
    if not novo_contato.get("mensagem"):
        return jsonify({"erro": "A mensagem é obrigatória"}), 400
    
    if not novo_contato.get("telefone") and not novo_contato.get("email"):
        return jsonify({"erro": "Ao menos um contato é obrigatório"}), 400
    
    try:
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''INSERT INTO contatos (nome,
                    telefone, email, mensagem) VALUES(%s, %s, %s, %s)''',
                    (novo_contato.get("nome"), novo_contato.get("telefone"),
                        novo_contato.get("email"), novo_contato.get("mensagem")))
            
    except psycopg.DatabaseError:
        return jsonify({"erro": "Sua mensagem não foi entregue, tente novamente, por favor!"})
    
    return jsonify({"sucesso": "Sua mensagem foi enviada com sucesso!"})

    