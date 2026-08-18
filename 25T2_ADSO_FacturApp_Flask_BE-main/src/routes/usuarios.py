from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from src.models import session
from src.routes import paginate_response
from src.auth import hash_password, verify_password, generate_token, token_required

usuarios_bp = Blueprint('usuarios', __name__)


# ==================================
# LOGIN
# ==================================

@usuarios_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Datos requeridos'}), 400

    usuario_nombre = data.get('usuario')
    password = data.get('password')

    if not usuario_nombre or not password:
        return jsonify({'message': 'Usuario y contraseña son obligatorios'}), 400

    usuario = session.query(Usuarios).filter_by(usuario=usuario_nombre).first()

    if usuario is None:
        return jsonify({'message': 'Credenciales inválidas'}), 401

    if not verify_password(password, usuario.password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = generate_token(usuario.id, usuario.rol)

    return jsonify({
        'access_token': token,
        'usuario': {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "usuario": usuario.usuario,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "telefono": usuario.telefono
        }
    }), 200


# ==================================
# CREAR USUARIO (público)
# ==================================

@usuarios_bp.route('/', methods=['POST'])
def create_usuario():

    data = request.get_json()

    usuario = Usuarios(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        usuario=data.get('usuario'),
        correo=data.get('correo'),
        password=hash_password(data.get('password')),
        rol=data.get('rol'),
        telefono=data.get('telefono')
    )

    if not usuario.nombre:
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not usuario.apellido:
        return jsonify({
            'message': 'El apellido es obligatorio'
        }), 400

    if not usuario.usuario:
        return jsonify({
            'message': 'El usuario es obligatorio'
        }), 400

    if not usuario.correo:
        return jsonify({
            'message': 'El correo es obligatorio'
        }), 400

    if not usuario.password:
        return jsonify({
            'message': 'La contraseña es obligatoria'
        }), 400

    if not usuario.rol:
        return jsonify({
            'message': 'El rol es obligatorio'
        }), 400

    try:
        usuario.save()

        return jsonify({
            'message': 'Usuario creado exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear el usuario',
            'error': str(e)
        }), 500


# ==================================
# LISTAR USUARIOS
# ==================================

def serialize_usuario(usuario):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "usuario": usuario.usuario,
        "correo": usuario.correo,
        "rol": usuario.rol,
        "telefono": usuario.telefono
    }


@token_required
@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    query = session.query(Usuarios)
    return paginate_response(query, serialize_usuario)


# ==================================
# BUSCAR USUARIO POR ID
# ==================================

@token_required
@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if usuario is None:
        return jsonify({
            'message': 'Usuario no encontrado'
        }), 404

    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "usuario": usuario.usuario,
        "correo": usuario.correo,
        "rol": usuario.rol,
        "telefono": usuario.telefono
    }), 200


# ==================================
# ACTUALIZAR USUARIO
# ==================================

@token_required
@usuarios_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if usuario is None:
        return jsonify({
            'message': 'Usuario no encontrado'
        }), 404

    data = request.get_json()

    usuario.nombre = data.get(
        'nombre',
        usuario.nombre
    )

    usuario.apellido = data.get(
        'apellido',
        usuario.apellido
    )

    usuario.usuario = data.get(
        'usuario',
        usuario.usuario
    )

    usuario.correo = data.get(
        'correo',
        usuario.correo
    )

    nuevo_password = data.get('password')
    if nuevo_password:
        usuario.password = hash_password(nuevo_password)

    usuario.rol = data.get(
        'rol',
        usuario.rol
    )

    usuario.telefono = data.get(
        'telefono',
        usuario.telefono
    )

    if not usuario.nombre:
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not usuario.apellido:
        return jsonify({
            'message': 'El apellido es obligatorio'
        }), 400

    if not usuario.usuario:
        return jsonify({
            'message': 'El usuario es obligatorio'
        }), 400

    if not usuario.correo:
        return jsonify({
            'message': 'El correo es obligatorio'
        }), 400

    if not usuario.password:
        return jsonify({
            'message': 'La contraseña es obligatoria'
        }), 400

    if not usuario.rol:
        return jsonify({
            'message': 'El rol es obligatorio'
        }), 400

    try:
        session.commit()

        return jsonify({
            'message': 'Usuario actualizado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el usuario',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR USUARIO
# ==================================

@token_required
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if usuario is None:
        return jsonify({
            'message': 'Usuario no encontrado'
        }), 404

    try:
        usuario.delete()

        return jsonify({
            'message': 'Usuario eliminado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar el usuario',
            'error': str(e)
        }), 500