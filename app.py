from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

# Importa os blueprints
from controllers.contatos import contatos_bp
from controllers.cloudinaryapi import cloudinary_bp
from controllers.auth import auth_bp
from controllers.formas_contato import formas_contato_bp

# Cria as extensões (sem inicializar)
# jwt = JWTManager()
# mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Carrega configurações
    app.config.from_object(config_class)

    jwt = JWTManager()
    mail = Mail()

    allowed_origins = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://portfolio-fotografo.vercel.app",
    ]

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

    # Inicializa as extensões COM a app
    jwt.init_app(app)
    mail.init_app(app)

    # Configurações da DENYLIST
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """
        Verifica se o token está na denylist a cada requisição protegida.
        Esta função é chamada automaticamente pelo Flask-JWT-Extended
        """

        # manter esse import dentro da função para evitar import circular
        from database.database import get_cursor

        jti = jwt_payload["jti"]

        try:
            with get_cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM tokens_denylist WHERE token_jti = %s", (jti,)
                )
                token_denylistado = cur.fetchone()

            # Retorna True se o token estiver na denylist
            return token_denylistado is not None

        except Exception as e:
            print(f"Erro ao verificar denylist: {e}")
            # em caso de erro no banco, considera o token válido para não quebrar o sistema
            return False

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """
        Resposta personalizada quando um token denylistado
        tenta acessar uma rota protegida.
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

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        Resposta quando token expirou
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

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        Resposta quando token é inválido/malformado
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

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """
        Resposta quando token não foi fornecido
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

    # Rotas
    @app.route("/")
    def home():
        return "Olá, estou online!"

    # Registra blueprints
    app.register_blueprint(contatos_bp, url_prefix="/api/contatos")
    app.register_blueprint(cloudinary_bp, url_prefix="/api/cloudinary")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(formas_contato_bp, url_prefix="/api/formas-contato")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["FLASK_DEBUG"])
