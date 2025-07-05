from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class ServicioModel(Base):
    __tablename__ = "servicios"
    __table_args__ = {'schema': 'usr_app'}

    id_servicio = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    proveedor_id = Column(UUID(as_uuid=True), nullable=False)
    nombre = Column(String)
    descripcion = Column(String)
    tipo_servicio = Column(String)
    precio = Column(Numeric(10,2), nullable=False)
    moneda = Column(String, default='USD')
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime(timezone=True))
    relevancia = Column(String)
    ciudad = Column(String)
    departamento = Column(String)
    ubicacion = Column(String)
    detalles_del_servicio = Column(String)
 
class ProveedorModel(Base):
    __tablename__ = "proveedores"
    __table_args__ = {'schema': 'usr_app'}

    id_proveedor = Column(UUID(as_uuid=True), primary_key=True)    
    tipo = Column(String)
    nombre = Column(String)
    descripcion = Column(String)
    email = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    sitio_web = Column(String)
    rating_promedio = Column(Numeric)
    verificado = Column(Boolean)
    fecha_registro = Column(DateTime(timezone=True), default=datetime.utcnow)
    ubicacion = Column(String)
    redes_sociales = Column(String)
    relevancia = Column(String)
    usuario_creador = Column(String)
    tipo_documento = Column(String)
    numero_documento = Column(String)
    activo = Column(Boolean, default=True)
