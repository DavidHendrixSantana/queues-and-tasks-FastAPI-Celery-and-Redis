from celery import Celery
from app.config import settings

def create_celery_app() -> Celery:
    celery_app = Celery(
        "email_queue_system",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
        include=['app.tasks']
    )
    
    # Configuración de Celery
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_routes={
            'app.tasks.send_email_task': 'email_queue'
        }
    )
    
    return celery_app

celery_app = create_celery_app()