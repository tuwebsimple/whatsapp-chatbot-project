from flask import Blueprint, jsonify, request
import requests
import json
import logging
from src.services.llm_service import get_llm_response

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

whatsapp_bp = Blueprint('whatsapp', __name__)

# Configuración de WhatsApp Business API
WHATSAPP_TOKEN = "YOUR_WHATSAPP_ACCESS_TOKEN"  # Debe ser configurado
WHATSAPP_PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"  # Debe ser configurado
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"  # Token para verificar el webhook

@whatsapp_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Verificación del webhook de WhatsApp.
    WhatsApp enviará una solicitud GET para verificar el webhook.
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        logger.info("Webhook verificado exitosamente")
        return challenge, 200
    else:
        logger.warning("Falló la verificación del webhook")
        return "Forbidden", 403

@whatsapp_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Maneja los mensajes entrantes de WhatsApp.
    """
    try:
        data = request.get_json()
        logger.info(f"Datos recibidos del webhook: {json.dumps(data, indent=2)}")
        
        # Verificar si hay mensajes en los datos
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            value = change.get('value', {})
                            
                            # Procesar mensajes entrantes
                            if 'messages' in value:
                                for message in value['messages']:
                                    process_incoming_message(message, value.get('metadata', {}))
                            
                            # Procesar estados de mensajes (entregado, leído, etc.)
                            if 'statuses' in value:
                                for status in value['statuses']:
                                    process_message_status(status)
        
        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def process_incoming_message(message, metadata):
    """
    Procesa un mensaje entrante de WhatsApp.
    """
    try:
        message_id = message.get('id')
        from_number = message.get('from')
        message_type = message.get('type')
        timestamp = message.get('timestamp')
        
        logger.info(f"Procesando mensaje {message_id} de {from_number}")
        
        # Extraer el contenido del mensaje según su tipo
        message_content = ""
        if message_type == 'text':
            message_content = message.get('text', {}).get('body', '')
        elif message_type == 'image':
            # Manejar imágenes (por ahora solo log)
            logger.info("Mensaje de imagen recibido")
            message_content = "Imagen recibida"
        elif message_type == 'audio':
            # Manejar audio (por ahora solo log)
            logger.info("Mensaje de audio recibido")
            message_content = "Audio recibido"
        else:
            logger.info(f"Tipo de mensaje no soportado: {message_type}")
            message_content = f"Tipo de mensaje no soportado: {message_type}"
        
        # Generar respuesta usando el LLM
        response_text = get_llm_response(message_content, user_id=from_number)
        
        # Enviar respuesta
        send_whatsapp_message(from_number, response_text)
        
    except Exception as e:
        logger.error(f"Error procesando mensaje entrante: {str(e)}")

def process_message_status(status):
    """
    Procesa el estado de un mensaje (entregado, leído, etc.).
    """
    try:
        message_id = status.get('id')
        status_type = status.get('status')
        timestamp = status.get('timestamp')
        
        logger.info(f"Estado del mensaje {message_id}: {status_type}")
        
    except Exception as e:
        logger.error(f"Error procesando estado del mensaje: {str(e)}")

def send_whatsapp_message(to_number, message_text):
    """
    Envía un mensaje de texto a través de la WhatsApp Business API.
    """
    try:
        url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            logger.info(f"Mensaje enviado exitosamente a {to_number}")
            return True
        else:
            logger.error(f"Error enviando mensaje: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando mensaje de WhatsApp: {str(e)}")
        return False

@whatsapp_bp.route('/send-message', methods=['POST'])
def send_message_endpoint():
    """
    Endpoint para enviar mensajes manualmente (útil para pruebas).
    """
    try:
        data = request.get_json()
        to_number = data.get('to')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({"error": "Faltan parámetros 'to' y 'message'"}), 400
        
        success = send_whatsapp_message(to_number, message)
        
        if success:
            return jsonify({"status": "success", "message": "Mensaje enviado"}), 200
        else:
            return jsonify({"error": "Error enviando mensaje"}), 500
            
    except Exception as e:
        logger.error(f"Error en endpoint send-message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@whatsapp_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud del servicio.
    """
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Chatbot",
        "version": "1.0.0"
    }), 200

