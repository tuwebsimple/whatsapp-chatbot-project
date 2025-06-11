"""
Implementación alternativa usando Hugging Face Transformers para LLMs locales.
Esta implementación permite ejecutar modelos directamente sin servicios externos.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)

class LocalLLMService:
    """
    Servicio para ejecutar modelos de lenguaje localmente usando Transformers.
    """
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """
        Inicializa el servicio LLM local.
        
        Args:
            model_name: Nombre del modelo de Hugging Face
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_length = 512
        
    def load_model(self) -> bool:
        """
        Carga el modelo y tokenizer.
        
        Returns:
            True si el modelo se cargó exitosamente
        """
        try:
            logger.info(f"Cargando modelo {self.model_name} en {self.device}")
            
            # Cargar tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Configurar pad_token si no existe
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Cargar modelo
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Crear pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("Modelo cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando modelo: {str(e)}")
            return False
    
    def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """
        Genera una respuesta usando el modelo local.
        
        Args:
            message: Mensaje del usuario
            context: Contexto de la conversación
            
        Returns:
            Respuesta generada
        """
        try:
            if not self.pipeline:
                if not self.load_model():
                    return self._get_fallback_response(message)
            
            # Construir prompt
            prompt = self._build_prompt(message, context)
            
            # Generar respuesta
            outputs = self.pipeline(
                prompt,
                max_length=self.max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                truncation=True
            )
            
            # Extraer respuesta
            generated_text = outputs[0]['generated_text']
            response = generated_text[len(prompt):].strip()
            
            # Limpiar respuesta
            response = self._clean_response(response)
            
            return response if response else self._get_fallback_response(message)
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {str(e)}")
            return self._get_fallback_response(message)
    
    def _build_prompt(self, message: str, context: Optional[str] = None) -> str:
        """Construye el prompt para el modelo."""
        if self.model_name.startswith("microsoft/DialoGPT"):
            # Para DialoGPT, usar formato de conversación
            if context:
                return f"{context}\nUsuario: {message}\nAsistente:"
            else:
                return f"Usuario: {message}\nAsistente:"
        else:
            # Para otros modelos, usar formato de instrucción
            system_prompt = "Eres un asistente virtual útil y amigable. Responde de manera concisa y profesional."
            if context:
                return f"{system_prompt}\n\nContexto: {context}\n\nUsuario: {message}\nAsistente:"
            else:
                return f"{system_prompt}\n\nUsuario: {message}\nAsistente:"
    
    def _clean_response(self, response: str) -> str:
        """Limpia la respuesta generada."""
        # Remover tokens especiales
        response = response.replace("<|endoftext|>", "")
        response = response.replace("<|pad|>", "")
        
        # Tomar solo la primera línea/oración si es muy larga
        lines = response.split('\n')
        if lines:
            response = lines[0].strip()
        
        # Limitar longitud
        if len(response) > 300:
            sentences = response.split('.')
            if len(sentences) > 1:
                response = sentences[0] + '.'
            else:
                response = response[:300] + '...'
        
        return response
    
    def _get_fallback_response(self, message: str) -> str:
        """Respuesta de respaldo cuando el modelo no está disponible."""
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in ['hola', 'buenos días', 'buenas tardes']):
            return "¡Hola! Gracias por contactarnos. ¿En qué puedo ayudarte?"
        elif any(help_word in message_lower for help_word in ['ayuda', 'help']):
            return "Estoy aquí para ayudarte. Por favor, describe tu consulta."
        elif any(thanks in message_lower for thanks in ['gracias', 'thank you']):
            return "¡De nada! ¿Hay algo más en lo que pueda ayudarte?"
        else:
            return "He recibido tu mensaje. Nuestro equipo te responderá pronto."
    
    def is_available(self) -> bool:
        """Verifica si el modelo está disponible."""
        return self.pipeline is not None

# Modelos recomendados para diferentes casos de uso
RECOMMENDED_MODELS = {
    "conversational": [
        "microsoft/DialoGPT-medium",
        "microsoft/DialoGPT-small",
        "facebook/blenderbot-400M-distill"
    ],
    "instruction": [
        "microsoft/phi-2",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "stabilityai/stablelm-tuned-alpha-3b"
    ],
    "multilingual": [
        "microsoft/DialoGPT-medium",
        "facebook/mbart-large-50-many-to-many-mmt"
    ]
}

def get_recommended_model(use_case: str = "conversational", size: str = "medium") -> str:
    """
    Obtiene un modelo recomendado según el caso de uso.
    
    Args:
        use_case: Tipo de uso ("conversational", "instruction", "multilingual")
        size: Tamaño del modelo ("small", "medium", "large")
        
    Returns:
        Nombre del modelo recomendado
    """
    models = RECOMMENDED_MODELS.get(use_case, RECOMMENDED_MODELS["conversational"])
    
    if size == "small" and len(models) > 1:
        return models[1]
    elif size == "large" and len(models) > 2:
        return models[2]
    else:
        return models[0]

# Instancia global del servicio LLM local
local_llm_service = LocalLLMService()

def get_local_llm_response(message: str, context: Optional[str] = None) -> str:
    """
    Función de conveniencia para obtener respuestas del LLM local.
    
    Args:
        message: Mensaje del usuario
        context: Contexto de la conversación
        
    Returns:
        Respuesta generada
    """
    return local_llm_service.generate_response(message, context)

