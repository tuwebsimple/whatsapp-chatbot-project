# Sistema de Chatbot para WhatsApp con IA Gratuita

Un sistema completo de chatbot inteligente para WhatsApp Business que utiliza modelos de lenguaje grandes (LLMs) de código abierto y gratuitos. Diseñado para pequeñas y medianas empresas que buscan automatizar su atención al cliente sin costos elevados de licenciamiento.

## 🚀 Características Principales

- **💰 100% Gratuito**: Utiliza exclusivamente tecnologías de código abierto
- **🤖 IA Avanzada**: Integración con modelos como Mistral 7B, LLaMA 2, Phi-2
- **📱 WhatsApp Business**: Integración completa con WhatsApp Business Cloud API
- **🔧 Fácil Configuración**: Scripts automatizados y documentación detallada
- **📈 Escalable**: Arquitectura modular que crece con tu negocio
- **🛡️ Robusto**: Manejo de errores y respuestas de respaldo automáticas

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │   Flask Backend  │    │   LLM Service   │
│   Cloud API     │◄──►│   (Webhooks)     │◄──►│   (Ollama/HF)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Base de Datos  │
                       │   (Opcional)     │
                       └──────────────────┘
```

## 📋 Requisitos del Sistema

### Mínimos
- **OS**: Ubuntu 20.04+ / CentOS 7+ / macOS 10.15+
- **RAM**: 4GB (recomendado 8GB+)
- **CPU**: 2 cores (recomendado 4+ cores)
- **Almacenamiento**: 10GB libres
- **Python**: 3.8+

### Para Producción
- **RAM**: 8GB+ (16GB para modelos grandes)
- **CPU**: 4+ cores
- **Almacenamiento**: 50GB+ SSD
- **Conexión**: Internet estable con IP pública

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/whatsapp-chatbot.git
cd whatsapp-chatbot
```

### 2. Configurar Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
nano .env  # Editar con tus credenciales
```

### 5. Instalar Ollama (Recomendado)
```bash
chmod +x install_ollama.sh
./install_ollama.sh
```

### 6. Ejecutar el Sistema
```bash
python src/main.py
```

## ⚙️ Configuración

### Variables de Entorno Principales

```bash
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=tu_token_de_acceso
WHATSAPP_PHONE_NUMBER_ID=id_del_numero_de_telefono
WHATSAPP_VERIFY_TOKEN=token_de_verificacion_personalizado

# Configuración LLM
LLM_PROVIDER=ollama  # ollama, huggingface, local
LLM_MODEL=mistral:7b
LLM_BASE_URL=http://localhost:11434

# Configuración de Aplicación
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_segura
LOG_LEVEL=INFO
```

### Configuración de WhatsApp Business API

1. **Crear Aplicación en Facebook Developers**
   - Visita [developers.facebook.com](https://developers.facebook.com)
   - Crea una nueva aplicación tipo "Business"
   - Agrega el producto "WhatsApp Business Platform"

2. **Configurar Webhook**
   - URL: `https://tu-dominio.com/api/whatsapp/webhook`
   - Token de verificación: El mismo que configuraste en `.env`

3. **Obtener Credenciales**
   - Usa el script automatizado: `python setup_whatsapp.py`
   - O sigue la guía detallada en `WHATSAPP_SETUP.md`

## 🤖 Opciones de Modelos de IA

### Ollama (Recomendado)
```bash
# Instalar y configurar
./install_ollama.sh

# Modelos disponibles
ollama pull mistral:7b      # Equilibrio óptimo
ollama pull llama2:7b       # Alternativa robusta
ollama pull phi:2.7b        # Para recursos limitados
```

### Hugging Face Local
```bash
# Configurar en .env
LLM_PROVIDER=local
LLM_MODEL=microsoft/DialoGPT-medium
```

### Hugging Face API
```bash
# Configurar en .env
LLM_PROVIDER=huggingface
LLM_MODEL=microsoft/DialoGPT-medium
HUGGINGFACE_API_KEY=tu_api_key
```

## 🧪 Pruebas

### Ejecutar Suite de Pruebas
```bash
python test_chatbot.py
```

### Probar Endpoints Manualmente
```bash
# Verificar salud del sistema
curl http://localhost:5001/api/whatsapp/health

# Probar envío de mensaje
curl -X POST http://localhost:5001/api/whatsapp/send-message \
  -H "Content-Type: application/json" \
  -d '{"to": "1234567890", "message": "Hola desde el chatbot!"}'
```

## 📊 Monitoreo

### Métricas Disponibles
- Tiempo de respuesta promedio
- Tasa de éxito de mensajes
- Uso de recursos del sistema
- Disponibilidad del LLM

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/chatbot.log

# Logs de acceso
tail -f logs/access.log
```

## 🚀 Despliegue en Producción

### Con Docker (Próximamente)
```bash
docker-compose up -d
```

### Con Systemd
```bash
# Crear servicio
sudo cp whatsapp-chatbot.service /etc/systemd/system/
sudo systemctl enable whatsapp-chatbot
sudo systemctl start whatsapp-chatbot
```

### Con Nginx
```bash
# Configurar proxy reverso
sudo cp nginx.conf /etc/nginx/sites-available/whatsapp-chatbot
sudo ln -s /etc/nginx/sites-available/whatsapp-chatbot /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## 📚 Documentación

- **[Documentación Completa](DOCUMENTACION_COMPLETA.md)**: Guía técnica detallada
- **[Configuración WhatsApp](WHATSAPP_SETUP.md)**: Guía paso a paso para WhatsApp Business API
- **[Configuración LLM](LLM_SETUP.md)**: Opciones y optimización de modelos de IA
- **[Arquitectura del Sistema](arquitectura_sistema.md)**: Diseño técnico detallado

## 🤝 Casos de Uso

### Comercio Electrónico
- Consultas sobre productos
- Seguimiento de pedidos
- Soporte post-venta
- Recomendaciones personalizadas

### Servicios
- Programación de citas
- Información de servicios
- Soporte técnico básico
- FAQ automatizadas

### Educación
- Información de cursos
- Soporte a estudiantes
- Procesos de admisión
- Recordatorios académicos

## 💰 Costos Estimados

### Pequeña Empresa (< 1,000 conversaciones/mes)
- WhatsApp: **Gratis** (primeras 1,000)
- Servidor VPS: **$20-50/mes**
- **Total: $20-50/mes**

### Mediana Empresa (1,000-5,000 conversaciones/mes)
- WhatsApp: **$50-150/mes**
- Servidor dedicado: **$100-200/mes**
- **Total: $150-350/mes**

## 🔧 Personalización

### Modificar Personalidad del Bot
Edita el prompt del sistema en `src/services/llm_service.py`:

```python
system_prompt = """Eres un asistente virtual para [TU_EMPRESA]. 
Responde de manera profesional y ayuda con:
- Información sobre productos/servicios
- Horarios de atención
- Preguntas frecuentes

Mantén un tono [AMIGABLE/FORMAL/CASUAL] y profesional."""
```

### Agregar Comandos Especiales
```python
# En src/routes/whatsapp.py
def handle_special_commands(message):
    if message.lower() == '/horarios':
        return "Nuestros horarios son: Lun-Vie 9:00-18:00"
    elif message.lower() == '/contacto':
        return "Contáctanos: email@empresa.com | +1234567890"
    return None
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Error: "Port 5000 already in use"**
```bash
# Cambiar puerto en src/main.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

**Error: "LLM not available"**
```bash
# Verificar Ollama
ollama list
ollama serve

# O usar respuestas de respaldo
LLM_PROVIDER=fallback
```

**Error: "WhatsApp webhook verification failed"**
```bash
# Verificar token en .env
WHATSAPP_VERIFY_TOKEN=tu_token_exacto
```

### Logs de Debug
```bash
# Activar modo debug
export LOG_LEVEL=DEBUG
python src/main.py
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas de Contribución
- 🌐 Soporte para nuevos idiomas
- 🔌 Integraciones con CRM/ERP
- 📊 Herramientas de análisis
- 🎨 Interfaces de administración
- 📱 Soporte para otros canales (Telegram, Discord)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai/) por simplificar la ejecución de LLMs
- [Hugging Face](https://huggingface.co/) por democratizar el acceso a modelos de IA
- [Meta](https://developers.facebook.com/) por WhatsApp Business Platform
- [Mistral AI](https://mistral.ai/) por modelos de código abierto de alta calidad

## 📞 Soporte

- **Documentación**: Ver archivos en `/docs`
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/whatsapp-chatbot/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/whatsapp-chatbot/discussions)
- **Email**: soporte@tu-empresa.com

---

**⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella en GitHub!**

---

*Desarrollado con ❤️ por [Manus AI](https://manus.ai) - Democratizando el acceso a la inteligencia artificial*

