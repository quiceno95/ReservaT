from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DatosMayorista(BaseModel):
    nombre: str
    apellidos: str
    descripcion: Optional[str] = None
    email: str
    telefono: str
    direccion: str
    ciudad: str
    pais: str
    recurente: bool = False
    usuario_creador: str
    verificado: bool = False
    intereses: Optional[str] = None
    tipo_documento: str
    numero_documento: str
    activo: bool = True

class ActualizarMayorista(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    descripcion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    recurente: Optional[bool] = None
    usuario_creador: Optional[str] = None
    verificado: Optional[bool] = None
    intereses: Optional[str] = None
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    activo: Optional[bool] = None


class RespuestaMayorista(DatosMayorista):
    id: UUID
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    mayoristas: List[RespuestaMayorista]
    total: int
    page: int
    size: int