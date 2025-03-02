"""Microservicio en FastAPI - Ejemplo básico."""

from fastapi import FastAPI

# Crear instancia de FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    """Endpoint raíz: Verifica que el servicio está funcionando."""
    return {"message": "El servicio está funcionando 🚀"}

@app.get("/health")
def health_check():
    """Endpoint de salud: Permite a Docker verificar si el servicio está activo."""
    return {"status": "ok"}
