"""Lógica para registrar un usuario en la base de datos y autenticación."""

import bcrypt
import jwt
import os
import re
from config import db, logger
from models import UserCreate, UserDB, UserLogin, Token, TokenData
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Optional
from pydantic import ValidationError
from jwt import ExpiredSignatureError, InvalidTokenError

async def create_user(user: UserCreate):
    """Registra un usuario en la base de datos."""
    # Verificar si el usuario ya existe
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise ValueError("El email ya está registrado.")

    # Validar política de contraseñas
    if not validate_password(user.password):
        raise ValueError("La contraseña no cumple con los requisitos de seguridad.")

    # Encriptar la contraseña antes de guardarla
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Crear usuario con contraseña encriptada
    new_user = UserDB(email=user.email, hashed_password=hashed_password, created_at=datetime.utcnow())

    
    # Insertar en la base de datos
    await db.users.insert_one(new_user.dict())
    logger.info(f"Usuario registrado: {user.email}")

    return {"message": "Usuario registrado exitosamente"}

def validate_password(password: str) -> bool:
    """Valida si la contraseña cumple con los requisitos de seguridad."""
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
    return bool(re.match(pattern, password))


"""Lógica para autenticación de usuarios con JWT."""


# Configuración del token JWT
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30
REFRESH_TOKEN_EXPIRATION_DAYS = 7

# Implementación simple de rate limiting
login_attempts = {}
MAX_ATTEMPTS = 5
ATTEMPT_WINDOW = 300  # 5 minutos en segundos

async def check_rate_limit(ip_address: str) -> bool:
    """Verifica si una IP ha excedido el límite de intentos de login."""
    current_time = datetime.utcnow().timestamp()
    
    # Limpiar intentos antiguos
    if ip_address in login_attempts:
        login_attempts[ip_address] = [attempt for attempt in login_attempts[ip_address] 
                                     if current_time - attempt < ATTEMPT_WINDOW]
    else:
        login_attempts[ip_address] = []
    
    # Verificar si ha excedido el límite
    if len(login_attempts[ip_address]) >= MAX_ATTEMPTS:
        logger.warning(f"Rate limit excedido para IP: {ip_address}")
        return False
    
    # Registrar nuevo intento
    login_attempts[ip_address].append(current_time)
    return True

async def authenticate_user(user: UserLogin):
    """Verifica credenciales y genera un token JWT."""
    # Buscar usuario en la base de datos
    user_data = await db.users.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

    # Verificar la contraseña
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_data["hashed_password"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")

    # Generar token JWT
    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Genera un token JWT con expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=TOKEN_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


"""Middleware para verificar autenticación con JWT en cada request."""

# Configuración de FastAPI para autenticación con OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Valida el JWT y extrae el usuario autenticado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return TokenData(email=email)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

