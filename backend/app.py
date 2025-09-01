import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv  # ← Import para ler .env
from blueprints.cirurgias import cirurgias_bp
from blueprints.auth import auth_bp

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Define a chave secreta pegando do .env
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

@app.route('/')
def home():
    return "API funcionando!"

# Registrar blueprints
app.register_blueprint(cirurgias_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(
        host='10.14.1.172',
        port=8080,
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )
