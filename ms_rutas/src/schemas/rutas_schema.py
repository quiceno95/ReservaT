from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosRuta(BaseModel):
    nombre: str
    descripcion: str
    duracion_estimada: int
    activo: bool
    puntos_interes: str
    recomendada: bool
    origen: str
    destino: str
    precio: str
    
class ActualizarRuta(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_estimada: Optional[int] = None
    activo: Optional[bool] = None
    puntos_interes: Optional[str] = None
    recomendada: Optional[bool] = None
    origen: Optional[str] = None
    destino: Optional[str] = None
    precio: Optional[str] = None


class RespuestaRuta(DatosRuta):
    id: UUID
    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    rutas: List[RespuestaRuta]
    total: int
    page: int
    size: int


class DatosOrigenDestino(BaseModel):
    origen: str
    destino: str
