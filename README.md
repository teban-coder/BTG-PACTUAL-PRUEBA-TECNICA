BTG Backend - Prueba Técnica
Descripción
Backend desarrollado con FastAPI que permite la gestión de suscripciones a fondos, autenticación con JWT y manejo de transacciones.

Tecnologías usadas:

FastAPI

MongoDB

Docker

JWT Authentication

AWS CloudFormation

Seguridad:

Autenticación con JWT

Autorización por roles (user/admin)

Encriptación de contraseñas


Funcionalidades:

Suscripción a fondos

Cancelación de suscripción

Historial de transacciones

Notificaciones (simuladas)


Tests:

pytest

Ejecución local:

docker build -t btg-backend .

docker run -p 8000:8000 btg-backend


Despliegue en AWS:

El despliegue se realiza utilizando AWS CloudFormation.

Requisitos:

Cuenta en AWS

AWS CLI instalado

Credenciales configuradas:

aws configure

Despliegue:

Ejecutar el siguiente comando:

aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name btg-backend \
  --capabilities CAPABILITY_NAMED_IAM

Verificación:

Ir a AWS CloudFormation

Seleccionar el stack btg-backend

Ir a la pestaña Outputs

Copiar la IP pública generada


Acceso a la API:

Abrir en navegador:

http://<IP_PUBLICA>:8000/docs

Arquitectura

Instancia EC2 (Amazon Linux)

Contenedor Docker con FastAPI

Contenedor Docker con MongoDB

Comunicación interna entre servicios con Docker Compose