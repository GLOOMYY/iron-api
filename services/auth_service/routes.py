"""Rutas para autenticación de usuarios."""

from fastapi import APIRouter, Depends
from service import create_user, authenticate_user, get_current_user
from models import UserCreate, UserLogin, Token, TokenData

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    """Registra un usuario en la base de datos."""
    return await create_user(user)

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Autentica un usuario y devuelve un token JWT."""
    return await authenticate_user(user)

@router.get("/me", response_model=TokenData)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    """Devuelve la información del usuario autenticado."""
    return current_user
