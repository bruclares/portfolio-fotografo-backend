from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Importa os blueprints (rotas organizadas por funcionalidade)
from controllers.contatos import contatos_bp
from controllers.cloudinaryapi import cloudinary_bp
from controllers.auth import auth_bp

# Carrega as variáveis de ambiente definidas no arquivo .env
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)

# Habilita o CORS para permitir requisições de diferentes origens (útil para frontend separado)
CORS(app)

# Configura a chave secreta para geração e validação de tokens JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Inicializa o gerenciador de tokens JWT
jwt = JWTManager(app)


# Rota básica para verificar se o servidor está online
@app.route("/")
def home():
    return "Olá, estou online!"


# Registro das rotas organizadas por blueprint
app.register_blueprint(contatos_bp, url_prefix="/api/contatos")
app.register_blueprint(cloudinary_bp, url_prefix="/api/cloudinary")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Inicializa o servidor Flask
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)

# Para executar: python app.py
