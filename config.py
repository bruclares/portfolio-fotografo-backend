import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configurações básicas do Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Configurações de e-mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL") == "True"
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_SALT = os.getenv("MAIL_SALT")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Cloudinary
    CLOUD_NAME = os.getenv("CLOUD_NAME")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
