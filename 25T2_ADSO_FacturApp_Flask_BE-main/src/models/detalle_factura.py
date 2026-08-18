from sqlalchemy import Column, Integer, Numeric, ForeignKey
from src.models import Base, session

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'

    id = Column(Integer, primary_key=True)

    factura_id = Column(Integer, ForeignKey('facturas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    def __init__(self, factura_id, producto_id, cantidad, precio_unitario, subtotal):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    def save(self):
        session.add(self)
        session.commit()

    def get():
        detalles = session.query(DetalleFactura).all()
        return detalles

    def get_by_id(id):
        detalle = session.query(DetalleFactura).filter_by(id=id).first()
        return detalle
   
    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()