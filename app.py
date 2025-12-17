"""
app.py – Ponto de entrada principal da aplicação Flask

Este módulo contém a configuração inicial da API Flask, carregamento de configurações,
registro de blueprints e setup das extensões como JWT e CORS.
"""

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

# Importa os blueprints das rotas
from controllers.contatos import contatos_bp
from controllers.cloudinaryapi import cloudinary_bp
from controllers.auth import auth_bp
from controllers.formas_contato import formas_contato_bp


def create_app(config_class=Config):
    """
    Cria e configura a instância principal da aplicação Flask.

    Args:
        config_class (class): Classe de configuração a ser usada (padrão: Config).

    Returns:
        Flask: Instância configurada da aplicação Flask.
    """
    app = Flask(__name__)

    # Carrega as configurações da aplicação
    app.config.from_object(config_class)

    # Inicializa extensões com a aplicação
    jwt = JWTManager()
    mail = Mail()

    # Define origens permitidas para requisições CORS
    allowed_origins = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://portfolio-fotografo.vercel.app",
    ]

    # Configura CORS com políticas específicas para rotas sob /api/*
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allowed_origins,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
        supports_credentials=True,
    )

    # Inicializa extensões com a aplicação
    jwt.init_app(app)
    mail.init_app(app)

    # Callback que verifica se o token está na denylist (lista negra)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """
        Verifica se o token atual está na lista negra de tokens revogados.

        Esta função é chamada automaticamente pelo Flask-JWT-Extended antes de cada
        acesso a uma rota protegida.

        Args:
            jwt_header (dict): Cabeçalho do token JWT.
            jwt_payload (dict): Conteúdo decodificado do token.

        Returns:
            bool: True se o token estiver na denylist, False caso contrário.
        """
        jti = jwt_payload["jti"]

        try:
            from database.database import get_cursor

            with get_cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM tokens_denylist WHERE token_jti = %s", (jti,)
                )
                token_denylistado = cur.fetchone()

            return token_denylistado is not None

        except Exception as e:
            print(f"Erro ao verificar denylist: {e}")
            # Em caso de erro no banco, considera o token válido para não quebrar o sistema
            return False

    # Callback para token revogado
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """
        Retorna resposta personalizada quando um token revogado tenta acessar uma rota protegida.

        Returns:
            tuple: Resposta JSON e código HTTP 401 Unauthorized.
        """
        return (
            jsonify(
                {
                    "erro": "Token foi invalidado. Faça login novamente.",
                    "codigo": "TOKEN_REVOGADO",
                }
            ),
            401,
        )

    # Callback para token expirado
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        Retorna resposta personalizada quando o token JWT expirou.

        Returns:
            tuple: Resposta JSON e código HTTP 401 Unauthorized.
        """
        return (
            jsonify(
                {
                    "erro": "Token expirado. Faça login novamente.",
                    "codigo": "TOKEN_EXPIRADO",
                }
            ),
            401,
        )

    # Callback para token inválido
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        Retorna resposta personalizada quando o token é inválido ou malformado.

        Args:
            error (str): Mensagem de erro do token inválido.

        Returns:
            tuple: Resposta JSON e código HTTP 401 Unauthorized.
        """
        print(error)
        return (
            jsonify(
                {
                    "erro": f"Token inválido. {error}",
                    "codigo": "TOKEN_INVALIDO",
                }
            ),
            401,
        )

    # Callback para token ausente
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """
        Retorna resposta personalizada quando nenhum token foi fornecido.

        Args:
            error (str): Mensagem de erro sobre token ausente.

        Returns:
            tuple: Resposta JSON e código HTTP 401 Unauthorized.
        """
        return (
            jsonify(
                {
                    "erro": f"Token de acesso necessário. {error}",
                    "codigo": "TOKEN_NECESSARIO",
                }
            ),
            401,
        )

    # Rota raiz da API
    @app.route("/")
    def home():
        """
        Rota inicial da API — apenas confirma que a aplicação está rodando.

        Returns:
            str: Mensagem simples de saúde/status.
        """
        return "Olá, estou online!"

    # Registro dos blueprints com prefixos de URL
    app.register_blueprint(contatos_bp, url_prefix="/api/contatos")
    app.register_blueprint(cloudinary_bp, url_prefix="/api/cloudinary")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(formas_contato_bp, url_prefix="/api/formas-contato")

    return app


# Cria a instância da aplicação
app = create_app()

# Executa o servidor apenas se o script for executado diretamente
if __name__ == "__main__":
    app.run(debug=app.config["FLASK_DEBUG"])
