from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import EmailRequest, TaskResponse, TaskStatusResponse, TaskStatus
from app.tasks import send_email_task
from app.celery_app import celery_app
from celery.result import AsyncResult
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="Email Queue System",
    description="Sistema de envío de correos con colas usando Celery y Redis",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Email Queue System API",
        "version": "1.0.0",
        "endpoints": {
            "send_email": "/send-email",
            "task_status": "/status/{task_id}",
            "docs": "/docs"
        }
    }

@app.post("/send-email", response_model=TaskResponse)
async def send_email(email_request: EmailRequest):
    """
    Endpoint para enviar correos electrónicos de forma asíncrona
    
    - **to**: Email del destinatario
    - **subject**: Asunto del correo
    - **body**: Contenido del mensaje
    - **from_email**: Email del remitente (opcional, usa el configurado por defecto)
    """
    try:
        logger.info(f"Recibida solicitud de envío de correo para: {email_request.to}")
        
        # Enviar tarea a Celery
        task = send_email_task.delay(
            to_email=str(email_request.to),
            subject=email_request.subject,
            body=email_request.body,
            from_email=email_request.from_email
        )
        
        logger.info(f"Tarea creada con ID: {task.id}")
        
        return TaskResponse(
            task_id=task.id,
            status="PENDING",
            message=f"Tarea de envío de correo creada. ID: {task.id}"
        )
        
    except Exception as e:
        logger.error(f"Error creando tarea de envío de correo: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Endpoint para consultar el estado de una tarea
    
    - **task_id**: ID de la tarea a consultar
    """
    try:
        # Obtener resultado de la tarea
        task_result = AsyncResult(task_id, app=celery_app)
        
        if not task_result:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea con ID {task_id} no encontrada"
            )
        
        # Mapear estados de Celery a nuestro enum
        status = task_result.status
        
        response = TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus(status) if status in TaskStatus.__members__ else TaskStatus.PENDING
        )
        
        if task_result.successful():
            response.result = task_result.result
        elif task_result.failed():
            response.error = str(task_result.info)
        elif status == 'PROGRESS':
            response.progress = task_result.info
        else:
            response.progress = task_result.info if task_result.info else None
        
        logger.info(f"Estado de tarea {task_id}: {status}")
        
        return response
        
    except ValueError as e:
        # Error de enum inválido
        raise HTTPException(
            status_code=400,
            detail=f"Estado de tarea inválido: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error consultando estado de tarea {task_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    try:
        # Verificar conexión con Redis/Celery
        inspection = celery_app.control.inspect()
        stats = inspection.stats()
        
        return {
            "status": "healthy",
            "celery_workers": len(stats) if stats else 0,
            "redis_connection": "connected" if stats else "disconnected"
        }
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000,
        log_level=settings.LOG_LEVEL.lower(),
        reload=not settings.IS_DOCKER  # Disable reload in Docker
    )