
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, engine
from models import LibroDB
import models

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

class LibroSchema(BaseModel):
    titulo:str
    autor:str
    paginas:int

@app.get("/")
def inicio():
    return "H"

@app.get("/libros")
def listar_libros(db = Depends(get_db)):
    libros = db.query(LibroDB).all()
    return libros

@app.get("/libros/{titulo}")
def buscar_libro( titulo: str, db = Depends(get_db)):
    libro = db.query(LibroDB).filter(LibroDB.titulo == titulo).first()
    if libro:
        return libro
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/libros")
def crear_libro(libro: LibroSchema, db = Depends(get_db)):
    nuevo = LibroDB(
        titulo=libro.titulo,
        autor=libro.autor,
        paginas=libro.paginas
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/libros/{titulo}")
def modificar_libro(titulo: str, libro: LibroSchema, db = Depends(get_db)):
    mod = db.query(LibroDB).filter(LibroDB.titulo == titulo).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    mod.titulo=libro.titulo
    mod.autor=libro.autor
    mod.paginas=libro.paginas
    db.commit()
    db.refresh(mod)
    return mod

@app.delete("/libros/{titulo}")
def eliminar_libro(titulo: str, db = Depends(get_db)):
    mod = db.query(LibroDB).filter(LibroDB.titulo == titulo).first()
    if mod:
        db.delete(mod)
        db.commit()
        return "Libro eliminado"
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
