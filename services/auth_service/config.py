"""Configuración de conexión a MongoDB Atlas para Auth Service."""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URI de MongoDB Atlas desde variable de entorno
MONGO_URI = os.getenv("MONGO_URI")

# Crear el cliente de conexión a MongoDB Atlas
client = AsyncIOMotorClient(MONGO_URI)
db = client.auth_service  # Seleccionar la base de datos en Atlas
