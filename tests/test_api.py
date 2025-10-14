import requests
import time
import json

def test_send_email_api():
    """Función para probar el endpoint de envío de correos"""
    
    # URL base de la API
    base_url = "http://localhost:8000"
    
    # Datos del correo de prueba
    email_data = {
        "to": "test@example.com",
        "subject": "Correo de prueba desde API",
        "body": "Este es un mensaje de prueba enviado desde la API de colas de correo."
    }
    
    print("🚀 Probando endpoint /send-email...")
    
    try:
        # Enviar solicitud POST
        response = requests.post(
            f"{base_url}/send-email",
            json=email_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            
            print(f"✅ Correo enviado exitosamente!")
            print(f"📋 Task ID: {task_id}")
            print(f"📄 Respuesta: {json.dumps(result, indent=2)}")
            
            # Probar endpoint de estado
            test_task_status(base_url, task_id)
            
        else:
            print(f"❌ Error en el envío: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_task_status(base_url, task_id):
    """Función para probar el endpoint de estado de tareas"""
    
    print(f"\n🔍 Consultando estado de la tarea {task_id}...")
    
    for i in range(5):  # Consultar 5 veces con intervalo
        try:
            response = requests.get(f"{base_url}/status/{task_id}")
            
            if response.status_code == 200:
                result = response.json()
                status = result["status"]
                
                print(f"📊 Estado {i+1}/5: {status}")
                
                if result.get("progress"):
                    print(f"🔄 Progreso: {result['progress']}")
                
                if result.get("result"):
                    print(f"✅ Resultado: {json.dumps(result['result'], indent=2)}")
                    break
                    
                if result.get("error"):
                    print(f"❌ Error: {result['error']}")
                    break
                
                if status in ["SUCCESS", "FAILURE"]:
                    break
                    
            else:
                print(f"❌ Error consultando estado: {response.status_code}")
                print(f"📄 Respuesta: {response.text}")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            break
        
        # Esperar antes de la siguiente consulta
        if i < 4:
            time.sleep(2)

def test_health_check():
    """Función para probar el endpoint de health check"""
    
    base_url = "http://localhost:8000"
    
    print("\n🏥 Probando health check...")
    
    try:
        response = requests.get(f"{base_url}/health")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check exitoso!")
            print(f"📄 Estado: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error en health check: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🧪 Iniciando pruebas de la API de Email Queue System\n")
    
    # Probar health check primero
    test_health_check()
    
    # Probar envío de correo
    test_send_email_api()
    
    print("\n🏁 Pruebas completadas!")