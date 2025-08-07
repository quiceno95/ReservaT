from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, and_, text
from datetime import datetime, timedelta
import logging
import uuid
from uuid import UUID
from fastapi.responses import JSONResponse
from config.db2 import DB
from models.reservas_model import ReservaModel, ServicioModel, ProveedorModel, MayoristaModel, ServicioModel
from schemas.reservas_schema import DatosReserva, ActualizarReserva, RespuestaReserva, ResponseMessage, ResponseList
from typing import List
from pydantic import ValidationError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

db = DB.create()
Session = sessionmaker(bind=db.engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

reservas = APIRouter()

@reservas.post("/reservas/crear/", response_model=ResponseMessage)
async def crear_reserva(reserva: DatosReserva, db: Session = Depends(get_db)):
    """Crea un nuevas reservas  en la base de datos"""
    existing_url = db.query(ReservaModel).filter(ReservaModel.url == reserva.url).first()
    existing_servicio = db.query(ServicioModel).filter(and_(ServicioModel.id_servicio == reserva.servicio_id)).first()

    if existing_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="la URL de la foto ya existe"
        )
    if existing_servicio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="el servicio no existe"
        )
    try:
        nuevo_foto = FotoModel(**foto.model_dump())
        db.add(nuevo_foto)
        db.commit()
        db.refresh(nuevo_foto)
        return ResponseMessage(message="Foto creada exitosamente")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la foto"
        )

@reservas.get("/reservas/listar/", response_model=ResponseList)
async def listar_fotos(pagina: int = 0, limite: int = 100, db: Session = Depends(get_db)):
    """Lista todas las fechas bloqueadas con paginación"""
    try:
        skip = (pagina - 1) * pagina
        total = db.query(FotoModel).filter(FotoModel.eliminado == False).count()
        fotos = db.query(FotoModel).filter(FotoModel.eliminado == False).offset(skip).limit(limite).all()
        
        return ResponseList(
            fotos=fotos,
            total=total,
            page=pagina,
            size=limite
        )
        
    except Exception as e:
        logger.error(f"Error en listado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar las fotos"
        )

@reservas.get("/reservas/servicios/{id_servicio}", response_model=ResponseList)
async def listar_reservas(id_servicio: str, pagina: int = 0, limite: int = 100, db: Session = Depends(get_db)):
    """Lista todas las fechas bloqueadas con paginación"""
   
    existing_servicio = db.query(ServicioModel).filter(and_(ServicioModel.id_servicio == id_servicio)).first()

    if existing_servicio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="el servicio no existe"
        )
    try:
        skip = (pagina - 1) * pagina
        total = db.query(FotoModel).filter(FotoModel.eliminado == False, FotoModel.servicio_id == id_servicio).count()
        fotos = db.query(FotoModel).filter(FotoModel.eliminado == False, FotoModel.servicio_id == id_servicio).offset(skip).limit(limite).all()
        
        return ResponseList(
            fotos=fotos,
            total=total,
            page=pagina,
            size=limite
        )
        
    except Exception as e:
        logger.error(f"Error en listado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar las fotos para el servicio: " + id_servicio
        )

@reservas.get("/reservas/consultar/{id_reserva}", response_model=RespuestaReserva)
async def consultar_reserva(id_reserva: str, db: Session = Depends(get_db)):
    """Consulta un mayorista específico por su ID"""
    try:
        uuid_obj = UUID(id_reserva)

        db_foto = db.query(FotoModel).filter(FotoModel.id == id_foto).filter(FotoModel.eliminado == False).first()

        if db_foto is None:
            raise HTTPException(status_code=404, detail="Foto no encontrado")

        return db_foto

    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )
    
@reservas.put("/reservas/editar/{id_reserva}", response_model=RespuestaReserva)
async def actualizar_reserva(id_reserva: str, datos: ActualizarReserva, db: Session = Depends(get_db)):
    """Actualiza los datos de una fecha bloqueada existente"""

    db_reserva = db.query(ReservaModel).filter(ReservaModel.id == id_reserva).filter(ReservaModel.eliminado == False).first()
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Foto no encontrado")

    existing_servicio = db.query(Servicio).filter(and_(Servicio.id_servicio == datos.servicio_id)).first()
    if existing_servicio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="el servicio no existe"
        )
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(db_foto, key, value)
    
    db.commit()
    db.refresh(db_foto)
    return db_foto

@reservas.delete("/reservas/eliminar/{id_reserva}", response_model=ResponseMessage)
async def eliminar_reserva(id_reserva: str, db: Session = Depends(get_db)):
    
    try:
        uuid_obj = UUID(id_reserva)
        db_reserva = db.query(ReservaModel).filter(ReservaModel.id == id_reserva).first()
        if not db_fecha:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foto no encontrada"
            )
        if db_fecha.eliminado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La foto ya ha sido eliminada"
            )  
        try:
            db_fecha.eliminado = True
            db.commit()
            return ResponseMessage(message="Foto eliminada exitosamente") 
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en eliminación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la foto"
            )
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )

# Endpoint de Health Check
@reservas.get("/reservas/healthchecker")
def get_live():
    return {"message": "Reservas service is LIVE!!"}

# Endpoint de Readiness
@reservas.get("/reservas/readiness")
def check_readiness(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result and result[0] == 1:
            return {"status": "Ready"}
        return {"status": "Not Ready"}
    except Exception as e:
        logger.error(f"Error en readiness check: {str(e)}")
        return {"status": "Not Ready"}