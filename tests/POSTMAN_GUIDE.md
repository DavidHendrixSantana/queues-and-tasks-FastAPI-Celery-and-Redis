# 📮 Guía de Pruebas con Postman

## 🎯 **Archivos de Postman incluidos:**

1. **`Email_Queue_System_API.postman_collection.json`** - Colección completa de tests
2. **`Email_Queue_System.postman_environment.json`** - Variables de entorno

## 🚀 **Importar en Postman**

### **Paso 1: Importar Colección**
1. Abrir Postman
2. Click en **"Import"**
3. Seleccionar **"Upload Files"**
4. Importar `Email_Queue_System_API.postman_collection.json`

### **Paso 2: Importar Environment**
1. En Postman, ir a **"Environments"** (⚙️)
2. Click **"Import"**
3. Seleccionar `Email_Queue_System.postman_environment.json`
4. Activar el environment "Email Queue System Environment"

### **Paso 3: Configurar Variables**
Edita las variables del environment:
- **`base_url`**: `http://localhost:8000` (por defecto)
- **`test_email`**: Tu email real para recibir pruebas

## 📋 **Tests Incluidos**

### **1. Health Check** 🏥
- **Método**: GET `/health`
- **Propósito**: Verificar que la API, Redis y Celery estén funcionando
- **Tests automáticos**:
  - Status code 200
  - Service status = "healthy" 
  - Redis connected
  - Celery workers > 0

### **2. API Root Information** 🏠
- **Método**: GET `/`
- **Propósito**: Obtener información general de la API
- **Tests automáticos**:
  - Status code 200
  - Contiene message, version, endpoints

### **3. Send Email - Valid Request** ✅
- **Método**: POST `/send-email`
- **Propósito**: Enviar correo válido y obtener task_id
- **Tests automáticos**:
  - Status code 200
  - Respuesta contiene task_id
  - Status = "PENDING"
  - **Guarda task_id** para tests posteriores

### **4. Check Task Status - Immediate** 🔍
- **Método**: GET `/status/{{task_id}}`
- **Propósito**: Consultar estado inmediatamente después del envío
- **Tests automáticos**:
  - Status code 200
  - Task_id coincide con el enviado

### **5. Send Email - Invalid Format** ❌
- **Método**: POST `/send-email`
- **Body**: Email con formato inválido
- **Tests automáticos**:
  - Status code 422 (Validation Error)
  - Contiene detalle de error

### **6. Send Email - Missing Fields** ❌
- **Método**: POST `/send-email`
- **Body**: Falta subject y body
- **Tests automáticos**:
  - Status code 422
  - Error de validación

### **7. Check Non-existent Task** 🔍
- **Método**: GET `/status/non-existent-task-id-12345`
- **Propósito**: Verificar comportamiento con task inexistente
- **Tests automáticos**:
  - Status code 200
  - Status = "PENDING" (comportamiento esperado de Celery)

### **8. Send Multiple Emails** 📨📨
- **Método**: POST `/send-email`
- **Propósito**: Probar procesamiento en paralelo
- **Tests automáticos**:
  - Status code 200
  - **Guarda segundo task_id**

### **9. Check Second Task** 🔍
- **Método**: GET `/status/{{task_id_2}}`
- **Propósito**: Verificar segunda tarea
- **Tests automáticos**:
  - Status code 200
  - Task_id correcto

### **10. Send HTML Email** 🎨
- **Método**: POST `/send-email`
- **Body**: Contenido HTML con estilos
- **Propósito**: Probar diferentes tipos de contenido

## 🏃‍♂️ **Ejecutar Pruebas**

### **Opción A: Ejecutar Individual**
- Seleccionar cada request y hacer click en **"Send"**
- Ver tests automáticos en la pestaña **"Test Results"**

### **Opción B: Ejecutar Collection**
1. Click derecho en la colección
2. **"Run collection"**
3. Seleccionar environment
4. Click **"Run Email Queue System API"**
5. Ver resultados en tiempo real

### **Opción C: Ejecutar desde línea de comandos**
```bash
# Instalar newman (CLI de Postman)
npm install -g newman

# Ejecutar colección
newman run Email_Queue_System_API.postman_collection.json \
       -e Email_Queue_System.postman_environment.json \
       --reporters cli,htmlextra \
       --reporter-htmlextra-export results.html
```

## 🔧 **Configuración Previa**

### **1. Servicios ejecutándose**
```bash
# Iniciar con Docker
docker-compose -f docker-compose.dev.yml up -d

# Verificar servicios
docker-compose -f docker-compose.dev.yml ps
```

### **2. Variables correctas**
- `base_url`: URL donde corre tu API
- `test_email`: Email válido para recibir correos de prueba

### **3. SMTP configurado (opcional)**
Para que los correos se envíen realmente:
- Configurar `.env` con credenciales SMTP reales
- Usar App Password de Gmail

## 📊 **Interpretación de Resultados**

### **✅ Success States:**
- **PENDING**: Tarea en cola
- **STARTED**: Tarea iniciada
- **SUCCESS**: Correo enviado exitosamente

### **❌ Error States:**
- **FAILURE**: Error en envío (normal con SMTP mal configurado)
- **422**: Error de validación (esperado para pruebas negativas)

### **🔄 Progress States:**
Puedes ver progreso en tiempo real:
```json
{
  "status": "PROGRESS",
  "progress": {
    "step": "connecting",
    "message": "Conectando al servidor SMTP"
  }
}
```

## 🐛 **Troubleshooting**

### **Connection Refused**
```bash
# Verificar que la API esté corriendo
curl http://localhost:8000/health
```

### **Tests Failing**
- Verificar variables de environment
- Asegurarse que los servicios estén up
- Revisar logs: `docker-compose logs -f`

### **SMTP Errors (normal)**
Los errores de SMTP son esperados si no configuras credenciales reales:
```json
{
  "error": "Error connecting to smtp.gmail.com on port 587"
}
```

## 🚀 **Alternativa: Test Automático con Python**

Si prefieres no usar Postman:

```bash
# Ejecutar tests automatizados con Python
python tests/test_api_complete.py

# Con parámetros personalizados
python tests/test_api_complete.py --url http://localhost:8000 --email tu_email@gmail.com
```

## 📈 **Métricas de Rendimiento**

Los tests incluyen verificaciones de:
- **Response time** < 5000ms
- **Status codes** correctos
- **Data validation** automática
- **Error handling** apropiado

¡Disfruta probando tu Email Queue System! 🎉