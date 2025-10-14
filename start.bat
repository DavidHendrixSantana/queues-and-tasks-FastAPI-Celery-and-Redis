@echo off
echo Iniciando Email Queue System...
echo.

echo [1/4] Verificando dependencias...
pip install -r requirements.txt

echo.
echo [2/4] Iniciando Redis (asegurate de tener Redis instalado)...
echo Ejecuta en otra terminal: redis-server
pause

echo.
echo [3/4] Iniciando Celery Worker...
start "Celery Worker" cmd /k "celery -A app.celery_app worker --loglevel=info"

echo.
echo [4/4] Iniciando FastAPI...
python start_api.py