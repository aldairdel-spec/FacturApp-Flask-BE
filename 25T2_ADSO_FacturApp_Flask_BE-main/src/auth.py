import datetime
import jwt
from functools import wraps
from flask import request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from src.config import SECRET_KEY
from src.models import session
from src.models.usuarios import Usuarios


TOKEN_EXPIRATION_HOURS = 24


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


def generate_token(usuario_id, rol):
    payload = {
        "usuario_id": usuario_id,
        "rol": rol,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token de autenticación requerido'}), 401

        try:
            data = decode_token(token)
            usuario = session.query(Usuarios).filter_by(id=data['usuario_id']).first()
            if usuario is None:
                return jsonify({'message': 'Usuario no encontrado'}), 401
            g.user = usuario
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated
