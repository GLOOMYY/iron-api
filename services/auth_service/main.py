"""Microservicio en FastAPI - Ejemplo básico."""

from fastapi import FastAPI, Depends, HTTPException
from routes import router 
from config import db, client

# Crear instancia de FastAPI
app = FastAPI(title="Auth Service", version="0.9")

app.include_router(router, prefix="/auth")

@app.get("/")
def read_root():
    """Endpoint raíz: Verifica que el servicio está funcionando."""
    return {"message": "El auth_service está funcionando 🚀"}

@app.get("/health")
async def health_check():
    """Endpoint de salud: Verifica si el servicio y la base de datos están activos."""
    try:
        # Verificar conexión a MongoDB
        await client.admin.command('ping')
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection error: {str(e)}")
