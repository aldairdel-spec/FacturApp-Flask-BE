from flask import Blueprint, request, jsonify
from src.models.metodos_pago import MetodosPago
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

metodos_pago_bp = Blueprint('metodos_pago', __name__)


# ==================================
# CREAR METODO DE PAGO
# ==================================

@token_required
@metodos_pago_bp.route('/', methods=['POST'])
def create_metodo_pago():

    data = request.get_json()

    metodo = MetodosPago(
        nombre=data.get('nombre')
    )

    if not metodo.nombre:
        return jsonify({
            'message': 'El nombre del método de pago es obligatorio'
        }), 400

    try:
        metodo.save()

        return jsonify({
            'message': 'Método de pago creado exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear el método de pago',
            'error': str(e)
        }), 500


# ==================================
# LISTAR METODOS DE PAGO
# ==================================

def serialize_metodo_pago(metodo):
    return {
        "id": metodo.id,
        "nombre": metodo.nombre
    }


@token_required
@metodos_pago_bp.route('/', methods=['GET'])
def get_metodos_pago():
    query = session.query(MetodosPago)
    return paginate_response(query, serialize_metodo_pago)


# ==================================
# BUSCAR METODO POR ID
# ==================================

@token_required
@metodos_pago_bp.route('/<int:id>', methods=['GET'])
def get_metodo_pago(id):

    metodo = MetodosPago.get_by_id(id)

    if metodo is None:
        return jsonify({
            "message": "Método de pago no encontrado"
        }), 404

    return jsonify({
        "id": metodo.id,
        "nombre": metodo.nombre
    }), 200


# ==================================
# ACTUALIZAR METODO DE PAGO
# ==================================

@token_required
@metodos_pago_bp.route('/<int:id>', methods=['PUT'])
def update_metodo_pago(id):

    metodo = MetodosPago.get_by_id(id)

    if metodo is None:
        return jsonify({
            "message": "Método de pago no encontrado"
        }), 404

    data = request.get_json()

    metodo.nombre = data.get(
        'nombre',
        metodo.nombre
    )

    if not metodo.nombre:
        return jsonify({
            'message': 'El nombre del método de pago es obligatorio'
        }), 400

    try:
        session.commit()

        return jsonify({
            "message": "Método de pago actualizado correctamente"
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el método de pago',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR METODO DE PAGO
# ==================================

@token_required
@metodos_pago_bp.route('/<int:id>', methods=['DELETE'])
def delete_metodo_pago(id):

    metodo = MetodosPago.get_by_id(id)

    if metodo is None:
        return jsonify({
            "message": "Método de pago no encontrado"
        }), 404

    try:
        metodo.delete()

        return jsonify({
            "message": "Método de pago eliminado correctamente"
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar el método de pago',
            'error': str(e)
        }), 500 