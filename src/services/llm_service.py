"""
Módulo para la integración con modelos de lenguaje grandes (LLMs).
Este módulo maneja la comunicación con diferentes LLMs de código abierto.
"""
from src.services.local_llm_service import LocalLLMService
import logging
import json
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)

class LLMService:
    """
    Servicio para interactuar con modelos de lenguaje grandes.
    Soporta diferentes proveedores y modelos.
    """
    
    def __init__(self, provider: str = "ollama", model_name: str = "mistral:7b"):
        """
        Inicializa el servicio LLM.
        
        Args:
            provider: Proveedor del LLM (ollama, huggingface, local)
            model_name: Nombre del modelo a utilizar
        """
        self.provider = provider
        self.model_name = model_name
        self.base_url = self._get_base_url()

        # --- AÑADE ESTA LÍNEA --- #
        logger.info(f"DEBUG LLMService initialized with provider: {self.provider} and model: {self.model_name}")
        # ------------------------ #

         
        if self.provider == "local":
            self.local_llm_instance = LocalLLMService(model_name=self.model_name)
        else:
            self.local_llm_instance = None
        
    def _get_base_url(self) -> str:
        """Obtiene la URL base según el proveedor."""
        if self.provider == "ollama":
            return "http://localhost:11434"
        elif self.provider == "huggingface":
            return "https://api-inference.huggingface.co"
        else:
            return "http://localhost:8000"  # Para modelos locales
    
    def generate_response(self, message: str, context: Optional[str] = None, 
                         user_id: Optional[str] = None) -> str:
        """
        Genera una respuesta usando el LLM.
        
        Args:
            message: Mensaje del usuario
            context: Contexto adicional de la conversación
            user_id: ID del usuario para personalización
            
        Returns:
            Respuesta generada por el LLM
        """
        try:
            if self.provider == "ollama":
                return self._generate_ollama_response(message, context)
            elif self.provider == "huggingface":
                return self._generate_huggingface_response(message, context)
            else:
                return self._generate_local_response(message, context)
                
        except Exception as e:
            logger.error(f"Error generando respuesta con LLM: {str(e)}")
            return self._get_fallback_response(message)
    
    def _generate_ollama_response(self, message: str, context: Optional[str] = None) -> str:
        """Genera respuesta usando Ollama."""
        try:
            # Construir el prompt con contexto si está disponible
            prompt = self._build_prompt(message, context)
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Error en Ollama API: {response.status_code} - {response.text}")
                return self._get_fallback_response(message)
                
        except Exception as e:
            logger.error(f"Error en _generate_ollama_response: {str(e)}")
            return self._get_fallback_response(message)
    
    def _generate_huggingface_response(self, message: str, context: Optional[str] = None) -> str:
        """Genera respuesta usando Hugging Face Inference API."""
        try:
            # Nota: Requiere API key de Hugging Face
            headers = {
                "Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY",
                "Content-Type": "application/json"
            }
            
            prompt = self._build_prompt(message, context)
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/models/{self.model_name}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").replace(prompt, "").strip()
                return "Lo siento, no pude generar una respuesta."
            else:
                logger.error(f"Error en Hugging Face API: {response.status_code} - {response.text}")
                return self._get_fallback_response(message)
                
        except Exception as e:
            logger.error(f"Error en _generate_huggingface_response: {str(e)}")
            return self._get_fallback_response(message)
    
    def _generate_local_response(self, message: str, context: Optional[str] = None) -> str:
        """Genera respuesta utilizando el modelo local de Hugging Face."""
        if self.local_llm_instance:
            return self.local_llm_instance.generate_response(message, context)
        else:
            logger.error("Local LLM instance not initialized.")
            return self._get_fallback_response(message)

    
    def _build_prompt(self, message: str, context: Optional[str] = None) -> str:
        """Construye el prompt para el LLM."""
        system_prompt = """Eres un asistente virtual útil y amigable para un negocio. 
Responde de manera profesional, concisa y en español. 
Ayuda a los clientes con sus consultas sobre productos, servicios y información general.
Mantén un tono cordial y profesional en todo momento."""
        
        if context:
            prompt = f"{system_prompt}\n\nContexto de la conversación:\n{context}\n\nUsuario: {message}\nAsistente:"
        else:
            prompt = f"{system_prompt}\n\nUsuario: {message}\nAsistente:"
        
        return prompt
    
    def _get_fallback_response(self, message: str) -> str:
        """Respuesta de respaldo cuando el LLM no está disponible."""
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in ['hola', 'buenos días', 'buenas tardes', 'buenas noches']):
            return "¡Hola! Gracias por contactarnos. En este momento estoy experimentando algunas dificultades técnicas, pero nuestro equipo te responderá pronto. ¿En qué puedo ayudarte?"
        elif any(help_word in message_lower for help_word in ['ayuda', 'help', 'información']):
            return "Estoy aquí para ayudarte, aunque actualmente tengo limitaciones técnicas. Por favor, describe tu consulta y nuestro equipo te asistirá lo antes posible."
        elif any(thanks in message_lower for thanks in ['gracias', 'thank you', 'thanks']):
            return "¡De nada! Si tienes alguna otra pregunta, no dudes en escribirme."
        else:
            return "He recibido tu mensaje y nuestro equipo te responderá pronto. Disculpa las molestias por la demora en la respuesta automática."
    
    def is_available(self) -> bool:
        """Verifica si el servicio LLM está disponible."""
        try:
            if self.provider == "ollama":
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
                return response.status_code == 200
            elif self.provider == "huggingface":
                # Para HF, asumimos que está disponible si tenemos API key
                return True
            else:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                return response.status_code == 200
        except:
            return False

# Instancia global del servicio LLM
llm_service = LLMService()

def get_llm_response(message: str, context: Optional[str] = None, 
                    user_id: Optional[str] = None) -> str:
    """
    Función de conveniencia para obtener respuestas del LLM.
    
    Args:
        message: Mensaje del usuario
        context: Contexto de la conversación
        user_id: ID del usuario
        
    Returns:
        Respuesta generada
    """
    return llm_service.generate_response(message, context, user_id)

