"""Manejo de la conexión a MongoDB."""

import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener la URI de MongoDB desde las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    logger.error("MONGO_URI no está configurada en las variables de entorno")
    raise ValueError("MONGO_URI environment variable is not set")

try:
    # Crear el cliente de MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    
    # Verificar la conexión
    client.admin.command('ping')
    logger.info("Conexión exitosa a MongoDB")
    
    # Seleccionar la base de datos
    db = client["auth_service"]
    
except Exception as e:
    logger.error(f"Error al conectar a MongoDB: {e}")
    raise
