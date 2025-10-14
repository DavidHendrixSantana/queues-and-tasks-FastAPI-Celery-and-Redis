import asyncio
import aiosmtplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import ssl

# Cargar variables de entorno
load_dotenv()

class SMTPTester:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        
    def print_config(self, port, use_ssl, use_tls, description):
        """Imprime la configuración que se va a probar"""
        print(f"\n{'='*60}")
        print(f"🧪 Probando: {description}")
        print(f"📧 Host: {self.smtp_host}")
        print(f"🔌 Puerto: {port}")
        print(f"🔒 SSL: {use_ssl}")
        print(f"🛡️ TLS: {use_tls}")
        print(f"👤 Usuario: {self.smtp_user}")
        print('='*60)
    
    async def test_aiosmtplib_ssl(self):
        """Prueba 1: Puerto 465 con SSL directo usando aiosmtplib"""
        self.print_config(465, True, False, "aiosmtplib - Puerto 465 SSL")
        
        try:
            smtp_client = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=465,
                use_tls=True  # SSL directo en puerto 465
            )
            
            print("🔌 Conectando con SSL directo...")
            await smtp_client.connect()
            
            print("🔑 Autenticando...")
            await smtp_client.login(self.smtp_user, self.smtp_password)
            
            print("✅ ¡Conexión SSL exitosa con aiosmtplib!")
            await smtp_client.quit()
            return True
            
        except Exception as e:
            print(f"❌ Error con SSL: {str(e)}")
            return False
    
    async def test_aiosmtplib_tls(self):
        """Prueba 2: Puerto 587 con STARTTLS usando aiosmtplib"""
        self.print_config(587, False, True, "aiosmtplib - Puerto 587 STARTTLS")
        
        try:
            smtp_client = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=587,
                use_tls=False  # No SSL directo
            )
            
            print("🔌 Conectando sin SSL...")
            await smtp_client.connect()
            
            print("🛡️ Iniciando STARTTLS...")
            await smtp_client.starttls()
            
            print("🔑 Autenticando...")
            await smtp_client.login(self.smtp_user, self.smtp_password)
            
            print("✅ ¡Conexión TLS exitosa con aiosmtplib!")
            await smtp_client.quit()
            return True
            
        except Exception as e:
            print(f"❌ Error con TLS: {str(e)}")
            return False
    
    def test_smtplib_ssl(self):
        """Prueba 3: Puerto 465 con SSL usando smtplib estándar"""
        self.print_config(465, True, False, "smtplib - Puerto 465 SSL")
        
        try:
            print("🔌 Conectando con SSL directo (smtplib)...")
            server = smtplib.SMTP_SSL(self.smtp_host, 465)
            
            print("🔑 Autenticando...")
            server.login(self.smtp_user, self.smtp_password)
            
            print("✅ ¡Conexión SSL exitosa con smtplib!")
            server.quit()
            return True
            
        except Exception as e:
            print(f"❌ Error con SSL (smtplib): {str(e)}")
            return False
    
    def test_smtplib_tls(self):
        """Prueba 4: Puerto 587 con STARTTLS usando smtplib estándar"""
        self.print_config(587, False, True, "smtplib - Puerto 587 STARTTLS")
        
        try:
            print("🔌 Conectando sin SSL (smtplib)...")
            server = smtplib.SMTP(self.smtp_host, 587)
            
            print("🛡️ Iniciando STARTTLS...")
            server.starttls()
            
            print("🔑 Autenticando...")
            server.login(self.smtp_user, self.smtp_password)
            
            print("✅ ¡Conexión TLS exitosa con smtplib!")
            server.quit()
            return True
            
        except Exception as e:
            print(f"❌ Error con TLS (smtplib): {str(e)}")
            return False
    
    async def send_test_email_async(self, use_ssl=True):
        """Envía un correo de prueba usando la configuración que funcione"""
        port = 465 if use_ssl else 587
        self.print_config(port, use_ssl, not use_ssl, f"Envío real de correo - {'SSL' if use_ssl else 'TLS'}")
        
        try:
            # Crear mensaje
            message = MIMEMultipart()
            message["From"] = self.smtp_user
            message["To"] = self.smtp_user  # Enviarse a sí mismo
            message["Subject"] = "✅ Prueba SSL/TLS exitosa - Email Queue System"
            
            body = f"""
🎉 ¡Felicitaciones!

La configuración SMTP está funcionando correctamente:

📧 Servidor: {self.smtp_host}
🔌 Puerto: {port}
🔒 Método: {'SSL directo' if use_ssl else 'STARTTLS'}
👤 Usuario: {self.smtp_user}

Tu sistema de colas de correo está listo para funcionar! 🚀

---
Email Queue System - Test automático
            """
            
            message.attach(MIMEText(body, "plain", "utf-8"))
            
            # Configurar cliente
            if use_ssl:
                smtp_client = aiosmtplib.SMTP(
                    hostname=self.smtp_host,
                    port=465,
                    use_tls=True
                )
            else:
                smtp_client = aiosmtplib.SMTP(
                    hostname=self.smtp_host,
                    port=587,
                    use_tls=False
                )
            
            print("🔌 Conectando para envío real...")
            await smtp_client.connect()
            
            if not use_ssl:
                print("🛡️ Iniciando STARTTLS...")
                await smtp_client.starttls()
            
            print("🔑 Autenticando...")
            await smtp_client.login(self.smtp_user, self.smtp_password)
            
            print("📧 Enviando correo de prueba...")
            await smtp_client.send_message(message)
            
            await smtp_client.quit()
            
            print("✅ ¡Correo enviado exitosamente!")
            print(f"📥 Revisa tu bandeja: {self.smtp_user}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando correo: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("🔍 Iniciando diagnóstico completo de SMTP")
        print(f"📧 Email configurado: {self.smtp_user}")
        print(f"🔑 Password configurado: {'✅ Sí' if self.smtp_password else '❌ No'}")
        
        if not self.smtp_user or not self.smtp_password:
            print("\n❌ Faltan credenciales SMTP. Configura SMTP_USER y SMTP_PASSWORD en .env")
            return False
        
        results = {}
        
        # Probar todas las configuraciones
        print("\n🧪 FASE 1: Pruebas de Conexión")
        results['aiosmtplib_ssl'] = await self.test_aiosmtplib_ssl()
        results['aiosmtplib_tls'] = await self.test_aiosmtplib_tls()
        results['smtplib_ssl'] = self.test_smtplib_ssl()
        results['smtplib_tls'] = self.test_smtplib_tls()
        
        # Resumen de conexiones
        print(f"\n📊 RESUMEN DE CONEXIONES:")
        for test, result in results.items():
            status = "✅ FUNCIONA" if result else "❌ FALLA"
            print(f"   {test}: {status}")
        
        # Intentar envío real con la configuración que funcione
        print(f"\n🧪 FASE 2: Envío Real de Correo")
        
        if results['aiosmtplib_ssl']:
            print("🎯 Usando configuración SSL (puerto 465)")
            success = await self.send_test_email_async(use_ssl=True)
        elif results['aiosmtplib_tls']:
            print("🎯 Usando configuración TLS (puerto 587)")
            success = await self.send_test_email_async(use_ssl=False)
        else:
            print("❌ Ninguna configuración de aiosmtplib funcionó")
            success = False
        
        # Recomendaciones finales
        print(f"\n🎯 RECOMENDACIONES:")
        
        if results['aiosmtplib_ssl']:
            print("✅ Usar configuración SSL:")
            print("   SMTP_PORT=465")
            print("   SMTP_USE_SSL=true")
            print("   SMTP_USE_TLS=false")
        elif results['aiosmtplib_tls']:
            print("✅ Usar configuración TLS:")
            print("   SMTP_PORT=587")
            print("   SMTP_USE_SSL=false") 
            print("   SMTP_USE_TLS=true")
        else:
            print("❌ Revisar credenciales o configuración de red")
            print("🔍 Posibles problemas:")
            print("   - App Password incorrecto")
            print("   - 2FA no habilitado en Gmail")
            print("   - Firewall bloqueando conexiones")
        
        return success

async def main():
    """Función principal"""
    tester = SMTPTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())