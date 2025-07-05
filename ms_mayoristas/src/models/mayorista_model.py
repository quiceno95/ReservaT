from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Mayorista(Base):
    __tablename__ = "mayoristas"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    nombre = Column(String)
    apellidos = Column(String)
    descripcion = Column(String)
    email = Column(String, unique=True)
    telefono = Column(String)
    direccion = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    recurente = Column(Boolean)
    usuario_creador = Column(String)
    verificado = Column(Boolean)
    intereses = Column(String)
    tipo_documento = Column(String)
    numero_documento = Column(String)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
