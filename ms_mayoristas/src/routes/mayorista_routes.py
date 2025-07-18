from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, and_, text
from datetime import datetime, timedelta
import logging
import uuid
from uuid import UUID
from fastapi.responses import JSONResponse
from config.db2 import DB
from models.mayorista_model import Mayorista
from schemas.mayorista_schema import DatosMayorista, ActualizarMayorista, RespuestaMayorista, ResponseMessage, ResponseList
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

mayorista = APIRouter()

@mayorista.post("/mayorista", response_model=ResponseMessage)
async def crear_mayorista(mayorista: DatosMayorista, db: Session = Depends(get_db)):
    """Crea un nuevo mayorista en la base de datos"""
    existing_mayorista = db.query(Mayorista).filter(Mayorista.email == mayorista.email).first()
    if existing_mayorista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    try:
        nuevo_mayorista = Mayorista(**mayorista.model_dump())
        db.add(nuevo_mayorista)
        db.commit()
        db.refresh(nuevo_mayorista)
        return ResponseMessage(message="Mayorista creado exitosamente")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear mayorista"
        )

@mayorista.get("/mayorista", response_model=ResponseList)
async def listar_mayoristas(pagina: int = 0, limite: int = 100, db: Session = Depends(get_db)):
    """Lista todos los mayoristas con paginación"""
    try:
        skip = (pagina - 1) * pagina
        total = db.query(Mayorista).filter(Mayorista.activo == True).count()
        mayoristas = db.query(Mayorista).filter(Mayorista.activo == True).offset(skip).limit(limite).all()
        
        return ResponseList(
            mayoristas=mayoristas,
            total=total,
            page=pagina,
            size=limite
        )
        
    except Exception as e:
        logger.error(f"Error en listado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar mayoristas"
        )

@mayorista.get("/mayorista/listar/{id_mayorista}", response_model=RespuestaMayorista)
async def consultar_mayorista(id_mayorista: str, db: Session = Depends(get_db)):
    """Consulta un mayorista específico por su ID"""
    try:
        uuid_obj = UUID(id_mayorista)

        db_mayorista = db.query(Mayorista).filter(Mayorista.id == id_mayorista).filter(Mayorista.activo == True).first()

        if db_mayorista is None:
            raise HTTPException(status_code=404, detail="Mayorista no encontrado")

        return db_mayorista

    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )
    
  
        

@mayorista.put("/mayorista/editar/{id_mayorista}", response_model=RespuestaMayorista)
async def actualizar_mayorista(id_mayorista: str, datos: ActualizarMayorista, db: Session = Depends(get_db)):
    """Actualiza los datos de un mayorista existente"""
    db_mayorista = db.query(Mayorista).filter(Mayorista.id == id_mayorista).filter(Mayorista.activo == True).first()
    if db_mayorista is None:
        raise HTTPException(status_code=404, detail="Mayorista no encontrado")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(db_mayorista, key, value)
    
    db.commit()
    db.refresh(db_mayorista)
    return db_mayorista

@mayorista.delete("/mayorista/{id_mayorista}", response_model=ResponseMessage)
async def eliminar_mayorista(id_mayorista: str, db: Session = Depends(get_db)):
    
    try:
        uuid_obj = UUID(id_mayorista)
        db_mayorista = db.query(Mayorista).filter(Mayorista.id == id_mayorista).first()
        if not db_mayorista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mayorista no encontrado"
            )
        if not db_mayorista.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El mayorista ya ha sido eliminado"
            )  
        try:
            db_mayorista.activo = False
            db.commit()
            return ResponseMessage(message="Mayorista eliminado exitosamente") 
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en eliminación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar mayorista"
            )
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )

# Endpoint de Health Check
@mayorista.get("/mayorista/healthchecker")
def get_live():
    return {"message": "Mayorista service is LIVE!!"}

# Endpoint de Readiness
@mayorista.get("/mayorista/readiness")
def check_readiness(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result and result[0] == 1:
            return {"status": "Ready"}
        return {"status": "Not Ready"}
    except Exception as e:
        logger.error(f"Error en readiness check: {str(e)}")
        return {"status": "Not Ready"}