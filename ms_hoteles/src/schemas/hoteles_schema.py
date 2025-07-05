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

class DatosHotel(BaseModel):
    estrellas: int
    numero_habitaciones: int
    servicios_incluidos: str
    check_in: time
    check_out: time
    admite_mascotas: bool
    tiene_estacionamiento: bool
    tipo_habitacion: str
    precio_ascendente:  float  
    servicio_restaurante: bool
    recepcion_24_horas: bool
    bar: bool
    room_service: bool
    asensor: bool
    rampa_discapacitado: bool
    pet_friendly: bool
    auditorio: bool
    parqueadero: bool
    piscina: bool
    planta_energia: bool

class CrearHotelRequest(BaseModel):
    proveedor: DatosProveedor
    hotel: DatosHotel

############# listar hoteles #############

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

class ListarDatosHotel(BaseModel):
    id_hotel: UUID
    estrellas: int
    numero_habitaciones: int
    servicios_incluidos: str
    check_in: time
    check_out: time
    admite_mascotas: bool
    tiene_estacionamiento: bool
    tipo_habitacion: str
    precio_ascendente:  float  
    servicio_restaurante: bool
    recepcion_24_horas: bool
    bar: bool
    room_service: bool
    asensor: bool
    rampa_discapacitado: bool
    pet_friendly: bool
    auditorio: bool
    parqueadero: bool
    piscina: bool
    planta_energia: bool

class ListarHotelResponse(BaseModel):
    proveedor: ListarDatosProveedor
    hotel: ListarDatosHotel

class ResponseList(BaseModel):
    data: List[ListarHotelResponse]
    total: int
    page: int
    size: int

############# respuesta mensaje hotel #############

class ResponseMessage(BaseModel):
    message: str
    status: int = 200