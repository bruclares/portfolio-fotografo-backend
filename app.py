from flask import Flask
from controllers.contatos import contatos_bp
from flask_cors import CORS

# python app.py

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "Olá, estou online!"


app.register_blueprint(contatos_bp, url_prefix="/api/contatos")


if __name__ == "__main__":
    app.run(debug=True)
