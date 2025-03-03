"""Definición de modelos de usuario usando Pydantic."""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Modelo para la creación de usuarios."""
    email: EmailStr
    password: str

class UserDB(UserCreate):
    """Modelo de usuario almacenado en la base de datos."""
    hashed_password: str
    created_at: datetime = datetime.utcnow()

class UserLogin(BaseModel):
    """Modelo para el inicio de sesión de usuarios."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Modelo para el token JWT."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Modelo para los datos contenidos en el token JWT."""
    email: Optional[str] = None
