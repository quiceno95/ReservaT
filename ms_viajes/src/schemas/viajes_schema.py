from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosViaje(BaseModel):
    ruta_id: UUID
    fecha_inicio: datetime
    fecha_fin: datetime
    capacidad_total: int
    capacidad_disponible: int
    precio: int
    guia_asignado: str  
    estado: str
    id_transportador: UUID
    activo: bool

class ActualizarViaje(BaseModel):
    ruta_id: Optional[UUID] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    capacidad_total: Optional[int] = None
    capacidad_disponible: Optional[int] = None
    precio: Optional[int] = None
    guia_asignado: Optional[str] = None
    estado: Optional[str] = None
    id_transportador: Optional[UUID] = None
    activo: Optional[bool] = None

class RespuestaViaje(BaseModel):
    id: UUID
    ruta_id: Optional[UUID] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    capacidad_total: Optional[int] = None
    capacidad_disponible: Optional[int] = None
    precio: Optional[int] = None
    guia_asignado: Optional[str] = None
    estado: Optional[str] = None
    id_transportador: Optional[UUID] = None
    activo: Optional[bool] = None
    
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    viajes: List[RespuestaViaje]
    total: int
    page: int
    size: int