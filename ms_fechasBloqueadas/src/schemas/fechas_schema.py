from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosFechaBloqueada(BaseModel):
    servicio_id: UUID
    fecha: datetime
    motivo: str
    bloqueado_por: str
    bloqueo_activo: bool
    
class ActualizarFechaBloqueada(BaseModel):
    servicio_id: Optional[UUID] = None
    fecha: Optional[datetime] = None
    motivo: Optional[str] = None
    bloqueado_por: Optional[str] = None
    bloqueo_activo: Optional[bool] = None

class RespuestaFechaBloqueada(DatosFechaBloqueada):
    id: UUID
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    fechas_bloqueadas: List[RespuestaFechaBloqueada]
    total: int
    page: int
    size: int