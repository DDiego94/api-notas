from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class LibroDB(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    paginas = Column(Integer, nullable=False)
    disponible = Column(Boolean, default=True)