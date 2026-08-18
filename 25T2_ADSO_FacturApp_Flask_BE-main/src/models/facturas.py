from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from src.models import Base, session

class Facturas(Base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True)
    numero_factura = Column(String(50), unique=True, nullable=False)

    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    subtotal = Column(Numeric(10, 2), nullable=False)
    iva = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    def __init__(self, numero_factura, cliente_id, vendedor_id, subtotal, iva, total):
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        self.subtotal = subtotal
        self.iva = iva
        self.total = total

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Facturas).all()

    def get_by_id(id):
        return session.query(Facturas).filter_by(id=id).first()
    
    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()