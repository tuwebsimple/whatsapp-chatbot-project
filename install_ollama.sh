#!/bin/bash

# Script de instalación de Ollama y modelos LLM
# Este script instala Ollama y descarga modelos de lenguaje recomendados

echo "=== Instalación de Ollama y Modelos LLM ==="

# Verificar si Ollama ya está instalado
if command -v ollama &> /dev/null; then
    echo "Ollama ya está instalado."
    ollama --version
else
    echo "Instalando Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if [ $? -eq 0 ]; then
        echo "Ollama instalado exitosamente."
    else
        echo "Error instalando Ollama."
        exit 1
    fi
fi

# Iniciar el servicio de Ollama en segundo plano
echo "Iniciando servicio de Ollama..."
ollama serve &
OLLAMA_PID=$!

# Esperar a que Ollama esté listo
echo "Esperando a que Ollama esté listo..."
sleep 10

# Función para descargar un modelo
download_model() {
    local model_name=$1
    echo "Descargando modelo: $model_name"
    ollama pull $model_name
    
    if [ $? -eq 0 ]; then
        echo "Modelo $model_name descargado exitosamente."
    else
        echo "Error descargando modelo $model_name."
    fi
}

# Descargar modelos recomendados
echo "Descargando modelos recomendados..."

# Mistral 7B - Modelo principal recomendado
download_model "mistral:7b"

# Llama 2 7B - Alternativa
download_model "llama2:7b"

# Phi-2 - Modelo más pequeño para recursos limitados
download_model "phi"

# Verificar modelos instalados
echo "Modelos instalados:"
ollama list

echo "=== Instalación completada ==="
echo "Para usar los modelos:"
echo "1. Asegúrate de que Ollama esté ejecutándose: ollama serve"
echo "2. Configura LLM_PROVIDER=ollama en tu archivo .env"
echo "3. Configura LLM_MODEL=mistral:7b (o el modelo que prefieras)"

# Mantener Ollama ejecutándose
echo "Ollama está ejecutándose en segundo plano (PID: $OLLAMA_PID)"
echo "Para detenerlo: kill $OLLAMA_PID"

