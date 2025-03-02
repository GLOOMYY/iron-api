"""API Gateway - Maneja la comunicación entre microservicios."""
from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get("/")
async def root():
    """Verifica que el API Gateway está funcionando."""
    return {"message": "API Gateway funcionando 🚀"}


@app.get("/auth/users")
async def get_users():
    """Redirige la petición al servicio de autenticación."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://auth_service:8001/users")
    return response.json()


@app.get("/armors")
async def get_armors():
    """Redirige la petición al servicio de armaduras."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://armors_service:8002/armors")
    return response.json()


@app.get("/events")
async def get_events():
    """Redirige la petición al servicio de eventos."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://events_service:8003/events")
    return response.json()
