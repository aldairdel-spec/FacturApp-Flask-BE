from flask import Blueprint, request, jsonify
from src.models.productos import Productos
from src.models import session
from src.routes import paginate_response
from src.auth import token_required

productos_bp = Blueprint('productos', __name__)


# ==========================
# CREAR PRODUCTO
# ==========================

@token_required
@productos_bp.route('/', methods=['POST'])
def create_producto():

    data = request.get_json()

    producto = Productos(
        codigo=data.get('codigo'),
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        unidad_medida=data.get('unidad_medida'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        id_categoria=data.get('id_categoria')
    )

    if not producto.codigo:
        return jsonify({
            'message': 'El código es obligatorio'
        }), 400

    if not producto.nombre:
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not producto.descripcion:
        return jsonify({
            'message': 'La descripción es obligatoria'
        }), 400

    if not producto.unidad_medida:
        return jsonify({
            'message': 'La unidad de medida es obligatoria'
        }), 400

    if producto.id_categoria is None:
        return jsonify({
            'message': 'La categoría es obligatoria'
        }), 400

    try:
        producto.precio = float(producto.precio)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'El precio debe ser un número válido'
        }), 400

    if producto.precio <= 0:
        return jsonify({
            'message': 'El precio debe ser mayor a cero'
        }), 400

    try:
        producto.stock = int(producto.stock)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'El stock debe ser un número entero'
        }), 400

    if producto.stock < 0:
        return jsonify({
            'message': 'El stock no puede ser negativo'
        }), 400

    try:
        producto.save()

        return jsonify({
            'message': 'Producto creado exitosamente'
        }), 201

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al crear el producto',
            'error': str(e)
        }), 500


# ==========================
# LISTAR PRODUCTOS
# ==========================

def serialize_producto(producto):
    return {
        "id": producto.id,
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "unidad_medida": producto.unidad_medida,
        "precio": producto.precio,
        "stock": producto.stock,
        "id_categoria": producto.id_categoria
    }


@token_required
@productos_bp.route('/', methods=['GET'])
def get_productos():
    query = session.query(Productos)
    return paginate_response(query, serialize_producto)


# ==========================
# BUSCAR PRODUCTO POR ID
# ==========================

@token_required
@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):

    producto = Productos.get_by_id(id)

    if producto is None:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    return jsonify({
        "id": producto.id,
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "unidad_medida": producto.unidad_medida,
        "precio": producto.precio,
        "stock": producto.stock,
        "id_categoria": producto.id_categoria
    }), 200


# ==========================
# ACTUALIZAR PRODUCTO
# ==========================

@token_required
@productos_bp.route('/<int:id>', methods=['PUT'])
def update_producto(id):

    producto = Productos.get_by_id(id)

    if producto is None:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    data = request.get_json()

    producto.codigo = data.get(
        'codigo',
        producto.codigo
    )

    producto.nombre = data.get(
        'nombre',
        producto.nombre
    )

    producto.descripcion = data.get(
        'descripcion',
        producto.descripcion
    )

    producto.unidad_medida = data.get(
        'unidad_medida',
        producto.unidad_medida
    )

    producto.precio = data.get(
        'precio',
        producto.precio
    )

    producto.stock = data.get(
        'stock',
        producto.stock
    )

    producto.id_categoria = data.get(
        'id_categoria',
        producto.id_categoria
    )

    if not producto.codigo:
        return jsonify({
            'message': 'El código es obligatorio'
        }), 400

    if not producto.nombre:
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if not producto.descripcion:
        return jsonify({
            'message': 'La descripción es obligatoria'
        }), 400

    if not producto.unidad_medida:
        return jsonify({
            'message': 'La unidad de medida es obligatoria'
        }), 400

    try:
        producto.precio = float(producto.precio)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'El precio debe ser un número válido'
        }), 400

    if producto.precio <= 0:
        return jsonify({
            'message': 'El precio debe ser mayor a cero'
        }), 400

    try:
        producto.stock = int(producto.stock)
    except (ValueError, TypeError):
        return jsonify({
            'message': 'El stock debe ser un número entero'
        }), 400

    if producto.stock < 0:
        return jsonify({
            'message': 'El stock no puede ser negativo'
        }), 400

    try:
        session.commit()

        return jsonify({
            'message': 'Producto actualizado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al actualizar el producto',
            'error': str(e)
        }), 500


# ==========================
# ELIMINAR PRODUCTO
# ==========================

@token_required
@productos_bp.route('/<int:id>', methods=['DELETE'])
def delete_producto(id):

    producto = Productos.get_by_id(id)

    if producto is None:
        return jsonify({
            'message': 'Producto no encontrado'
        }), 404

    try:
        producto.delete()

        return jsonify({
            'message': 'Producto eliminado correctamente'
        }), 200

    except Exception as e:
        session.rollback()

        return jsonify({
            'message': 'Error al eliminar el producto',
            'error': str(e)
        }), 500