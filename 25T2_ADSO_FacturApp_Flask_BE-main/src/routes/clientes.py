from flask import Blueprint, request, jsonify
from src.models.clientes import Clientes
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

clientes_bp = Blueprint('clientes', __name__)


# ==================================
# CREAR CLIENTE
# ==================================

@token_required
@clientes_bp.route('/', methods=['POST'])
def create_cliente():

    data = request.get_json()

    cliente = Clientes(
        documento=data.get('documento'),
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        telefono=data.get('telefono'),
        email=data.get('email')
    )

    if not cliente.documento:
        return jsonify({'message': 'El documento es obligatorio'}), 400

    if not cliente.nombre:
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    if not cliente.direccion:
        return jsonify({'message': 'La dirección es obligatoria'}), 400

    if not cliente.telefono:
        return jsonify({'message': 'El teléfono es obligatorio'}), 400

    if not cliente.email:
        return jsonify({'message': 'El correo es obligatorio'}), 400

    try:
        cliente.save()
        return jsonify({
            'message': 'Cliente creado exitosamente'
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': 'Error al crear el cliente',
            'error': str(e)
        }), 500


# ==================================
# LISTAR CLIENTES
# ==================================

def serialize_cliente(cliente):
    return {
        "id": cliente.id,
        "documento": cliente.documento,
        "nombre": cliente.nombre,
        "direccion": cliente.direccion,
        "telefono": cliente.telefono,
        "email": cliente.email
    }


@token_required
@clientes_bp.route('/', methods=['GET'])
def get_clientes():
    query = session.query(Clientes)
    return paginate_response(query, serialize_cliente)


# ==================================
# BUSCAR CLIENTE POR ID
# ==================================

@token_required
@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente is None:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    return jsonify({
        "id": cliente.id,
        "documento": cliente.documento,
        "nombre": cliente.nombre,
        "direccion": cliente.direccion,
        "telefono": cliente.telefono,
        "email": cliente.email
    }), 200


# ==================================
# ACTUALIZAR CLIENTE
# ==================================

@token_required
@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente is None:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    data = request.get_json()

    cliente.documento = data.get(
        'documento',
        cliente.documento
    )

    cliente.nombre = data.get(
        'nombre',
        cliente.nombre
    )

    cliente.direccion = data.get(
        'direccion',
        cliente.direccion
    )

    cliente.telefono = data.get(
        'telefono',
        cliente.telefono
    )

    cliente.email = data.get(
        'email',
        cliente.email
    )

    try:
        session.commit()

        return jsonify({
            'message': 'Cliente actualizado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el cliente',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR CLIENTE
# ==================================

@token_required
@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente is None:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    try:
        cliente.delete()

        return jsonify({
            'message': 'Cliente eliminado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar el cliente',
            'error': str(e)
        }), 500