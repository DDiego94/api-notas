from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_engine_with_retry():
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            return engine
        except Exception:
            retries -= 1
            time.sleep(2)
    raise Exception("No se pudo conectar a la base de datos")

engine = create_engine_with_retry()
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass