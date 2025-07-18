from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, and_, text
from datetime import datetime, timedelta
import logging
import uuid
from uuid import UUID
from fastapi.responses import JSONResponse
from config.db2 import DB
from models.hoteles_model import HotelModel, ProveedorModel
from schemas.hoteles_schema import DatosHotel, CrearHotelRequest, ResponseMessage, ResponseList, DatosProveedor, ListarHotelResponse, ListarDatosProveedor, ListarDatosHotel
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

hoteles = APIRouter()

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

@hoteles.post("/hoteles/crear/", response_model=ResponseMessage)
async def crear_hotel(request: CrearHotelRequest, db: Session = Depends(get_db)):
    """Crea un nuevo hotel y su proveedor asociado en la base de datos"""
    
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
        
        # Crear y guardar hotel
        hotel_datos = request.hotel.model_dump()
        nuevo_hotel = crear_registro(HotelModel, hotel_datos, nuevo_uuid)
        db.add(nuevo_hotel)
        db.commit()
        
        return ResponseMessage(message="Proveedor y hotel creados exitosamente")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el proveedor y hotel"
        )

@hoteles.get("/hoteles/listar/", response_model=ResponseList)
async def listar_hoteles(pagina: int = 1,limite: int = 100,db: Session = Depends(get_db)):
    """Lista todos los hoteles con su información de proveedor"""
    try:
        pagina = max(1, pagina)
        skip = (pagina - 1) * limite

        query = db.query(HotelModel, ProveedorModel)\
            .join(ProveedorModel, HotelModel.id_hotel == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True)

        total = query.count()

        resultados = query.offset(skip).limit(limite).all()

        lista_respuesta = []

        for hotel, proveedor in resultados:

            proveedor_dict = proveedor.__dict__.copy()
            hotel_dict = hotel.__dict__.copy()

            item = ListarHotelResponse(
                proveedor=ListarDatosProveedor(**proveedor_dict),
                hotel=ListarDatosHotel(**hotel_dict)
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
        raise HTTPException(status_code=500, detail="Error al listar hoteles")

@hoteles.get("/hoteles/consultar/{id_hotel}", response_model=ListarHotelResponse)
async def listar_hoteles(id_hotel: str,db: Session = Depends(get_db)):
    """Lista todos los hoteles con su información de proveedor"""
    try:

        query = db.query(HotelModel, ProveedorModel)\
            .join(ProveedorModel, HotelModel.id_hotel == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True, HotelModel.id_hotel == id_hotel)

        resultados = query.all()

        if not resultados:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel no encontrado")

        try:
            for hotel, proveedor in resultados:
                proveedor_dict = proveedor.__dict__.copy()
                hotel_dict = hotel.__dict__.copy()

            return ListarHotelResponse(
                    proveedor=ListarDatosProveedor(**proveedor_dict),
                    hotel=ListarDatosHotel(**hotel_dict)
                )
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Error al listar hoteles")

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al listar hoteles")
   
@hoteles.put("/hoteles/editar/{id_hotel}", response_model=ListarHotelResponse)
async def actualizar_hotel(id_hotel: str, datos: CrearHotelRequest, db: Session = Depends(get_db)):
    """Actualiza los datos de un hotel y su proveedor"""
    try:
        # Obtener el hotel y proveedor existentes
        db_hotel, db_proveedor = db.query(HotelModel, ProveedorModel)\
            .join(ProveedorModel, HotelModel.id_hotel == ProveedorModel.id_proveedor)\
            .filter(ProveedorModel.activo == True, HotelModel.id_hotel == id_hotel).first()
        
        if db_hotel is None:
            raise HTTPException(status_code=404, detail="Hotel no encontrado")

        # Actualizar los campos del hotel
        for key, value in datos.hotel.model_dump(exclude_unset=True).items():
            setattr(db_hotel, key, value)

        # Actualizar los campos del proveedor
        for key, value in datos.proveedor.model_dump(exclude_unset=True).items():
            setattr(db_proveedor, key, value)

        # Guardar cambios
        db.commit()
        
        # Refrescar los objetos
        db.refresh(db_hotel)
        db.refresh(db_proveedor)

        # Devolver la respuesta con los datos actualizados
        return ListarHotelResponse(
            proveedor=ListarDatosProveedor(**db_proveedor.__dict__),
            hotel=ListarDatosHotel(**db_hotel.__dict__)
        )

    except Exception as e:
        logger.error(f"Error al actualizar hotel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el hotel"
        )

@hoteles.delete("/hoteles/eliminar/{id_hotel}", response_model=ResponseMessage)
async def eliminar_hotel(id_hotel: str, db: Session = Depends(get_db)):
    
    try:
        uuid_obj = UUID(id_hotel)
        
        db_proveedor = db.query(ProveedorModel)\
            .filter(ProveedorModel.id_proveedor == id_hotel).first()

        if not db_proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hotel no encontrada"
            )
        if db_proveedor.activo == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El hotel ya ha sido eliminado"
            )  
        try:
            db_proveedor.activo = False
            db.commit()
            return ResponseMessage(message="Hotel eliminado exitosamente") 
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en eliminación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el hotel"
            )
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID proporcionado no es un UUID válido"
        )

# Endpoint de Health Check
@hoteles.get("/hoteles/healthchecker")
def get_live():
    return {"message": "Hoteles service is LIVE!!"}

# Endpoint de Readiness
@hoteles.get("/hoteles/readiness")
def check_readiness(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result and result[0] == 1:
            return {"status": "Ready"}
        return {"status": "Not Ready"}
    except Exception as e:
        logger.error(f"Error en readiness check: {str(e)}")
        return {"status": "Not Ready"}