from flask import Blueprint, request, jsonify, current_app
from ldap3 import Server, Connection, ALL, NTLM
import jwt
import datetime
import json
from pathlib import Path
from io import BytesIO
import base64
import pyotp
import qrcode

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Lista negra para tokens invalidados (logout)
blacklist = set()
usuarios_permitidos = ['Eriston', 'Patricia.rodrigues', 'Danilo.valim', 'Paulo.bastos', 'Joab.marques']

MFA_FILE = Path(__file__).resolve().parent.parent / 'mfa_secrets.json'


def load_mfa_secrets():
    if MFA_FILE.exists():
        with open(MFA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_mfa_secrets(data):
    with open(MFA_FILE, 'w') as f:
        json.dump(data, f)

def gerar_token(username, secret_key):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verificar_token(token):
    try:
        if token in blacklist:
            return 'Token inválido (logout realizado)'
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expirado'
    except jwt.InvalidTokenError:
        return 'Token inválido'

# --- Rotas de Autenticação ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"erro": "corpo JSON ausente ou inválido"}), 400
    username = data.get('username')
    password = data.get('password')
    token_2fa = data.get('token_2fa')

    if not username or not password:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    try:
        server = Server('hu.local', get_info=ALL)
        conn = Connection(
            server,
            user=f"hu.local\\{username}",
            password=password,
            authentication=NTLM,
            auto_bind=True,
        )
        if username not in usuarios_permitidos:
            conn.unbind()
            return jsonify({"erro": "Acesso negado"}), 403
        conn.unbind()
    except Exception as e:
        return jsonify({"erro": "Falha na autenticação", "detalhes": str(e)}), 401

    secrets = load_mfa_secrets()
    secret = secrets.get(username)
    if not secret:
        return jsonify({"erro": "MFA não configurado"}), 403

    if not token_2fa:
        return jsonify({"mfaRequired": True}), 200

    if not pyotp.TOTP(secret).verify(token_2fa):
        return jsonify({"erro": "Código 2FA inválido"}), 401

    token = gerar_token(username, current_app.config['SECRET_KEY'])
    return jsonify({"token": token, "mensagem": "Autenticação bem-sucedida"}), 200


@auth_bp.route('/mfa/setup', methods=['GET'])
def mfa_setup():
    username = request.args.get('username')
    if not username:
        return jsonify({"erro": "username é obrigatório"}), 400
    if username not in usuarios_permitidos:
        return jsonify({"erro": "Acesso negado"}), 403
    secret = pyotp.random_base32()
    secrets = load_mfa_secrets()
    secrets[username] = secret
    save_mfa_secrets(secrets)
    uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name="Mapa Cirurgico")
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{img_b64}"
    return jsonify({"qr_code": data_url}), 200
@auth_bp.route('/validate', methods=['POST'])
def validate():
    token = request.json.get('token')
    if not token:
        return jsonify({"erro": "Token é obrigatório"}), 400

    resultado = verificar_token(token)
    if resultado in ['Token expirado', 'Token inválido', 'Token inválido (logout realizado)']:
        return jsonify({"erro": resultado}), 401

    return jsonify({"mensagem": "Token válido", "username": resultado}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.json.get('token')
    if not token:
        return jsonify({"erro": "Token é obrigatório"}), 400

    blacklist.add(token)
    return jsonify({"mensagem": "Logout realizado com sucesso"}), 200
