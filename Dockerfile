# Dockerfile para la aplicación FastAPI
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ ./app/
COPY start_api.py .

# Copiar archivos de configuración y script de inicialización
COPY .env.example .env.example
COPY .env.docker .env.docker
COPY init-env.sh .
RUN chmod +x init-env.sh

# Copiar .env si existe, sino preparar para usar .env.docker
COPY .env* ./
RUN ./init-env.sh

# Crear usuario no root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "start_api.py"]