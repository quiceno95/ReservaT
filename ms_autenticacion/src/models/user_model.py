from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class UserModel(Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'usr_app'}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True)
    contraseña = Column(String)
    fecha_registro = Column(DateTime)
    ultimo_login = Column(DateTime)
    activo = Column(Boolean)
    tipo_usuario = Column(String)
    
class MayoristaModel(Base):
    __tablename__ = 'mayoristas'
    __table_args__ = {'schema': 'usr_app'}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String, unique=True)
    

class ProveedorModel(Base):
    __tablename__ = 'proveedores'
    __table_args__ = {'schema': 'usr_app'}
    
    id_proveedor = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String, unique=True)
    tipo = Column(String)


