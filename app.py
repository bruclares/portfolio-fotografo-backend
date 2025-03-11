from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary

from controllers.contatos import contatos_bp
from controllers.cloudinaryapi import cloudinary_bp

load_dotenv()

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "Olá, estou online!"


app.register_blueprint(contatos_bp, url_prefix="/api/contatos")
app.register_blueprint(cloudinary_bp, url_prefix="/api/cloudinary")


if __name__ == "__main__":
    app.run(debug=True)
