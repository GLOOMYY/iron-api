# Usa Python 3.11 Slim como base
FROM python:3.11-slim

WORKDIR /app

# Variables de entorno para mejorar rendimiento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copia el archivo de dependencias y las instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del API Gateway
COPY . .

# Crear usuario no root por seguridad
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expone el puerto 8000 para el API Gateway
EXPOSE 8000

# Agrega un healthcheck para monitoreo
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para iniciar el API Gateway con FastAPI y Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
