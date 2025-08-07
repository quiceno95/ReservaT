from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class ReservaModel(Base):
    __tablename__ = "reservas"
    __table_args__ = {'schema': 'usr_app'}

    id_reserva = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    id_proveedor = Column(UUID(as_uuid=True), nullable=False)
    id_servicio = Column(UUID(as_uuid=True), nullable=False)
    id_mayorista = Column(UUID(as_uuid=True), nullable=True)
    nombre_servicio = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    tipo_servicio = Column(String, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    ciudad = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
    estado = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow)
    cantidad = Column(Integer, nullable=False) 

class ServicioModel(Base):
    __tablename__ = "servicios"
    __table_args__ = {'schema': 'usr_app'}

    id_servicio = Column(UUID(as_uuid=True), primary_key=True)
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

class MayoristaModel(Base):
    __tablename__ = "mayoristas"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True)
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
