from flask import Blueprint, request, jsonify
from src.models.detalle_factura import DetalleFactura
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

detalle_factura_bp = Blueprint('detalle_factura', __name__)


# ==================================
# CREAR DETALLE FACTURA
# ==================================

@token_required
@detalle_factura_bp.route('/', methods=['POST'])
def create_detalle_factura():

    data = request.get_json()

    detalle = DetalleFactura(
        factura_id=data.get('factura_id'),
        producto_id=data.get('producto_id'),
        cantidad=data.get('cantidad'),
        precio_unitario=data.get('precio_unitario'),
        subtotal=data.get('subtotal')
    )

    if detalle.factura_id is None:
        return jsonify({
            'message': 'La factura es obligatoria'
        }), 400

    if detalle.producto_id is None:
        return jsonify({
            'message': 'El producto es obligatorio'
        }), 400

    try:
        detalle.cantidad = int(detalle.cantidad)
        detalle.precio_unitario = float(detalle.precio_unitario)
        detalle.subtotal = float(detalle.subtotal)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'Cantidad, precio y subtotal deben ser numéricos'
        }), 400

    if detalle.cantidad <= 0:
        return jsonify({
            'message': 'La cantidad debe ser mayor que cero'
        }), 400

    if detalle.precio_unitario < 0:
        return jsonify({
            'message': 'El precio unitario no puede ser negativo'
        }), 400

    if detalle.subtotal < 0:
        return jsonify({
            'message': 'El subtotal no puede ser negativo'
        }), 400

    try:
        detalle.save()

        return jsonify({
            'message': 'Detalle de factura creado exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear el detalle',
            'error': str(e)
        }), 500


# ==================================
# LISTAR DETALLES
# ==================================

def serialize_detalle(detalle):
    return {
        "id": detalle.id,
        "factura_id": detalle.factura_id,
        "producto_id": detalle.producto_id,
        "cantidad": detalle.cantidad,
        "precio_unitario": float(detalle.precio_unitario),
        "subtotal": float(detalle.subtotal)
    }


@token_required
@detalle_factura_bp.route('/', methods=['GET'])
def get_detalles():
    query = session.query(DetalleFactura)
    return paginate_response(query, serialize_detalle)


# ==================================
# BUSCAR DETALLE POR ID
# ==================================

@token_required
@detalle_factura_bp.route('/<int:id>', methods=['GET'])
def get_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if detalle is None:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    return jsonify({
        "id": detalle.id,
        "factura_id": detalle.factura_id,
        "producto_id": detalle.producto_id,
        "cantidad": detalle.cantidad,
        "precio_unitario": float(detalle.precio_unitario),
        "subtotal": float(detalle.subtotal)
    }), 200


# ==================================
# ACTUALIZAR DETALLE
# ==================================

@token_required
@detalle_factura_bp.route('/<int:id>', methods=['PUT'])
def update_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if detalle is None:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    data = request.get_json()

    detalle.factura_id = data.get(
        'factura_id',
        detalle.factura_id
    )

    detalle.producto_id = data.get(
        'producto_id',
        detalle.producto_id
    )

    detalle.cantidad = data.get(
        'cantidad',
        detalle.cantidad
    )

    detalle.precio_unitario = data.get(
        'precio_unitario',
        detalle.precio_unitario
    )

    detalle.subtotal = data.get(
        'subtotal',
        detalle.subtotal
    )

    if detalle.factura_id is None:
        return jsonify({
            'message': 'La factura es obligatoria'
        }), 400

    if detalle.producto_id is None:
        return jsonify({
            'message': 'El producto es obligatorio'
        }), 400

    try:
        detalle.cantidad = int(detalle.cantidad)
        detalle.precio_unitario = float(detalle.precio_unitario)
        detalle.subtotal = float(detalle.subtotal)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'Cantidad, precio y subtotal deben ser numéricos'
        }), 400

    if detalle.cantidad <= 0:
        return jsonify({
            'message': 'La cantidad debe ser mayor que cero'
        }), 400

    if detalle.precio_unitario < 0:
        return jsonify({
            'message': 'El precio unitario no puede ser negativo'
        }), 400

    if detalle.subtotal < 0:
        return jsonify({
            'message': 'El subtotal no puede ser negativo'
        }), 400

    try:
        session.commit()

        return jsonify({
            'message': 'Detalle actualizado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el detalle',
            'error': str(e)
        }), 500


# ==================================
# ELIMINAR DETALLE
# ==================================

@token_required
@detalle_factura_bp.route('/<int:id>', methods=['DELETE'])
def delete_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if detalle is None:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    try:
        detalle.delete()

        return jsonify({
            'message': 'Detalle eliminado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar el detalle',
            'error': str(e)
        }), 500 