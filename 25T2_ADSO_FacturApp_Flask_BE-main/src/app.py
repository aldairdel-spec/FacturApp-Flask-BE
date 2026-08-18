from flask import Flask
from src.config import SECRET_KEY
from src.models import Base, engine

# Modelos
from src.models.categorias import Categorias
from src.models.clientes import Clientes
from src.models.productos import Productos
from src.models.usuarios import Usuarios
from src.models.facturas import Facturas
from src.models.detalle_factura import DetalleFactura
from src.models.metodos_pago import MetodosPago

# Rutas (Blueprints)
from src.routes.productos import productos_bp
from src.routes.clientes import clientes_bp
from src.routes.categorias import categorias_bp
from src.routes.usuarios import usuarios_bp
from src.routes.facturas import facturas_bp
from src.routes.detalle_factura import detalle_factura_bp
from src.routes.metodos_pago import metodos_pago_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Registrar las rutas
app.register_blueprint(productos_bp, url_prefix='/productos')
app.register_blueprint(clientes_bp, url_prefix='/clientes')
app.register_blueprint(categorias_bp, url_prefix='/categorias')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(facturas_bp, url_prefix='/facturas')
app.register_blueprint(detalle_factura_bp, url_prefix='/detalle_factura')
app.register_blueprint(metodos_pago_bp, url_prefix='/metodos_pago')

if __name__ == '__main__':
    app.run(debug=True)
