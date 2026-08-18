from sqlalchemy import Column, Integer, String
from src.models import Base, session

class MetodosPago(Base):
    __tablename__ = 'metodos_pago'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        session.add(self)
        session.commit()

    def get():
        metodos = session.query(MetodosPago).all()
        return metodos

    def get_by_id(id):
        metodo = session.query(MetodosPago).filter_by(id=id).first()
        return metodo
   
    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()