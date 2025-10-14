import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import current_task
from app.celery_app import celery_app
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def send_email_sync(to_email: str, subject: str, body: str, from_email: str = None):
    """Función síncrona para enviar correos electrónicos usando smtplib"""
    if not from_email:
        from_email = settings.SMTP_USER
    
    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    
    # Agregar el cuerpo del mensaje
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Actualizar progreso
        if current_task:
            current_task.update_state(
                state='PROGRESS',
                meta={'step': 'connecting', 'message': 'Conectando al servidor SMTP'}
            )
        
        # Usar la configuración que sabemos que funciona
        if settings.SMTP_PORT == 465:
            # Puerto 465: SSL directo con smtplib
            logger.info("Conectando con SSL directo (puerto 465)")
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, 465)
        else:
            # Puerto 587: STARTTLS con smtplib
            logger.info("Conectando con STARTTLS (puerto 587)")
            server = smtplib.SMTP(settings.SMTP_HOST, 587)
            server.starttls()
        
        if current_task:
            current_task.update_state(
                state='PROGRESS',
                meta={'step': 'authenticating', 'message': 'Autenticando usuario'}
            )
        
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        
        if current_task:
            current_task.update_state(
                state='PROGRESS',
                meta={'step': 'sending', 'message': f'Enviando correo a {to_email}'}
            )
        
        # Enviar el correo
        server.send_message(message)
        server.quit()
        
        logger.info(f"Correo enviado exitosamente a {to_email}")
        return {
            "success": True,
            "message": f"Correo enviado exitosamente a {to_email}",
            "to": to_email,
            "subject": subject
        }
        
    except Exception as e:
        logger.error(f"Error enviando correo a {to_email}: {str(e)}")
        raise Exception(f"Error enviando correo: {str(e)}")

@celery_app.task(bind=True, name='send_email_task')
def send_email_task(self, to_email: str, subject: str, body: str, from_email: str = None):
    """Tarea de Celery para enviar correos electrónicos"""
    try:
        # Actualizar estado inicial
        self.update_state(
            state='STARTED',
            meta={'step': 'initializing', 'message': 'Iniciando envío de correo'}
        )
        
        # Usar función síncrona con smtplib (más confiable)
        result = send_email_sync(to_email, subject, body, from_email)
        
        return result
        
    except Exception as e:
        logger.error(f"Error en tarea de envío de correo: {str(e)}")
        # Return error instead of raising to avoid Celery exception issues
        return {
            "success": False,
            "error": str(e),
            "message": f"Error enviando correo: {str(e)}"
        }