from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosReserva(BaseModel):
    servicio_id: UUID
    id_proveedor: UUID
    id_servicio: UUID
    id_mayorista: UUID
    nombre_servicio: str
    descripcion: str
    tipo_servicio: str
    precio: float
    ciudad: str
    activo: bool
    estado: str
    observaciones: str
    fecha_creacion: datetime
    cantidad: int
    
class ActualizarReserva(BaseModel):
    servicio_id: Optional[UUID] = None
    id_proveedor: Optional[UUID] = None
    id_servicio: Optional[UUID] = None
    id_mayorista: Optional[UUID] = None
    nombre_servicio: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_servicio: Optional[str] = None
    precio: Optional[float] = None
    ciudad: Optional[str] = None
    activo: Optional[bool] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    cantidad: Optional[int] = None

class RespuestaReserva(DatosReserva):
    id: UUID
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    reservas: List[RespuestaReserva]
    total: int
    page: int
    size: int