from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class RutaModel(Base):
    __tablename__ = "rutas"
    __table_args__ = {'schema': 'usr_app'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)    
    nombre = Column(String)
    descripcion = Column(String)
    duracion_estimada = Column(Integer)
    activo = Column(Boolean)
    puntos_interes = Column(String)
    recomendada = Column(Boolean)
    origen = Column(String)
    destino = Column(String)
    precio = Column(String)  


 
