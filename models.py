
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    notas = relationship("NotaDB", back_populates="autor")

class NotaDB(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    autor = relationship("UsuarioDB", back_populates="notas")