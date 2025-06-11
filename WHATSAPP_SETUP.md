# Guía de Configuración de WhatsApp Business API

## Prerrequisitos

1. **Cuenta de Facebook Business**: Necesitas una cuenta de Facebook Business Manager
2. **Aplicación de Facebook**: Crear una aplicación en Facebook Developers
3. **Número de teléfono**: Un número de teléfono que no esté registrado en WhatsApp personal
4. **Servidor público**: Tu webhook debe ser accesible desde internet (HTTPS requerido)

## Pasos de Configuración

### 1. Crear Aplicación en Facebook Developers

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Crea una nueva aplicación
3. Selecciona "Business" como tipo de aplicación
4. Agrega el producto "WhatsApp Business Platform"

### 2. Configurar WhatsApp Business Platform

1. En tu aplicación, ve a "WhatsApp" > "Getting Started"
2. Selecciona o crea una cuenta de WhatsApp Business
3. Agrega un número de teléfono
4. Verifica el número de teléfono

### 3. Obtener Credenciales

Necesitarás:
- **Access Token**: Token de acceso temporal o permanente
- **App ID**: ID de tu aplicación de Facebook
- **Phone Number ID**: ID del número de teléfono de WhatsApp
- **Verify Token**: Token personalizado para verificar tu webhook

### 4. Configurar Webhook

1. Tu webhook debe estar disponible en HTTPS
2. Debe responder a solicitudes GET para verificación
3. Debe procesar solicitudes POST para mensajes entrantes

### 5. Usar el Script de Configuración

Ejecuta el script de configuración incluido:

```bash
cd whatsapp-chatbot
source venv/bin/activate
python setup_whatsapp.py
```

Este script te ayudará a:
- Obtener tus cuentas de negocio
- Listar números de teléfono disponibles
- Configurar el webhook
- Enviar un mensaje de prueba
- Generar el archivo .env con la configuración

### 6. Variables de Entorno

Copia `.env.example` a `.env` y configura las variables:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```
WHATSAPP_ACCESS_TOKEN=tu_access_token
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
WHATSAPP_VERIFY_TOKEN=tu_verify_token
```

### 7. Probar la Configuración

1. Inicia el servidor Flask:
```bash
cd whatsapp-chatbot
source venv/bin/activate
python src/main.py
```

2. Verifica que el webhook esté funcionando:
```bash
curl http://localhost:5000/api/whatsapp/health
```

3. Envía un mensaje a tu número de WhatsApp Business

## Solución de Problemas

### Error: Webhook no verificado
- Asegúrate de que tu servidor esté accesible desde internet
- Verifica que el VERIFY_TOKEN coincida
- Usa HTTPS en producción

### Error: Token inválido
- Verifica que el Access Token sea válido
- Asegúrate de que tenga los permisos necesarios
- Regenera el token si es necesario

### Error: Número no encontrado
- Verifica que el número esté registrado en WhatsApp Business
- Asegúrate de usar el Phone Number ID correcto

### Mensajes no se envían
- Verifica que el Access Token tenga permisos de envío
- Asegúrate de que el número de destino esté en formato internacional
- Revisa los logs del servidor para errores específicos

## Limitaciones de la Versión Gratuita

- **1000 conversaciones gratuitas por mes**
- Después de eso, se cobra por conversación
- Las conversaciones se definen como ventanas de 24 horas
- Los mensajes de plantilla tienen costos adicionales

## Próximos Pasos

Una vez configurado WhatsApp Business API:
1. Configura el modelo de lenguaje (LLM)
2. Personaliza las respuestas del chatbot
3. Implementa lógica de negocio específica
4. Despliega en un servidor de producción

