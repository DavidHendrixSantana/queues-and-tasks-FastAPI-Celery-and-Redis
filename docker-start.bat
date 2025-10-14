@echo off
echo 🐳 Iniciando Email Queue System con Docker
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker no está instalado. Instálalo desde: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Verificar si Docker Compose está instalado
docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose no está instalado. Instálalo desde: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

REM Verificar si existe el archivo .env
if not exist .env (
    echo ⚠️  Archivo .env no encontrado.
    echo 📋 Copiando .env.docker como plantilla...
    copy .env.docker .env
    echo ✏️  Edita el archivo .env con tus configuraciones SMTP antes de continuar.
    echo 📖 Consulta docs/setup_guide.md para más detalles.
    pause
)

echo 🔧 Construyendo contenedores...
docker-compose build

echo 🚀 Iniciando servicios...
docker-compose up -d

echo ⏳ Esperando que los servicios estén listos...
timeout /t 10 /nobreak >nul

REM Verificar estado de los servicios
echo 📊 Estado de los servicios:
docker-compose ps

echo.
echo ✅ Sistema iniciado exitosamente!
echo.
echo 📍 URLs disponibles:
echo    API: http://localhost:8000
echo    Documentación: http://localhost:8000/docs
echo    Flower (Monitor): http://localhost:5555
echo.
echo 🔍 Para ver logs:
echo    docker-compose logs -f
echo.
echo 🛑 Para detener:
echo    docker-compose down
echo.
pause