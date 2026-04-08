
import email

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, engine
from models import UsuarioDB, NotaDB
from passlib.context import CryptContext
import models, os
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

class UsuarioSchema(BaseModel):
    email: str
    password: str


def crear_token(email: str):
    expiracion = datetime.utcnow() + timedelta(hours=24)
    datos = {"sub": email, "exp": expiracion}
    return jwt.encode(datos, SECRET_KEY, algorithm="HS256")


@app.get("/")
def inicio():
    return "H"

@app.get("/libros")
def listar_libros(db = Depends(get_db)):
    libros = db.query(NotaDB).all()
    return libros

@app.get("/libros/{titulo}")
def buscar_libro( titulo: str, db = Depends(get_db)):
    libro = db.query(NotaDB).filter(NotaDB.titulo == titulo).first()
    if libro:
        return libro
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/registro")
def crear_usuario(usuario: UsuarioSchema, db = Depends(get_db)):
    password_hasheada = pwd_context.hash(usuario.password)
    nuevo = UsuarioDB(
        email=usuario.email,
        password=password_hasheada
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/login")
def login(usuario: UsuarioSchema, db = Depends(get_db)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not pwd_context.verify(usuario.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Usuario y clave no coinciden")
    else:
        return {"token": crear_token(usuario_db.email)}

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
