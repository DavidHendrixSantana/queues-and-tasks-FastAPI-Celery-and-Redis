# Email Queue System

Sistema de envío de correos con colas usando FastAPI, Celery y Redis.

## Características

- API FastAPI con endpoints para envío de correos
- Cola de tareas asíncrona con Celery
- Redis como broker de mensajes
- Seguimiento del estado de las tareas
- Envío de correos con SMTP

## Instalación

### 🐳 Opción 1: Docker (Recomendado)

1. **Configurar variables de entorno:**
```bash
cp .env.docker .env
# Editar .env con tus credenciales SMTP
```

2. **Iniciar con Docker:**
```bash
# Desarrollo
docker-compose -f docker-compose.dev.yml up

# Producción
docker-compose up -d
```

3. **Scripts de inicio rápido:**
```bash
# Windows
docker-start.bat

# Linux/macOS
chmod +x docker-start.sh
./docker-start.sh
```

### 📦 Opción 2: Instalación Local

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Iniciar servicios:**
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery worker
celery -A app.celery_app worker --loglevel=info

# Terminal 3: FastAPI
uvicorn app.main:app --reload
```

## Endpoints

- `POST /send-email` - Enviar correo electrónico
- `GET /status/{task_id}` - Consultar estado de tarea
- `GET /` - Documentación de la API

## Uso

### Enviar correo:
```bash
curl -X POST "http://localhost:8000/send-email" \
     -H "Content-Type: application/json" \
     -d '{
       "to": "destinatario@email.com",
       "subject": "Asunto del correo",
       "body": "Contenido del mensaje"
     }'
```

### Consultar estado:
```bash
curl "http://localhost:8000/status/task_id_aqui"
```

## 🚀 Despliegue

### Plataformas Recomendadas:
- **Railway** (recomendado): Soporte completo para Docker Compose
- **Render**: Web Services + Background Workers
- **DigitalOcean App Platform**: Aplicaciones multi-contenedor
- **AWS ECS/Fargate**: Para producción empresarial

⚠️ **Vercel NO es compatible** con esta aplicación (requiere workers persistentes)

Ver `deployment/README.md` para guías detalladas de despliegue.

## 🐳 Comandos Docker Útiles

```bash
# Ver logs
docker-compose logs -f

# Escalar workers
docker-compose up -d --scale celery_worker=3

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Limpiar volúmenes
docker-compose down -v
```

## 📊 Monitoreo

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Flower**: http://localhost:5555 (monitor de Celery)
- **Health**: http://localhost:8000/health
- **Redis**: localhost:6380 (puerto externo personalizable)