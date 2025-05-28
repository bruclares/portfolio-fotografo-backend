"""
config.py – Configurações da aplicação Flask

Este módulo contém a classe base de configuração da aplicação,
com valores carregados das variáveis de ambiente (.env).

As configurações são agrupadas por categoria:
    - Flask
    - JWT
    - E-mail
    - Banco de dados
    - Cloudinary
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    """
    Classe base que contém as configurações padrão da aplicação.

    As variáveis são carregadas via `.env` usando `os.getenv()`.
    """

    # ========================
    # Configurações do Flask
    # ========================
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # ========================
    # Configurações do JWT
    # ========================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret")

    # ========================
    # Configurações de E-mail (Flask-Mail)
    # ========================
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_SALT = os.getenv("MAIL_SALT")

    # ========================
    # Configurações do Banco de Dados
    # ========================
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ========================
    # Configurações do Cloudinary
    # ========================
    CLOUD_NAME = os.getenv("CLOUD_NAME")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    CLOUDINARY_SECURE = True  # Força uso de HTTPS

    # ========================
    # Ambiente da Aplicação
    # ========================
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
