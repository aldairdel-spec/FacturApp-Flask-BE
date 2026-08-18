from flask import Blueprint, request, jsonify
from src.models.facturas import Facturas
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

facturas_bp = Blueprint('facturas', __name__)


# ==================================
# CREAR FACTURA
# ==================================

@token_required
@facturas_bp.route('/', methods=['POST'])
def create_factura():

    data = request.get_json()

    factura = Facturas(
        numero_factura=data.get('numero_factura'),
        cliente_id=data.get('cliente_id'),
        vendedor_id=data.get('vendedor_id'),
        subtotal=data.get('subtotal'),
        iva=data.get('iva'),
        total=data.get('total')
    )

    if not factura.numero_factura:
        return jsonify({
            'message': 'El número de factura es obligatorio'
        }), 400

    if factura.cliente_id is None:
        return jsonify({
            'message': 'El cliente es obligatorio'
        }), 400

    if factura.vendedor_id is None:
        return jsonify({
            'message': 'El vendedor es obligatorio'
        }), 400

    try:
        factura.subtotal = float(factura.subtotal)
        factura.iva = float(factura.iva)
        factura.total = float(factura.total)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'Subtotal, IVA y Total deben ser numéricos'
        }), 400

    try:
        factura.save()

        return jsonify({
            'message': 'Factura creada exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear la factura',
            'error': str(e)
        }), 500


# ==================================
# LISTAR FACTURAS
# ==================================

def serialize_factura(factura):
    return {
        "id": factura.id,
        "numero_factura": factura.numero_factura,
        "cliente_id": factura.cliente_id,
        "vendedor_id": factura.vendedor_id,
        "subtotal": float(factura.subtotal),
        "iva": float(factura.iva),
        "total": float(factura.total)
    }


@token_required
@facturas_bp.route('/', methods=['GET'])
def get_facturas():
    query = session.query(Facturas)
    return paginate_response(query, serialize_factura)


# ==================================
# BUSCAR FACTURA POR ID
# ==================================

@token_required
@facturas_bp.route('/<int:id>', methods=['GET'])
def get_factura(id):

    factura = Facturas.get_by_id(id)

    if factura is None:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    return jsonify({
        "id": factura.id,
        "numero_factura": factura.numero_factura,
        "cliente_id": factura.cliente_id,
        "vendedor_id": factura.vendedor_id,
        "subtotal": float(factura.subtotal),
        "iva": float(factura.iva),
        "total": float(factura.total)
    }), 200


# ==================================
# ACTUALIZAR FACTURA
# ==================================

@token_required
@facturas_bp.route('/<int:id>', methods=['PUT'])
def update_factura(id):

    factura = Facturas.get_by_id(id)

    if factura is None:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    data = request.get_json()

    factura.numero_factura = data.get(
        'numero_factura',
        factura.numero_factura
    )

    factura.cliente_id = data.get(
        'cliente_id',
        factura.cliente_id
    )

    factura.vendedor_id = data.get(
        'vendedor_id',
        factura.vendedor_id
    )

    factura.subtotal = data.get(
        'subtotal',
        factura.subtotal
    )

    factura.iva = data.get(
        'iva',
        factura.iva
    )

    factura.total = data.get(
        'total',
        factura.total
    )

    if not factura.numero_factura:
        return jsonify({
            'message': 'El número de factura es obligatorio'
        }), 400

    if factura.cliente_id is None:
        return jsonify({
            'message': 'El cliente es obligatorio'
        }), 400

    if factura.vendedor_id is None:
        return jsonify({
            'message': 'El vendedor es obligatorio'
        }), 400

    try:
        factura.subtotal = float(factura.subtotal)
        factura.iva = float(factura.iva)
        factura.total = float(factura.total)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'Subtotal, IVA y Total deben ser numéricos'
        }), 400

    try:
        session.commit()

        return jsonify({
            'message': 'Factura actualizada correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar la factura',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR FACTURA
# ==================================

@token_required
@facturas_bp.route('/<int:id>', methods=['DELETE'])
def delete_factura(id):

    factura = Facturas.get_by_id(id)

    if factura is None:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    try:
        factura.delete()

        return jsonify({
            'message': 'Factura eliminada correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar la factura',
            'error': str(e)
        }), 500 