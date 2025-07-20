from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CheckConstraint
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class RutasModel(Base):
    __tablename__ = "rutas"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    nombre = Column(String, nullable=False)

class TransportesModel(Base):
    __tablename__ = "transportes"
    __table_args__ = {'schema': 'usr_app'}

    id_transporte = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    tipo_vehiculo = Column(String, nullable=False)

class ViajesModel(Base):
    __tablename__ = "viajes"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    ruta_id = Column(UUID(as_uuid=True), ForeignKey('usr_app.rutas.id'))
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True), nullable=False) 
    capacidad_total = Column(Integer)
    capacidad_disponible = Column(Integer)
    precio=Column(Integer)
    guia_asignado = Column(String)
    estado = Column(String, default='disponible', nullable=False)
    id_transportador = Column(UUID(as_uuid=True), ForeignKey('usr_app.transportes.id_transporte'), nullable=False)
    activo = Column(Boolean, default=True)


