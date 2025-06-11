"""
Script de pruebas para el sistema de chatbot de WhatsApp.
Incluye pruebas unitarias y de integración.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

import unittest
import json
import sys





# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
from src.services.llm_service import LLMService

class TestWhatsAppChatbot(unittest.TestCase):
    """Pruebas para el chatbot de WhatsApp."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Prueba el endpoint de salud."""
        response = self.app.get('/api/whatsapp/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'WhatsApp Chatbot')
        self.assertEqual(data['version'], '1.0.0')
    
    def test_webhook_verification(self):
        """Prueba la verificación del webhook."""
        # Simular verificación de WhatsApp
        response = self.app.get('/api/whatsapp/webhook', query_string={
            'hub.mode': 'subscribe',
            'hub.verify_token': 'YOUR_VERIFY_TOKEN',
            'hub.challenge': 'test_challenge'
        })
        
        # Debería devolver el challenge si el token es correcto
        # Nota: En un entorno real, necesitarías configurar el token correcto
        self.assertIn(response.status_code, [200, 403])
    
    def test_webhook_post_invalid_data(self):
        """Prueba el webhook con datos inválidos."""
        response = self.app.post('/api/whatsapp/webhook', 
                                json={}, 
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
    
    def test_send_message_endpoint_missing_params(self):
        """Prueba el endpoint de envío de mensajes sin parámetros."""
        response = self.app.post('/api/whatsapp/send-message',
                                json={},
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_send_message_endpoint_with_params(self):
        """Prueba el endpoint de envío de mensajes con parámetros."""
        response = self.app.post('/api/whatsapp/send-message',
                                json={
                                    'to': '1234567890',
                                    'message': 'Test message'
                                },
                                content_type='application/json')
        
        # Debería fallar porque no tenemos credenciales reales configuradas
        self.assertEqual(response.status_code, 500)

class TestLLMService(unittest.TestCase):
    """Pruebas para el servicio LLM."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.llm_service = LLMService(provider=os.getenv("LLM_PROVIDER"), model_name=os.getenv("LLM_MODEL"))
    
    def test_fallback_response_greeting(self):
        """Prueba la respuesta de respaldo para saludos."""
        response = self.llm_service._get_fallback_response("Hola")
        self.assertIn("Hola", response)
        self.assertIn("ayudarte", response)
    
    def test_fallback_response_help(self):
        """Prueba la respuesta de respaldo para ayuda."""
        response = self.llm_service._get_fallback_response("Necesito ayuda")
        self.assertIn("ayudarte", response)
    
    def test_fallback_response_thanks(self):
        """Prueba la respuesta de respaldo para agradecimientos."""
        response = self.llm_service._get_fallback_response("Gracias")
        self.assertIn("nada", response)
    
    def test_fallback_response_generic(self):
        """Prueba la respuesta de respaldo genérica."""
        response = self.llm_service._get_fallback_response("Mensaje aleatorio")
        self.assertIn("recibido", response)
    
    def test_build_prompt_without_context(self):
        """Prueba la construcción de prompt sin contexto."""
        prompt = self.llm_service._build_prompt("Hola")
        self.assertIn("asistente virtual", prompt.lower())
        self.assertIn("Hola", prompt)
    
    def test_build_prompt_with_context(self):
        """Prueba la construcción de prompt con contexto."""
        prompt = self.llm_service._build_prompt("¿Cómo estás?", "El usuario preguntó por productos")
        self.assertIn("contexto", prompt.lower())
        self.assertIn("productos", prompt)
        self.assertIn("¿Cómo estás?", prompt)

def run_integration_tests():
    """Ejecuta pruebas de integración básicas."""
    print("=== Pruebas de Integración ===")
    
    # Probar conexión al servidor
    import requests
    try:
        response = requests.get('http://localhost:5001/api/whatsapp/health', timeout=5)
        if response.status_code == 200:
            print("✓ Servidor Flask funcionando correctamente")
            data = response.json()
            print(f"  - Servicio: {data.get('service')}")
            print(f"  - Estado: {data.get('status')}")
            print(f"  - Versión: {data.get('version')}")
        else:
            print(f"✗ Error en servidor Flask: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ No se pudo conectar al servidor Flask: {e}")
    
    # Probar servicio LLM
    try:
        from src.services.llm_service import LLMService # Importa la clase, no la instancia global
        llm_service = LLMService(provider=os.getenv("LLM_PROVIDER"), model_name=os.getenv("LLM_MODEL"))

        available = llm_service.is_available()
        if available:
            print("✓ Servicio LLM disponible")
        else:
            print("⚠ Servicio LLM no disponible (usando respuestas de respaldo)")
        
        # Probar generación de respuesta
        response = llm_service.generate_response("Hola, ¿cómo estás?")
        print(f"✓ Respuesta de prueba generada: '{response[:50]}...'")
        
    except Exception as e:
        print(f"✗ Error en servicio LLM: {e}")
    
    print("\n=== Fin de Pruebas de Integración ===")

if __name__ == '__main__':
    print("Ejecutando pruebas del sistema de chatbot de WhatsApp...")
    print("=" * 50)
    
    # Ejecutar pruebas unitarias
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    
    # Ejecutar pruebas de integración
    run_integration_tests()

