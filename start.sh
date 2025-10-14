#!/bin/bash

echo "🚀 Iniciando Email Queue System..."
echo

echo "📦 [1/4] Instalando dependencias..."
pip install -r requirements.txt

echo
echo "🔴 [2/4] Iniciando Redis..."
echo "Asegúrate de tener Redis instalado y ejecuta: redis-server"
echo "Presiona Enter cuando Redis esté ejecutándose..."
read

echo
echo "👷 [3/4] Iniciando Celery Worker..."
gnome-terminal -- bash -c "celery -A app.celery_app worker --loglevel=info; exec bash" 2>/dev/null || \
xterm -e "celery -A app.celery_app worker --loglevel=info" 2>/dev/null || \
echo "Ejecuta en otra terminal: celery -A app.celery_app worker --loglevel=info"

echo
echo "🌐 [4/4] Iniciando FastAPI..."
python start_api.py