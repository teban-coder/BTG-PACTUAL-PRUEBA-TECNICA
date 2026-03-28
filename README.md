# BTG Backend - Prueba Técnica

## Tecnologías usadas
- FastAPI
- MongoDB
- JWT Authentication
- Docker

## Seguridad y autenticación
- Autenticación con JWT
- Autorización por roles (user/admin)
- Encriptación de contraseñas

## Funcionalidades
- Suscripción a fondos
- Cancelación de suscripción
- Historial de transacciones
- Notificaciones (email/SMS simuladas)

## Tests
Ejecutar:
pytest

## Docker
docker build -t btg-backend .
docker run -p 8000:8000 btg-backend

## AWS Deploy
Desplegar usando CloudFormation con el archivo:

template.yaml

- EC2
- Docker container con la API

## Notas
- Las notificaciones están desacopladas mediante un servicio
- El sistema está diseñado para escalar fácilmente a AWS SNS/SES
