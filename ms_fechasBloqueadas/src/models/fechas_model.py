from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class FechaBloqueada(Base):
    __tablename__ = "fechas_bloqueadas"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)    
    servicio_id = Column(UUID(as_uuid=True), ForeignKey('usr_app.servicios.id_servicio'))
    fecha = Column(DateTime)
    motivo = Column(String)
    bloqueado_por = Column(String)
    bloqueo_activo = Column(Boolean)

class Servicio(Base):
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
 
