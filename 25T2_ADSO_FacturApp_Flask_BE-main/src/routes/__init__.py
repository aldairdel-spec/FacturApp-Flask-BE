import math
from flask import request, jsonify
from src.models import session


MAX_PER_PAGE = 100


def get_pagination_params():
    page_param = request.args.get('page')
    per_page_param = request.args.get('per_page')

    if page_param is None and per_page_param is None:
        return None

    try:
        page = int(page_param) if page_param is not None else 1
        per_page = int(per_page_param) if per_page_param is not None else 10
    except (ValueError, TypeError):
        return 'invalid'

    if page < 1 or per_page < 1:
        return 'invalid'

    if per_page > MAX_PER_PAGE:
        per_page = MAX_PER_PAGE

    return {'page': page, 'per_page': per_page}


def paginate_response(query, serializer):
    pagination = get_pagination_params()

    if pagination is None:
        items = query.all()
        lista = [serializer(item) for item in items]
        return jsonify(lista), 200

    if pagination == 'invalid':
        return jsonify({
            'message': 'Parámetros de paginación inválidos. page y per_page deben ser enteros mayores o iguales a 1.'
        }), 400

    page = pagination['page']
    per_page = pagination['per_page']

    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    total_pages = math.ceil(total / per_page) if per_page > 0 else 0

    lista = [serializer(item) for item in items]

    return jsonify({
        'datos': lista,
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages
    }), 200
