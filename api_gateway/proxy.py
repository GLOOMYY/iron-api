import httpx

async def forward_request(service_url: str, path: str, request: dict):
    """Reenvía una petición a un servicio y devuelve la respuesta."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{service_url}/{path}", params=request)
        return response.json()