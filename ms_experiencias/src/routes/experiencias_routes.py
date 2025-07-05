from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, and_, text
from datetime import datetime, timedelta
import logging
import uuid
from uuid import UUID
from fastapi.responses import JSONResponse
from config.db2 import DB
from models.experiencias_model import ExperienciaModel, ProveedorModel
from schemas.experiencias_schema import DatosExperiencia, CrearExperienciaRequest, ResponseMessage, ResponseList, DatosProveedor, ListarExperienciaResponse, ListarDatosProveedor, ListarDatosExperiencia
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

experiencias = APIRouter()

def crear_registro(model, datos, uuid=None):
    """Crea un registro en la base de datos usando los datos del schema"""
    # Filtrar los campos que están en el modelo
    campos_modelo = {k: v for k, v in datos.items() if hasattr(model, k)}
    if uuid:
        # Obtener el nombre del campo ID del modelo
        for column in model.__table__.columns:
            if column.primary_key:
                campos_modelo[column.name] = uuid
                break
    return model(**campos_modelo)

@experiencias.post("/experiencias/crear/", response_model=ResponseMessage)
async def crear_experiencia(request: CrearExperienciaRequest, db: Session = Depends(get_db)):
    """Crea un nuevo restaurante y su proveedor asociado en la base de datos"""
    
    # Verificar si el proveedor ya existe
    if db.query(ProveedorModel).filter(ProveedorModel.email == request.proveedor.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El proveedor ya existe"
        )
    
    try:
        # Generar UUID único
        nuevo_uuid = uuid.uuid4()
        
        # Crear y guardar proveedor
        proveedor_datos = request.proveedor.model_dump()
        nuevo_proveedor = crear_registro(ProveedorModel, proveedor_datos, nuevo_uuid)
        db.add(nuevo_proveedor)
        db.commit()
        
        # Crear y guardar experiencia
        experiencia_datos = request.experiencia.model_dump()
        nuevo_experiencia = crear_registro(ExperienciaModel, experiencia_datos, nuevo_uuid)
        db.add(nuevo_experiencia)
        db.commit()
        
        return ResponseMessage(message="Proveedor y experiencia creados exitosamente")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el proveedor y experiencia"
        )

@experiencias.get("/experiencias/listar/", response_model=ResponseList)
async def listar_experiencias(pagina: int = 1,limite: int = 100,db: Session = Depends(get_db)):
    """Lista todos los restaurantes con su información de proveedor"""
    try:
        pagina = max(1, pagina)
        skip = (pagina - 1) * limite

        query = db.query(ExperienciaModel, ProveedorModel)\
            .join(ProveedorModel, ExperienciaModel.id_experiencia == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True)

        total = query.count()
        print("Total de experiencias:", total)
    
        resultados = query.offset(skip).limit(limite).all()

        lista_respuesta = []

        for experiencia, proveedor in resultados:

            proveedor_dict = proveedor.__dict__.copy()
            experiencia_dict = experiencia.__dict__.copy()

            item = ListarExperienciaResponse(
                proveedor=ListarDatosProveedor(**proveedor_dict),
                experiencia=ListarDatosExperiencia(**experiencia_dict)
            )
            lista_respuesta.append(item)

        return ResponseList(
            data=lista_respuesta,
            total=total,
            page=pagina,
            size=limite
        )

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al listar experiencias")

@experiencias.get("/experiencias/consultar/{id_experiencia}", response_model=ListarExperienciaResponse)
async def listar_experiencias(id_experiencia: str,db: Session = Depends(get_db)):
    """Lista todos los restaurantes con su información de proveedor"""
    try:

        query = db.query(ExperienciaModel, ProveedorModel)\
            .join(ProveedorModel, ExperienciaModel.id_experiencia == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True, ExperienciaModel.id_experiencia == id_experiencia)

        resultados = query.all()

        if not resultados:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="restaurante no encontrado")

        try:
            for experiencia, proveedor in resultados:
                proveedor_dict = proveedor.__dict__.copy()
                experiencia_dict = experiencia.__dict__.copy()

            return ListarExperienciaResponse(
                    proveedor=ListarDatosProveedor(**proveedor_dict),
                    experiencia=ListarDatosExperiencia(**experiencia_dict)
                )
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Error al listar experiencias")

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al listar experiencias")
   
@experiencias.put("/experiencias/editar/{id_experiencia}", response_model=ListarExperienciaResponse)
async def actualizar_experiencia(id_experiencia: str, datos: CrearExperienciaRequest, db: Session = Depends(get_db)):
    """Actualiza los datos de un restaurante y su proveedor"""
    try:
        # Obtener el restaurante y proveedor existentes
        db_experiencia, db_proveedor = db.query(ExperienciaModel, ProveedorModel)\
            .join(ProveedorModel, ExperienciaModel.id_experiencia == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True, ExperienciaModel.id_experiencia == id_experiencia).first()
        
        if db_experiencia is None:
            raise HTTPException(status_code=404, detail="Experiencia no encontrada")

        # Actualizar los campos del restaurante
        for key, value in datos.experiencia.model_dump(exclude_unset=True).items():
            setattr(db_experiencia, key, value)

        # Actualizar los campos del proveedor
        for key, value in datos.proveedor.model_dump(exclude_unset=True).items():
            setattr(db_proveedor, key, value)

        # Guardar cambios
        db.commit()
        
        # Refrescar los objetos
        db.refresh(db_experiencia)
        db.refresh(db_proveedor)

        # Devolver la respuesta con los datos actualizados
        return ListarExperienciaResponse(
            proveedor=ListarDatosProveedor(**db_proveedor.__dict__),
            experiencia=ListarDatosExperiencia(**db_experiencia.__dict__)
        )

    except Exception as e:
        logger.error(f"Error al actualizar restaurante: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la experiencia"
        )

@experiencias.delete("/experiencias/eliminar/{id_experiencia}", response_model=ResponseMessage)
async def eliminar_experiencia(id_experiencia: str, db: Session = Depends(get_db)):
    
    try:
        uuid_obj = UUID(id_experiencia)
        
        db_proveedor = db.query(ProveedorModel)\
            .filter(ProveedorModel.id_proveedor == id_experiencia).first()

        if not db_proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experiencia no encontrada"
            )
        if db_proveedor.activo == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La experiencia ya ha sido eliminada"
            )  
        try:
            db_proveedor.activo = False
            db.commit()
            return ResponseMessage(message="Experiencia eliminada exitosamente") 
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en eliminación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la experiencia"
            )
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )
