from fastapi import APIRouter, Depends
from proxy import forward_request

router = APIRouter()

@router.get("/auth/{path:path}")
async def auth_proxy(path: str, request: dict):
    """Reenvía las solicitudes de autenticación al microservicio auth_service."""
    return await forward_request("http://auth_service:8001", path, request)

@router.get("/armors/{path:path}")
async def armors_proxy(path: str, request: dict):
    """Reenvía las solicitudes de armaduras al microservicio armors_service."""
    return await forward_request("http://armors_service:8002", path, request)

@router.get("/events/{path:path}")
async def events_proxy(path: str, request: dict):
    """Reenvía las solicitudes de eventos al microservicio events_service."""
    return await forward_request("http://events_service:8003", path, request)
