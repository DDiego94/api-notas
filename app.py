from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, engine
from models import UsuarioDB, NotaDB
from passlib.context import CryptContext
import models
import os
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")

models.Base.metadata.create_all(bind=engine)

# Coneccion a la db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creacion de la app
app = FastAPI()

# Definicion de esquemas
class UsuarioSchema(BaseModel):
    email: str
    password: str

class NotaSchema(BaseModel):
    titulo: str
    contenido: str

# Creacion y verificacion de Tokens
def crear_token(email: str):
    expiracion = datetime.utcnow() + timedelta(hours=24)
    datos = {"sub": email, "exp": expiracion}
    return jwt.encode(datos, SECRET_KEY, algorithm="HS256")

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalido")
        return email
    except:
        raise HTTPException(status_code=401, detail="Token invalido")

# Ruta de inicio
@app.get("/")
def inicio():
    return "H"

# Ruta para listar notas
@app.get("/notas")
def listar_notas(db = Depends(get_db), email = Depends(verificar_token)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    notas = db.query(NotaDB).filter(NotaDB.usuario_id == usuario_db.id).all()
    return notas

# Ruta para crear notas
@app.post("/nota_nueva")
def crear_nota(nota: NotaSchema, db = Depends(get_db), email = Depends(verificar_token)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
    nueva_nota = NotaDB(
        titulo=nota.titulo,
        contenido=nota.contenido,
        usuario_id=usuario_db.id
    )
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota

# Ruta para eliminar nota
@app.delete("/notas/{id}")
def eliminar_nota(id: int, db = Depends(get_db), email = Depends(verificar_token)):
    nota = db.query(NotaDB).filter(NotaDB.id == id).first()
    if nota:
        db.delete(nota)
        db.commit()
        return "Nota eliminada"
    else:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

# Ruta para registro de usuario
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

# Ruta para login de usuario
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.email == form_data.username).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not pwd_context.verify(form_data.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Usuario y clave no coinciden")
    token = crear_token(usuario_db.email)
    return {
        "access_token": token, 
        "token_type": "bearer"
    }
