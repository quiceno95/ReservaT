from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy import Column, ForeignKey
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    tipo_usuario: str = "user"

    class Config:
        from_attributes = True

class UsuarioCreate(UsuarioBase):
    contraseña: str

    @property
    def hashed_password(self) -> str:
        return pwd_context.hash(self.contraseña)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contraseña: Optional[str] = None
    tipo_usuario: Optional[str] = None

    @property
    def hashed_password(self) -> Optional[str]:
        if self.contraseña:
            return pwd_context.hash(self.contraseña)
        return None

class Usuario(UsuarioBase):
    id: uuid.UUID
    fecha_registro: datetime
    ultimo_login: Optional[datetime] = None
    activo: bool = True

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    contraseña: str

class ChangePasswordRequest(BaseModel):
    email: EmailStr
    contraseña_actual: str
    nueva_contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ResponseMessage(BaseModel):
    message: str
    status: int = 200

class ResponseList(BaseModel):
    usuarios: List[Usuario]
    total: int
    page: int
    size: int
