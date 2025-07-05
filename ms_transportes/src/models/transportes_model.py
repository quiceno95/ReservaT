from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

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

class TransporteModel(Base):
    __tablename__ = "transportes"
    __table_args__ = {'schema': 'usr_app'}

    id_transporte = Column(UUID(as_uuid=True), ForeignKey('usr_app.proveedores.id_proveedor'), primary_key=True)
    tipo_vehiculo = Column(String)
    modelo = Column(String)
    anio = Column(Integer)
    placa = Column(String)
    capacidad = Column(Integer)
    aire_acondicionado = Column(Boolean)
    wifi = Column(Boolean)
    disponible = Column(Boolean)
    combustible = Column(String)
    seguro_vigente = Column(Boolean)
    fecha_mantenimiento = Column(DateTime(timezone=True))