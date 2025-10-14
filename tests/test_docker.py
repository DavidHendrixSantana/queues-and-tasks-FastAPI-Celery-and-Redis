import requests
import json
import time

def test_docker_deployment():
    """Prueba la aplicación desplegada con Docker"""
    
    base_url = "http://localhost:8000"
    
    print("🐳 Probando Email Queue System con Docker")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. 🏥 Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ API Status: {health_data['status']}")
            print(f"   🔄 Celery Workers: {health_data['celery_workers']}")
            print(f"   🔴 Redis: {health_data['redis_connection']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    # Test 2: API Root
    print("\n2. 🏠 Testing API Root...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            root_data = response.json()
            print(f"   ✅ API: {root_data['message']}")
            print(f"   📋 Version: {root_data['version']}")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test 3: Send Email
    print("\n3. 📧 Testing Send Email...")
    email_data = {
        "to": "test@example.com",
        "subject": "Docker Test Email",
        "body": "Este es un correo de prueba enviado desde Docker"
    }
    
    try:
        response = requests.post(
            f"{base_url}/send-email",
            json=email_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"   ✅ Email task created")
            print(f"   📋 Task ID: {task_id}")
            
            # Test 4: Monitor Task Status
            print("\n4. 🔍 Monitoring Task Status...")
            for i in range(10):
                try:
                    status_response = requests.get(
                        f"{base_url}/status/{task_id}",
                        timeout=5
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data["status"]
                        
                        print(f"   📊 Check {i+1}/10: {status}")
                        
                        if status_data.get("progress"):
                            progress = status_data["progress"]
                            if isinstance(progress, dict) and "message" in progress:
                                print(f"   🔄 Progress: {progress['message']}")
                        
                        if status in ["SUCCESS", "FAILURE"]:
                            if status == "SUCCESS" and status_data.get("result"):
                                print(f"   ✅ Task completed successfully!")
                                result_data = status_data["result"]
                                print(f"   📄 Result: {result_data.get('message', 'No message')}")
                            elif status == "FAILURE":
                                error = status_data.get("error", "Unknown error")
                                print(f"   ❌ Task failed: {error}")
                            break
                        
                        time.sleep(2)
                    else:
                        print(f"   ❌ Status check failed: {status_response.status_code}")
                        break
                        
                except requests.exceptions.RequestException as e:
                    print(f"   ❌ Status check error: {e}")
                    break
            
            return True
            
        else:
            print(f"   ❌ Send email failed: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Send email error: {e}")
        return False

def test_flower_monitor():
    """Prueba el monitor Flower de Celery"""
    print("\n5. 🌸 Testing Flower Monitor...")
    
    try:
        response = requests.get("http://localhost:5555", timeout=5)
        if response.status_code == 200:
            print("   ✅ Flower monitor is accessible")
            print("   🌐 URL: http://localhost:5555")
        else:
            print(f"   ⚠️  Flower returned: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Flower not accessible: {e}")

def main():
    print("🧪 Docker Deployment Test Suite")
    print("Make sure to run: docker-compose up -d")
    print()
    
    success = test_docker_deployment()
    test_flower_monitor()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        print("🐳 Docker deployment is working correctly!")
    else:
        print("❌ Some tests failed. Check the logs above.")
    
    print("\n📊 Useful URLs:")
    print("   API: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Health: http://localhost:8000/health")
    print("   Flower: http://localhost:5555")

if __name__ == "__main__":
    main()