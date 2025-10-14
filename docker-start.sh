#!/bin/bash

echo "🐳 Iniciando Email Queue System con Docker"
echo

# Verificar si Docker y Docker Compose están instalados
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Instálalo desde: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Instálalo desde: https://docs.docker.com/compose/install/"
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado."
    echo "📋 Copiando .env.docker como plantilla..."
    cp .env.docker .env
    echo "✏️  Edita el archivo .env con tus configuraciones SMTP antes de continuar."
    echo "📖 Consulta docs/setup_guide.md para más detalles."
    read -p "Presiona Enter cuando hayas configurado .env..."
fi

echo "🔧 Construyendo contenedores..."
docker-compose build

echo "🚀 Iniciando servicios..."
docker-compose up -d

echo "⏳ Esperando que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

echo
echo "✅ Sistema iniciado exitosamente!"
echo
echo "📍 URLs disponibles:"
echo "   API: http://localhost:8000"
echo "   Documentación: http://localhost:8000/docs"
echo "   Flower (Monitor): http://localhost:5555"
echo
echo "🔍 Para ver logs:"
echo "   docker-compose logs -f"
echo
echo "🛑 Para detener:"
echo "   docker-compose down"