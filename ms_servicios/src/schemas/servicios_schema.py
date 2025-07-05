from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosServicio(BaseModel):
    proveedor_id: UUID
    nombre: str
    descripcion: str
    tipo_servicio: str
    precio: int
    moneda: str
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    relevancia: str
    ciudad: str
    departamento: str
    ubicacion: str
    detalles_del_servicio: str
    
class ActualizarServicio(BaseModel):
    id_servicio: UUID
    proveedor_id: UUID
    nombre: str
    descripcion: str
    tipo_servicio: str
    precio: int
    moneda: str
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    relevancia: str
    ciudad: str
    departamento: str
    ubicacion: str
    detalles_del_servicio: str

class RespuestaServicio(DatosServicio):
    id_servicio: UUID
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    servicios: List[RespuestaServicio]
    total: int
    page: int
    size: int