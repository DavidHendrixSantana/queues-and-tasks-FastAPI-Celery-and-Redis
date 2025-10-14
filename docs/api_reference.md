# Documentación de la API

## Endpoints Disponibles

### 1. POST /send-email

Envía un correo electrónico de forma asíncrona usando colas.

**Request Body:**
```json
{
  "to": "destinatario@email.com",
  "subject": "Asunto del correo",
  "body": "Contenido del mensaje",
  "from_email": "remitente@email.com" // Opcional
}
```

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PENDING",
  "message": "Tarea de envío de correo creada. ID: 550e8400-e29b-41d4-a716-446655440000"
}
```

**Ejemplo con curl:**
```bash
curl -X POST "http://localhost:8000/send-email" \
     -H "Content-Type: application/json" \
     -d '{
       "to": "test@example.com",
       "subject": "Correo de prueba",
       "body": "Este es un mensaje de prueba"
     }'
```

### 2. GET /status/{task_id}

Consulta el estado y progreso de una tarea de envío de correo.

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "SUCCESS",
  "result": {
    "success": true,
    "message": "Correo enviado exitosamente a test@example.com",
    "to": "test@example.com",
    "subject": "Correo de prueba"
  },
  "error": null,
  "progress": null
}
```

**Estados posibles:**
- `PENDING`: Tarea en cola
- `STARTED`: Tarea iniciada
- `PROGRESS`: Tarea en progreso
- `SUCCESS`: Tarea completada exitosamente
- `FAILURE`: Tarea falló
- `RETRY`: Tarea reintentándose
- `REVOKED`: Tarea cancelada

**Ejemplo con curl:**
```bash
curl "http://localhost:8000/status/550e8400-e29b-41d4-a716-446655440000"
```

### 3. GET /health

Verifica el estado de la API y sus componentes.

**Response:**
```json
{
  "status": "healthy",
  "celery_workers": 1,
  "redis_connection": "connected"
}
```

### 4. GET /

Información general de la API.

**Response:**
```json
{
  "message": "Email Queue System API",
  "version": "1.0.0",
  "endpoints": {
    "send_email": "/send-email",
    "task_status": "/status/{task_id}",
    "docs": "/docs"
  }
}
```

## Estados de Progreso

Durante el envío de correos, puedes monitorear el progreso:

1. **connecting**: Conectando al servidor SMTP
2. **authenticating**: Autenticando usuario
3. **sending**: Enviando correo al destinatario
4. **failed**: Error en el envío

## Códigos de Error

- `400`: Solicitud malformada
- `404`: Tarea no encontrada
- `500`: Error interno del servidor

## Documentación Interactiva

Visita `http://localhost:8000/docs` para la documentación interactiva de Swagger.