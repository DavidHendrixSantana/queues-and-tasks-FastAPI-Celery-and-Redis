#!/bin/bash
# init-env.sh - Script para inicializar archivos de configuración en Docker

echo "🔧 Inicializando configuración de entorno..."

# Verificar si existe .env, si no, usar .env.docker como base
if [ ! -f /app/.env ]; then
    echo "📋 No se encontró .env, usando .env.docker como base..."
    if [ -f /app/.env.docker ]; then
        cp /app/.env.docker /app/.env
        echo "✅ Archivo .env creado desde .env.docker"
    else
        echo "⚠️  No se encontró .env.docker, usando valores por defecto..."
        cat > /app/.env << EOF
# Configuración por defecto
REDIS_URL=redis://redis:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_SSL=true
SMTP_USE_TLS=false
IS_DOCKER=true
LOG_LEVEL=INFO
EOF
    fi
else
    echo "✅ Archivo .env encontrado"
fi

# Mostrar configuración (sin mostrar password)
echo "📊 Configuración actual:"
echo "   REDIS_URL: $(grep REDIS_URL /app/.env | cut -d'=' -f2)"
echo "   SMTP_HOST: $(grep SMTP_HOST /app/.env | cut -d'=' -f2)"
echo "   SMTP_PORT: $(grep SMTP_PORT /app/.env | cut -d'=' -f2)"
echo "   SMTP_USER: $(grep SMTP_USER /app/.env | cut -d'=' -f2)"
echo "   SMTP_USE_SSL: $(grep SMTP_USE_SSL /app/.env | cut -d'=' -f2)"

# Verificar variables críticas
if [ -z "$(grep SMTP_USER /app/.env | cut -d'=' -f2)" ]; then
    echo "⚠️  ADVERTENCIA: SMTP_USER no está configurado"
    echo "   Configura las variables SMTP para envío de correos"
fi

if [ -z "$(grep SMTP_PASSWORD /app/.env | cut -d'=' -f2)" ]; then
    echo "⚠️  ADVERTENCIA: SMTP_PASSWORD no está configurado"
    echo "   Configura las variables SMTP para envío de correos"
fi

echo "🚀 Configuración lista!"