from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from controllers.contatos import contatos_bp
from controllers.cloudinaryapi import cloudinary_bp
from controllers.auth import auth_bp


load_dotenv()

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)


@app.route("/")
def home():
    return "Olá, estou online!"


app.register_blueprint(contatos_bp, url_prefix="/api/contatos")
app.register_blueprint(cloudinary_bp, url_prefix="/api/cloudinary")
app.register_blueprint(auth_bp, url_prefix="/api/auth")


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)


# python app.py
