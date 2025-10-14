import requests
import json
import time
from typing import Dict, Any

class EmailQueueSystemTester:
    def __init__(self, base_url: str = "http://localhost:8000", test_email: str = "dasalvasuper@gmail.com"):
        self.base_url = base_url
        self.test_email = test_email
        self.session = requests.Session()
        self.task_ids = {}
        
    def print_test_header(self, test_name: str, test_number: int):
        """Imprime el encabezado de cada test"""
        print(f"\n{'='*60}")
        print(f"🧪 Test {test_number}: {test_name}")
        print('='*60)
    
    def print_result(self, success: bool, message: str):
        """Imprime el resultado de un test"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {message}")
    
    def test_1_health_check(self) -> bool:
        """Test 1: Health Check"""
        self.print_test_header("Health Check", 1)
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            # Verificar status code
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            # Verificar que el servicio esté healthy
            if data.get("status") != "healthy":
                self.print_result(False, f"Expected status 'healthy', got '{data.get('status')}'")
                return False
            
            # Verificar Redis connection
            if data.get("redis_connection") != "connected":
                self.print_result(False, f"Redis not connected: {data.get('redis_connection')}")
                return False
            
            # Verificar Celery workers
            if data.get("celery_workers", 0) <= 0:
                self.print_result(False, f"No Celery workers available: {data.get('celery_workers')}")
                return False
            
            self.print_result(True, f"Service healthy - Redis: {data['redis_connection']}, Workers: {data['celery_workers']}")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_2_api_root(self) -> bool:
        """Test 2: API Root Information"""
        self.print_test_header("API Root Information", 2)
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            required_fields = ['message', 'version', 'endpoints']
            
            for field in required_fields:
                if field not in data:
                    self.print_result(False, f"Missing required field: {field}")
                    return False
            
            self.print_result(True, f"API Info - {data['message']} v{data['version']}")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_3_send_email_valid(self) -> bool:
        """Test 3: Send Email - Valid Request"""
        self.print_test_header("Send Email - Valid Request", 3)
        
        email_data = {
            "to": self.test_email,
            "subject": "Prueba desde Python - Email Queue System",
            "body": "¡Hola! Este es un correo de prueba enviado desde Python usando el sistema de colas de correo.\n\nCaracterísticas probadas:\n- FastAPI como API\n- Celery como sistema de colas\n- Redis como broker de mensajes\n- Docker para containerización\n\n¡El sistema funciona perfectamente!",
            "from_email": self.test_email
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json=email_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            if "task_id" not in data:
                self.print_result(False, "Response missing task_id")
                return False
            
            if data.get("status") != "PENDING":
                self.print_result(False, f"Expected status 'PENDING', got '{data.get('status')}'")
                return False
            
            # Guardar task_id para pruebas posteriores
            self.task_ids['main'] = data["task_id"]
            
            self.print_result(True, f"Email queued successfully - Task ID: {data['task_id']}")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_4_check_task_status(self) -> bool:
        """Test 4: Check Task Status"""
        self.print_test_header("Check Task Status - Immediate", 4)
        
        if 'main' not in self.task_ids:
            self.print_result(False, "No task_id available from previous test")
            return False
        
        task_id = self.task_ids['main']
        
        try:
            response = self.session.get(f"{self.base_url}/status/{task_id}", timeout=5)
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            if data.get("task_id") != task_id:
                self.print_result(False, f"Task ID mismatch: expected {task_id}, got {data.get('task_id')}")
                return False
            
            status = data.get("status", "UNKNOWN")
            self.print_result(True, f"Task status retrieved: {status}")
            
            # Si hay resultado o error, mostrarlo
            if data.get("result"):
                print(f"   📄 Result: {data['result']}")
            if data.get("error"):
                print(f"   ⚠️ Error: {data['error']}")
            if data.get("progress"):
                print(f"   🔄 Progress: {data['progress']}")
            
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_5_send_email_invalid_format(self) -> bool:
        """Test 5: Send Email - Invalid Email Format"""
        self.print_test_header("Send Email - Invalid Email Format", 5)
        
        email_data = {
            "to": "invalid-email-format",
            "subject": "Test Subject",
            "body": "Test Body"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json=email_data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code != 422:
                self.print_result(False, f"Status code expected 422, got {response.status_code}")
                return False
            
            data = response.json()
            
            if "detail" not in data:
                self.print_result(False, "Response missing validation error details")
                return False
            
            self.print_result(True, "Validation error correctly returned for invalid email format")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_6_send_email_missing_fields(self) -> bool:
        """Test 6: Send Email - Missing Required Fields"""
        self.print_test_header("Send Email - Missing Required Fields", 6)
        
        email_data = {
            "to": self.test_email
            # Missing subject and body
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json=email_data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code != 422:
                self.print_result(False, f"Status code expected 422, got {response.status_code}")
                return False
            
            self.print_result(True, "Validation error correctly returned for missing fields")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_7_check_nonexistent_task(self) -> bool:
        """Test 7: Check Non-existent Task Status"""
        self.print_test_header("Check Task Status - Non-existent Task", 7)
        
        fake_task_id = "non-existent-task-id-12345"
        
        try:
            response = self.session.get(f"{self.base_url}/status/{fake_task_id}", timeout=5)
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            # Para tareas no existentes, Celery normalmente devuelve PENDING
            if data.get("status") != "PENDING":
                self.print_result(False, f"Expected status 'PENDING' for non-existent task, got '{data.get('status')}'")
                return False
            
            self.print_result(True, "Non-existent task correctly returns PENDING status")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_8_send_multiple_emails(self) -> bool:
        """Test 8: Send Multiple Emails - Batch Test"""
        self.print_test_header("Send Multiple Emails - Batch Test", 8)
        
        email_data = {
            "to": self.test_email,
            "subject": "Segundo correo - Prueba de colas",
            "body": "Este es el segundo correo enviado para probar el sistema de colas.\n\nEste correo demuestra que múltiples tareas pueden ser procesadas en paralelo por Celery."
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/send-email",
                json=email_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            if "task_id" not in data:
                self.print_result(False, "Response missing task_id")
                return False
            
            # Guardar segundo task_id
            self.task_ids['second'] = data["task_id"]
            
            self.print_result(True, f"Second email queued - Task ID: {data['task_id']}")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def test_9_check_second_task(self) -> bool:
        """Test 9: Check Second Task Status"""
        self.print_test_header("Check Second Task Status", 9)
        
        if 'second' not in self.task_ids:
            self.print_result(False, "No second task_id available")
            return False
        
        task_id = self.task_ids['second']
        
        try:
            response = self.session.get(f"{self.base_url}/status/{task_id}", timeout=5)
            
            if response.status_code != 200:
                self.print_result(False, f"Status code expected 200, got {response.status_code}")
                return False
            
            data = response.json()
            
            if data.get("task_id") != task_id:
                self.print_result(False, f"Task ID mismatch")
                return False
            
            self.print_result(True, f"Second task status: {data.get('status')}")
            return True
            
        except Exception as e:
            self.print_result(False, f"Exception occurred: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print("🚀 Starting Email Queue System API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print(f"📧 Test Email: {self.test_email}")
        
        tests = [
            self.test_1_health_check,
            self.test_2_api_root,
            self.test_3_send_email_valid,
            self.test_4_check_task_status,
            self.test_5_send_email_invalid_format,
            self.test_6_send_email_missing_fields,
            self.test_7_check_nonexistent_task,
            self.test_8_send_multiple_emails,
            self.test_9_check_second_task
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ FAIL: Unexpected error in {test.__name__}: {str(e)}")
                failed += 1
            
            # Pequeña pausa entre tests
            time.sleep(1)
        
        # Resumen final
        print(f"\n{'='*60}")
        print(f"🏁 Test Results Summary")
        print('='*60)
        print(f"✅ Tests Passed: {passed}")
        print(f"❌ Tests Failed: {failed}")
        print(f"📊 Total Tests: {passed + failed}")
        print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed == 0:
            print("\n🎉 All tests passed! Your Email Queue System is working perfectly!")
        else:
            print(f"\n⚠️ {failed} test(s) failed. Please check the configuration and try again.")
        
        return failed == 0

def main():
    """Función principal para ejecutar los tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Email Queue System API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--email", default="dasalvasuper@gmail.com", help="Test email address")
    
    args = parser.parse_args()
    
    tester = EmailQueueSystemTester(args.url, args.email)
    success = tester.run_all_tests()
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main()