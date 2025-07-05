from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, time
from uuid import UUID

class DatosProveedor(BaseModel):
    tipo: str
    nombre: str
    descripcion: str
    email: str
    telefono: str
    direccion: str
    ciudad: str
    pais: str
    sitio_web: str
    rating_promedio: int 
    verificado: bool
    fecha_registro: datetime
    ubicacion: str
    redes_sociales: str
    relevancia: str
    usuario_creador: str
    tipo_documento: str
    numero_documento: str         
    activo: bool  

class DatosExperiencia(BaseModel):
    duracion: int
    dificultad: str
    idioma: str
    incluye_transporte: bool
    grupo_maximo: int
    guia_incluido: bool
    equipamiento_requerido: str
    punto_de_encuentro: str
    numero_rnt: str

class CrearExperienciaRequest(BaseModel):
    proveedor: DatosProveedor
    experiencia: DatosExperiencia

############# listar experiencias #############

class ListarDatosProveedor(BaseModel):
    id_proveedor: UUID
    tipo: str
    nombre: str
    descripcion: str
    email: str
    telefono: str
    direccion: str
    ciudad: str
    pais: str
    sitio_web: str
    rating_promedio: int 
    verificado: bool
    fecha_registro: datetime
    ubicacion: str
    redes_sociales: str
    relevancia: str
    usuario_creador: str
    tipo_documento: str
    numero_documento: str         
    activo: bool  

class ListarDatosExperiencia(BaseModel):
    id_experiencia: UUID
    duracion: int
    dificultad: str
    idioma: str
    incluye_transporte: bool
    grupo_maximo: int
    guia_incluido: bool
    equipamiento_requerido: str
    punto_de_encuentro: str
    numero_rnt: str

class ListarExperienciaResponse(BaseModel):
    proveedor: ListarDatosProveedor
    experiencia: ListarDatosExperiencia

class ResponseList(BaseModel):
    data: List[ListarExperienciaResponse]
    total: int
    page: int
    size: int

############# respuesta mensaje experiencia #############

class ResponseMessage(BaseModel):
    message: str
    status: int = 200