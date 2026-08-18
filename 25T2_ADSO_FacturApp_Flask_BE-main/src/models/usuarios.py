from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    telefono = Column(String(20))

    def __init__(self, nombre, apellido, usuario, correo, password, rol, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.correo = correo
        self.password = password
        self.rol = rol
        self.telefono = telefono

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Usuarios).all()

    @staticmethod
    def get_by_id(id):
        return session.query(Usuarios).filter_by(id=id).first()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()