# Guía de Implementación de Modelos de Lenguaje

## Opciones de Implementación

Este proyecto soporta múltiples opciones para ejecutar modelos de lenguaje grandes (LLMs):

### 1. Ollama (Recomendado para Producción)

Ollama es una herramienta que simplifica la ejecución de LLMs localmente.

**Ventajas:**
- Fácil instalación y gestión de modelos
- Optimizado para rendimiento
- API REST simple
- Soporte para múltiples modelos

**Instalación:**
```bash
# Ejecutar el script de instalación
./install_ollama.sh

# O instalar manualmente
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral:7b
```

**Configuración:**
```bash
# En .env
LLM_PROVIDER=ollama
LLM_MODEL=mistral:7b
LLM_BASE_URL=http://localhost:11434
```

### 2. Hugging Face Transformers (Local)

Ejecuta modelos directamente usando la librería Transformers.

**Ventajas:**
- Control total sobre el modelo
- No requiere servicios externos
- Amplia selección de modelos

**Desventajas:**
- Mayor uso de memoria
- Configuración más compleja
- Tiempo de carga inicial

**Configuración:**
```bash
# En .env
LLM_PROVIDER=local
LLM_MODEL=microsoft/DialoGPT-medium
```

### 3. Hugging Face Inference API

Usa la API de inferencia de Hugging Face (requiere API key).

**Ventajas:**
- Sin instalación local
- Acceso a modelos grandes
- Escalabilidad automática

**Desventajas:**
- Requiere conexión a internet
- Costos por uso
- Latencia de red

**Configuración:**
```bash
# En .env
LLM_PROVIDER=huggingface
LLM_MODEL=microsoft/DialoGPT-medium
HUGGINGFACE_API_KEY=tu_api_key
```

## Modelos Recomendados

### Para Recursos Limitados (< 4GB RAM)
- `microsoft/DialoGPT-small`
- `microsoft/phi-2`
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

### Para Recursos Moderados (4-8GB RAM)
- `microsoft/DialoGPT-medium`
- `mistral:7b` (Ollama)
- `llama2:7b` (Ollama)

### Para Recursos Altos (> 8GB RAM)
- `microsoft/DialoGPT-large`
- `mixtral:8x7b` (Ollama)
- `llama2:13b` (Ollama)

## Configuración del Servicio LLM

### Archivo de Configuración (.env)

```bash
# Proveedor principal
LLM_PROVIDER=ollama

# Modelo a usar
LLM_MODEL=mistral:7b

# URL base del servicio (para Ollama)
LLM_BASE_URL=http://localhost:11434

# API Key para Hugging Face (si se usa)
HUGGINGFACE_API_KEY=tu_api_key_aqui
```

### Personalización del Prompt

El sistema permite personalizar el prompt del asistente editando el método `_build_prompt` en `src/services/llm_service.py`:

```python
def _build_prompt(self, message: str, context: Optional[str] = None) -> str:
    system_prompt = """Eres un asistente virtual para [NOMBRE_DE_TU_NEGOCIO]. 
    Responde de manera profesional y ayuda con:
    - Información sobre productos/servicios
    - Horarios de atención
    - Preguntas frecuentes
    - Soporte al cliente
    
    Mantén un tono amigable y profesional."""
    
    # ... resto del método
```

## Pruebas del LLM

### Probar Ollama
```bash
# Verificar que Ollama esté ejecutándose
curl http://localhost:11434/api/tags

# Probar generación de texto
curl http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "Hola, ¿cómo estás?",
  "stream": false
}'
```

### Probar el Servicio Local
```python
# En una consola Python
from src.services.llm_service import get_llm_response

response = get_llm_response("Hola, ¿cómo puedes ayudarme?")
print(response)
```

## Optimización de Rendimiento

### Para Ollama
- Usar modelos cuantizados (Q4, Q8) para menor uso de memoria
- Configurar `OLLAMA_NUM_PARALLEL` para múltiples solicitudes
- Usar SSD para almacenamiento de modelos

### Para Transformers Local
- Usar `torch.float16` en GPUs compatibles
- Configurar `device_map="auto"` para distribución automática
- Implementar caché de modelos para evitar recargas

### Configuración de Memoria
```python
# En local_llm_service.py
self.model = AutoModelForCausalLM.from_pretrained(
    self.model_name,
    torch_dtype=torch.float16,  # Reduce uso de memoria
    device_map="auto",          # Distribución automática
    low_cpu_mem_usage=True      # Optimización de CPU
)
```

## Monitoreo y Logs

El sistema incluye logging detallado para monitorear el rendimiento:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Los logs incluyen:
- Tiempo de respuesta del LLM
- Errores de conexión
- Uso de memoria
- Estadísticas de mensajes

## Solución de Problemas

### Ollama no responde
```bash
# Verificar proceso
ps aux | grep ollama

# Reiniciar servicio
pkill ollama
ollama serve &
```

### Error de memoria insuficiente
- Usar modelos más pequeños
- Configurar swap en el sistema
- Usar cuantización

### Respuestas lentas
- Verificar recursos del sistema
- Usar modelos más pequeños
- Configurar timeout apropiado

### Modelo no encontrado
```bash
# Listar modelos disponibles
ollama list

# Descargar modelo faltante
ollama pull mistral:7b
```

## Escalabilidad

Para entornos de producción con alto volumen:

1. **Múltiples instancias de Ollama**
2. **Load balancer para distribución**
3. **Caché de respuestas frecuentes**
4. **Monitoreo de recursos**
5. **Auto-scaling basado en carga**

