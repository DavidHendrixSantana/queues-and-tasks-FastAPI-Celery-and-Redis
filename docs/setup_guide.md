# Guía de Configuración

## Configuración de Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura las siguientes variables:

### Configuración de Redis
```
REDIS_URL=redis://localhost:6379/0
```

### Configuración de SMTP

#### Gmail
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_app_password  # Usar App Password, no la contraseña normal
SMTP_USE_TLS=true
```

#### Outlook/Hotmail
```
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=tu_email@outlook.com
SMTP_PASSWORD=tu_contraseña
SMTP_USE_TLS=true
```

#### Servidor SMTP Personalizado
```
SMTP_HOST=mail.tu-dominio.com
SMTP_PORT=587
SMTP_USER=tu_email@tu-dominio.com
SMTP_PASSWORD=tu_contraseña
SMTP_USE_TLS=true
```

## Configuración de Gmail

### 1. Habilitar Autenticación de 2 Factores
1. Ve a tu cuenta de Google
2. Habilita la autenticación de 2 factores

### 2. Crear App Password
1. Ve a Configuración de Cuenta > Seguridad
2. En "Iniciar sesión en Google", selecciona "Contraseñas de aplicaciones"
3. Genera una nueva contraseña para "Aplicación personalizada"
4. Usa esta contraseña en `SMTP_PASSWORD`

## Instalación de Redis

### Windows
1. Descargar desde: https://github.com/microsoftarchive/redis/releases
2. Instalar y ejecutar: `redis-server.exe`

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

### macOS
```bash
brew install redis
brew services start redis
```

### Docker
```bash
docker run -d -p 6379:6379 redis:alpine
```

## Configuración de Celery

### Opciones Avanzadas

Puedes personalizar la configuración de Celery en `app/celery_app.py`:

```python
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    
    # Configuraciones adicionales
    worker_concurrency=4,  # Número de procesos worker
    task_soft_time_limit=300,  # Timeout suave (5 min)
    task_time_limit=600,  # Timeout duro (10 min)
    task_routes={
        'app.tasks.send_email_task': 'email_queue'
    },
    
    # Configuración de reintentos
    task_annotations={
        'app.tasks.send_email_task': {
            'rate_limit': '10/m',  # 10 tareas por minuto
            'max_retries': 3,
            'default_retry_delay': 60  # 1 minuto entre reintentos
        }
    }
)
```

## Configuración de Producción

### 1. Usar un Servidor ASGI
```bash
# Gunicorn con Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# O usar Uvicorn directamente
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 2. Configurar Redis con Autenticación
```
REDIS_URL=redis://:password@localhost:6379/0
```

### 3. Usar Variables de Entorno del Sistema
En lugar del archivo `.env`, configura las variables directamente en el sistema:

```bash
export REDIS_URL="redis://localhost:6379/0"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="tu_email@gmail.com"
export SMTP_PASSWORD="tu_app_password"
export SMTP_USE_TLS="true"
```

### 4. Supervisord para Celery Worker
```ini
[program:celery_worker]
command=celery -A app.celery_app worker --loglevel=info
directory=/path/to/your/app
user=your_user
numprocs=1
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
```

### 5. Nginx como Reverse Proxy
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```