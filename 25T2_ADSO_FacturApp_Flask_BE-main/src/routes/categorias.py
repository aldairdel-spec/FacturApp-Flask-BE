from flask import Blueprint, request, jsonify
from src.models.categorias import Categorias
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

categorias_bp = Blueprint('categorias', __name__)


# ==================================
# CREAR CATEGORIA
# ==================================

@token_required
@categorias_bp.route('/', methods=['POST'])
def create_categoria():

    data = request.get_json()

    categoria = Categorias(
        nombre=data.get('nombre')
    )

    if not categoria.nombre:
        return jsonify({
            'message': 'El nombre de la categoría es obligatorio'
        }), 400

    try:
        categoria.save()

        return jsonify({
            'message': 'Categoría creada exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear la categoría',
            'error': str(e)
        }), 500


# ==================================
# LISTAR CATEGORIAS
# ==================================

def serialize_categoria(categoria):
    return {
        "id": categoria.id,
        "nombre": categoria.nombre
    }


@token_required
@categorias_bp.route('/', methods=['GET'])
def get_categorias():
    query = session.query(Categorias)
    return paginate_response(query, serialize_categoria)


# ==================================
# BUSCAR CATEGORIA POR ID
# ==================================

@token_required
@categorias_bp.route('/<int:id>', methods=['GET'])
def get_categoria(id):

    categoria = Categorias.get_by_id(id)

    if categoria is None:
        return jsonify({
            "message": "Categoría no encontrada"
        }), 404

    return jsonify({
        "id": categoria.id,
        "nombre": categoria.nombre
    }), 200


# ==================================
# ACTUALIZAR CATEGORIA
# ==================================

@token_required
@categorias_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):

    categoria = Categorias.get_by_id(id)

    if categoria is None:
        return jsonify({
            "message": "Categoría no encontrada"
        }), 404

    data = request.get_json()

    categoria.nombre = data.get(
        'nombre',
        categoria.nombre
    )

    if not categoria.nombre:
        return jsonify({
            'message': 'El nombre de la categoría es obligatorio'
        }), 400

    try:
        session.commit()

        return jsonify({
            "message": "Categoría actualizada correctamente"
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar la categoría',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR CATEGORIA
# ==================================

@token_required
@categorias_bp.route('/<int:id>', methods=['DELETE'])
def delete_categoria(id):

    categoria = Categorias.get_by_id(id)

    if categoria is None:
        return jsonify({
            "message": "Categoría no encontrada"
        }), 404

    try:
        categoria.delete()

        return jsonify({
            "message": "Categoría eliminada correctamente"
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar la categoría',
            'error': str(e)
        }), 500