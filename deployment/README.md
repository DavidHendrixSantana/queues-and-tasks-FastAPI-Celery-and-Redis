# Guía de Despliegue

## ⚠️ IMPORTANTE: Limitaciones de Vercel

**Vercel NO es compatible** con esta aplicación porque:

1. **Arquitectura Serverless**: Vercel ejecuta funciones serverless que no pueden mantener workers persistentes como Celery
2. **Sin Redis integrado**: No tiene soporte nativo para Redis
3. **Sin background jobs**: No puede ejecutar tareas de larga duración en segundo plano
4. **Timeout de funciones**: Las funciones tienen límites de tiempo de ejecución

## 🎯 Plataformas Recomendadas

### 1. **Railway** (Recomendado) 🚂

**Ventajas:**
- Soporte completo para Docker Compose
- Redis integrado
- Deploy automático desde Git
- Configuración simple

**Pasos:**
1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar repositorio GitHub
3. Railway detecta automáticamente `docker-compose.yml`
4. Configurar variables de entorno:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=tu_email@gmail.com
   SMTP_PASSWORD=tu_app_password
   SMTP_USE_TLS=true
   ```
5. Deploy automático

### 2. **Render** 🎨

**Pasos:**
1. Crear Web Service para API
2. Crear Background Worker para Celery
3. Usar Redis Cloud como base de datos
4. Configurar variables de entorno

### 3. **DigitalOcean App Platform** 🌊

**Pasos:**
1. Crear App desde repositorio
2. Configurar servicios múltiples
3. Usar DigitalOcean Managed Redis
4. Deploy automático

### 4. **AWS ECS/Fargate** ☁️

**Para aplicaciones de producción:**
1. Usar AWS ECS con Fargate
2. ElastiCache para Redis
3. Application Load Balancer
4. CloudWatch para logs

### 5. **Google Cloud Run** 🏃‍♂️

**Pasos:**
1. Construir imagen Docker
2. Subir a Container Registry
3. Usar Memorystore para Redis
4. Deploy en Cloud Run

## 🐳 Despliegue Local con Docker

### Desarrollo:
```bash
# Clonar repositorio
git clone <repo-url>
cd queues-and-tasks

# Configurar variables de entorno
cp .env.docker .env
# Editar .env con tus credenciales SMTP

# Iniciar servicios
docker-compose -f docker-compose.dev.yml up
```

### Producción:
```bash
# Iniciar servicios de producción
docker-compose up -d

# Ver logs
docker-compose logs -f

# Escalar workers
docker-compose up -d --scale celery_worker=3
```

## 🔧 Configuración para Railway

### railway.json:
```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "restartPolicyType": "on-failure",
    "sleepApplication": false
  }
}
```

### Variables de Entorno Railway:
```
REDIS_URL=${{Redis.REDIS_URL}}
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password
SMTP_USE_TLS=true
```

## 🔧 Configuración para Render

### render.yaml:
```yaml
services:
  - type: web
    name: email-queue-api
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: REDIS_URL
        fromDatabase:
          name: redis
          property: connectionString
      - key: SMTP_HOST
        value: smtp.gmail.com
      - key: SMTP_PORT
        value: 587

  - type: worker
    name: email-queue-worker
    env: docker
    dockerfilePath: ./Dockerfile.celery
    envVars:
      - key: REDIS_URL
        fromDatabase:
          name: redis
          property: connectionString

databases:
  - name: redis
    databaseName: redis
    user: redis
```

## 📊 Monitoreo

### Flower Dashboard
- Accesible en puerto 5555
- Monitorea workers de Celery
- Estadísticas de tareas

### Health Checks
```bash
# API Health
curl http://localhost:8000/health

# Redis Health
docker exec email_queue_redis redis-cli ping

# Celery Health
docker exec email_queue_worker celery -A app.celery_app inspect ping
```

## 🔒 Seguridad en Producción

1. **Variables de Entorno**: Nunca commitear credenciales
2. **HTTPS**: Usar certificados SSL
3. **Redis Auth**: Configurar autenticación
4. **Rate Limiting**: Implementar límites de requests
5. **Firewall**: Restringir acceso a puertos

## 📈 Escalabilidad

### Horizontal Scaling:
```bash
# Múltiples workers
docker-compose up -d --scale celery_worker=5

# Load balancer
# Usar nginx o cloud load balancer
```

### Optimizaciones:
- Pool de conexiones Redis
- Batch processing para emails
- Caching de configuraciones
- Monitoring con Prometheus