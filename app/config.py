import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

class Settings:
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_USE_SSL: bool = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    
    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Email Queue System")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Docker/Production flags
    IS_DOCKER: bool = os.getenv("IS_DOCKER", "false").lower() == "true"

settings = Settings()