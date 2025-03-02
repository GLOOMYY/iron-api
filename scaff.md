iron-api/
│── api_gateway.py # Punto de entrada global (FastAPI)
│── services/
│ ├── auth_service/ # Servicio de autenticación
│ ├── armors_service/ # Servicio de gestión de armaduras
│ ├── events_service/ # Servicio de historial de eventos
│── docker-compose.yml # Define múltiples contenedores
│── kubernetes/ # Archivos para orquestación en Kubernetes (opcional)
│── tests/ # Pruebas unitarias
