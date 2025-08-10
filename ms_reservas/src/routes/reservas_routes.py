from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, and_, text
from datetime import datetime, timedelta, date
import logging
import uuid
from uuid import UUID
from fastapi.responses import JSONResponse
from config.db2 import DB
from models.reservas_model import (
    ReservaModel,
    ServicioModel,
    ProveedorModel,
    MayoristaModel,
)
from schemas.reservas_schema import (
    DatosReserva,
    ActualizarReserva,
    RespuestaReserva,
    ResponseMessage,
    ResponseList,
)
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

@reservas.post("/reservas/crear")
async def crear_reserva(datos: DatosReserva, db: Session = Depends(get_db)):
    """Crea una nueva reserva validando proveedor y mayorista"""
    try:
        # Validar existencia de proveedor
        prov = db.query(ProveedorModel).filter(ProveedorModel.id_proveedor == str(datos.id_proveedor)).first()
        if prov is None or (hasattr(ProveedorModel, "activo") and prov.activo is not None and prov.activo is False):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado o inactivo")

        # Validar existencia de mayorista (opcional si viene)
        if datos.id_mayorista is not None:
            may = db.query(MayoristaModel).filter(MayoristaModel.id == str(datos.id_mayorista)).first()
            if may is None or (hasattr(MayoristaModel, "activo") and may.activo is not None and may.activo is False):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mayorista no encontrado o inactivo")

        # Validar existencia de servicio
        serv = db.query(ServicioModel).filter(ServicioModel.id_servicio == str(datos.id_servicio)).first()
        if serv is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado")

        # Normalizar tipos según esquema real de BD
        precio_str = str(datos.precio) if datos.precio is not None else None
        # activo ahora es booleano
        activo_val = bool(getattr(datos, 'activo', True))
        # fechas
        fecha_crea = datos.fecha_creacion.date() if hasattr(datos, 'fecha_creacion') and datos.fecha_creacion else None
        fecha_inicio_val = datos.fecha_inicio if hasattr(datos, 'fecha_inicio') else None
        fecha_fin_val = datos.fecha_fin if hasattr(datos, 'fecha_fin') else None

        nueva = ReservaModel(
            id_proveedor=str(datos.id_proveedor),
            id_servicio=str(datos.id_servicio),
            id_mayorista=str(datos.id_mayorista) if datos.id_mayorista is not None else None,
            nombre_servicio=datos.nombre_servicio,
            descripcion=datos.descripcion,
            tipo_servicio=datos.tipo_servicio,
            precio=precio_str,
            ciudad=datos.ciudad,
            activo=activo_val,
            estado=datos.estado,
            observaciones=datos.observaciones,
            fecha_creacion=fecha_crea,
            fecha_inicio=fecha_inicio_val,
            fecha_fin=fecha_fin_val,
            cantidad=datos.cantidad,
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        return {"message": "Reserva creada exitosamente", "id_reserva": str(nueva.id_reserva)}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear reserva: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la reserva")

@reservas.get("/reservas/listar/")
async def listar_reservas(pagina: int = 1, limite: int = 100, db: Session = Depends(get_db)):
    """Lista todas las reservas con paginación"""
    try:
        if pagina < 1:
            pagina = 1
        if limite < 1:
            limite = 100
        skip = (pagina - 1) * limite

        base_query = db.query(ReservaModel).filter(ReservaModel.activo == True)
        total = base_query.count()
        reservas_db = base_query.offset(skip).limit(limite).all()

        # Serialización manual para evitar inconsistencias de schema
        reservas_list = [
            {
                "id": str(r.id_reserva),
                "id_proveedor": str(r.id_proveedor) if getattr(r, "id_proveedor", None) else None,
                "id_servicio": str(r.id_servicio) if getattr(r, "id_servicio", None) else None,
                "id_mayorista": str(r.id_mayorista) if getattr(r, "id_mayorista", None) else None,
                "nombre_servicio": r.nombre_servicio,
                "descripcion": r.descripcion,
                "tipo_servicio": r.tipo_servicio,
                "precio": r.precio,
                "ciudad": r.ciudad,
                "activo": r.activo,
                "estado": r.estado,
                "observaciones": r.observaciones,
                "fecha_creacion": r.fecha_creacion,
                "fecha_inicio": r.fecha_inicio,
                "fecha_fin": r.fecha_fin,
                "cantidad": r.cantidad,
            }
            for r in reservas_db
        ]

        return {
            "reservas": reservas_list,
            "total": total,
            "page": pagina,
            "size": limite,
        }

    except Exception as e:
        logger.error(f"Error en listado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar las reservas",
        )


@reservas.get("/reservas/listar/proveedor/{id_proveedor}")
async def listar_reservas_por_proveedor(id_proveedor: str, pagina: int = 1, limite: int = 100, db: Session = Depends(get_db)):
    """Lista reservas por proveedor con paginación"""
    try:
        # Validar UUID
        _ = UUID(id_proveedor)

        if pagina < 1:
            pagina = 1
        if limite < 1:
            limite = 100
        skip = (pagina - 1) * limite

        base_query = (
            db.query(ReservaModel)
            .filter(ReservaModel.id_proveedor == id_proveedor)
            .filter(ReservaModel.activo == True)
        )
        total = base_query.count()
        reservas_db = base_query.offset(skip).limit(limite).all()

        reservas_list = [
            {
                "id": str(r.id_reserva),
                "id_proveedor": str(r.id_proveedor) if getattr(r, "id_proveedor", None) else None,
                "id_servicio": str(r.id_servicio) if getattr(r, "id_servicio", None) else None,
                "id_mayorista": str(r.id_mayorista) if getattr(r, "id_mayorista", None) else None,
                "nombre_servicio": r.nombre_servicio,
                "descripcion": r.descripcion,
                "tipo_servicio": r.tipo_servicio,
                "precio": r.precio,
                "ciudad": r.ciudad,
                "activo": r.activo,
                "estado": r.estado,
                "observaciones": r.observaciones,
                "fecha_creacion": r.fecha_creacion,
                "fecha_inicio": r.fecha_inicio,
                "fecha_fin": r.fecha_fin,
                "cantidad": r.cantidad,
            }
            for r in reservas_db
        ]

        return {
            "reservas": reservas_list,
            "total": total,
            "page": pagina,
            "size": limite,
        }
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de proveedor no es un UUID válido",
        )
    except Exception as e:
        logger.error(f"Error al listar por proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar reservas por proveedor",
        )


@reservas.get("/reservas/listar/mayorista/{id_mayorista}")
async def listar_reservas_por_mayorista(id_mayorista: str, pagina: int = 1, limite: int = 100, db: Session = Depends(get_db)):
    """Lista reservas por mayorista con paginación"""
    try:
        # Validar UUID
        _ = UUID(id_mayorista)

        if pagina < 1:
            pagina = 1
        if limite < 1:
            limite = 100
        skip = (pagina - 1) * limite

        base_query = (
            db.query(ReservaModel)
            .filter(ReservaModel.id_mayorista == id_mayorista)
            .filter(ReservaModel.activo == True)
        )
        total = base_query.count()
        reservas_db = base_query.offset(skip).limit(limite).all()

        reservas_list = [
            {
                "id": str(r.id_reserva),
                "id_proveedor": str(r.id_proveedor) if getattr(r, "id_proveedor", None) else None,
                "id_servicio": str(r.id_servicio) if getattr(r, "id_servicio", None) else None,
                "id_mayorista": str(r.id_mayorista) if getattr(r, "id_mayorista", None) else None,
                "nombre_servicio": r.nombre_servicio,
                "descripcion": r.descripcion,
                "tipo_servicio": r.tipo_servicio,
                "precio": r.precio,
                "ciudad": r.ciudad,
                "activo": r.activo,
                "estado": r.estado,
                "observaciones": r.observaciones,
                "fecha_creacion": r.fecha_creacion,
                "cantidad": r.cantidad,
            }
            for r in reservas_db
        ]

        return {
            "reservas": reservas_list,
            "total": total,
            "page": pagina,
            "size": limite,
        }
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de mayorista no es un UUID válido",
        )
    except Exception as e:
        logger.error(f"Error al listar por mayorista: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar reservas por mayorista",
        )


@reservas.put("/reservas/editar/{id_reserva}")
async def editar_reserva(id_reserva: str, datos: ActualizarReserva, db: Session = Depends(get_db)):
    """Edita una reserva existente"""
    try:
        _ = UUID(id_reserva)
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de la reserva no es un UUID válido",
        )

    reserva = db.query(ReservaModel).filter(ReservaModel.id_reserva == id_reserva).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    try:
        for key, value in datos.model_dump(exclude_unset=True).items():
            # Asignación directa de campos del schema al modelo
            setattr(reserva, key, value)

        db.commit()
        db.refresh(reserva)

        return {"message": "Reserva actualizada exitosamente"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar reserva: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al editar la reserva",
        )


@reservas.delete("/reservas/eliminar/{id_reserva}")
async def eliminar_reserva(id_reserva: str, db: Session = Depends(get_db)):
    """Elimina lógicamente una reserva (activo = False)"""
    try:
        _ = UUID(id_reserva)
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de la reserva no es un UUID válido",
        )

    reserva = db.query(ReservaModel).filter(ReservaModel.id_reserva == id_reserva).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if getattr(reserva, "activo", True) is False:
        raise HTTPException(status_code=400, detail="La reserva ya está eliminada")

    try:
        # Eliminación lógica
        setattr(reserva, "activo", False)
        db.commit()
        return {"message": "Reserva eliminada exitosamente"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar reserva: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la reserva",
        )


@reservas.get("/reservas/consultar/{id_reserva}")
async def obtener_reserva(id_reserva: str, db: Session = Depends(get_db)):
    """Obtiene una reserva por su ID"""
    try:
        _ = UUID(id_reserva)
    except (ValueError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de la reserva no es un UUID válido",
        )

    reserva = db.query(ReservaModel).filter(ReservaModel.id_reserva == id_reserva).first()
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    data = {
        "id": str(reserva.id_reserva),
        "id_proveedor": str(reserva.id_proveedor) if getattr(reserva, "id_proveedor", None) else None,
        "id_servicio": str(reserva.id_servicio) if getattr(reserva, "id_servicio", None) else None,
        "id_mayorista": str(reserva.id_mayorista) if getattr(reserva, "id_mayorista", None) else None,
        "nombre_servicio": reserva.nombre_servicio,
        "descripcion": reserva.descripcion,
        "tipo_servicio": reserva.tipo_servicio,
        "precio": reserva.precio,
        "ciudad": reserva.ciudad,
        "activo": reserva.activo,
        "estado": reserva.estado,
        "observaciones": reserva.observaciones,
        "fecha_creacion": reserva.fecha_creacion,
        "fecha_inicio": reserva.fecha_inicio,
        "fecha_fin": reserva.fecha_fin,
        "cantidad": reserva.cantidad,
    }

    return data

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