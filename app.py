from flask import Flask
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
jwt = JWTManager()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Carrega configurações
    app.config.from_object(config_class)

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
