"""
Script de configuración para WhatsApp Business API.
Este script ayuda a configurar la integración con WhatsApp Business Platform.
"""

import os
import json
import requests
from typing import Dict, Any

class WhatsAppSetup:
    """Clase para configurar la integración con WhatsApp Business API."""
    
    def __init__(self, access_token: str, app_id: str):
        """
        Inicializa la configuración de WhatsApp.
        
        Args:
            access_token: Token de acceso de la aplicación de Facebook
            app_id: ID de la aplicación de Facebook
        """
        self.access_token = access_token
        self.app_id = app_id
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def get_business_accounts(self) -> Dict[str, Any]:
        """Obtiene las cuentas de negocio disponibles."""
        try:
            url = f"{self.base_url}/{self.app_id}"
            params = {
                "fields": "whatsapp_business_accounts",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo cuentas de negocio: {e}")
            return {}
    
    def get_phone_numbers(self, business_account_id: str) -> Dict[str, Any]:
        """Obtiene los números de teléfono asociados a una cuenta de negocio."""
        try:
            url = f"{self.base_url}/{business_account_id}/phone_numbers"
            params = {
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo números de teléfono: {e}")
            return {}
    
    def setup_webhook(self, phone_number_id: str, webhook_url: str, verify_token: str) -> bool:
        """
        Configura el webhook para recibir mensajes.
        
        Args:
            phone_number_id: ID del número de teléfono
            webhook_url: URL del webhook
            verify_token: Token de verificación
            
        Returns:
            True si la configuración fue exitosa
        """
        try:
            # Configurar webhook
            url = f"{self.base_url}/{phone_number_id}/webhooks"
            data = {
                "callback_url": webhook_url,
                "verify_token": verify_token,
                "access_token": self.access_token
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            print(f"Webhook configurado exitosamente: {response.json()}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error configurando webhook: {e}")
            return False
    
    def send_test_message(self, phone_number_id: str, to_number: str, message: str) -> bool:
        """
        Envía un mensaje de prueba.
        
        Args:
            phone_number_id: ID del número de teléfono
            to_number: Número de destino
            message: Mensaje a enviar
            
        Returns:
            True si el mensaje fue enviado exitosamente
        """
        try:
            url = f"{self.base_url}/{phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            print(f"Mensaje de prueba enviado exitosamente: {response.json()}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error enviando mensaje de prueba: {e}")
            return False

def interactive_setup():
    """Configuración interactiva de WhatsApp Business API."""
    print("=== Configuración de WhatsApp Business API ===\n")
    
    # Solicitar credenciales
    access_token = input("Ingresa tu Access Token de Facebook: ").strip()
    app_id = input("Ingresa tu App ID de Facebook: ").strip()
    
    if not access_token or not app_id:
        print("Error: Access Token y App ID son requeridos.")
        return
    
    setup = WhatsAppSetup(access_token, app_id)
    
    # Obtener cuentas de negocio
    print("\n1. Obteniendo cuentas de negocio...")
    business_accounts = setup.get_business_accounts()
    
    if not business_accounts.get("whatsapp_business_accounts", {}).get("data"):
        print("No se encontraron cuentas de negocio de WhatsApp.")
        return
    
    accounts = business_accounts["whatsapp_business_accounts"]["data"]
    print(f"Cuentas encontradas: {len(accounts)}")
    
    for i, account in enumerate(accounts):
        print(f"  {i + 1}. {account['name']} (ID: {account['id']})")
    
    # Seleccionar cuenta
    try:
        account_index = int(input("\nSelecciona una cuenta (número): ")) - 1
        selected_account = accounts[account_index]
        business_account_id = selected_account["id"]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return
    
    # Obtener números de teléfono
    print(f"\n2. Obteniendo números de teléfono para {selected_account['name']}...")
    phone_numbers = setup.get_phone_numbers(business_account_id)
    
    if not phone_numbers.get("data"):
        print("No se encontraron números de teléfono.")
        return
    
    numbers = phone_numbers["data"]
    print(f"Números encontrados: {len(numbers)}")
    
    for i, number in enumerate(numbers):
        print(f"  {i + 1}. {number['display_phone_number']} (ID: {number['id']})")
    
    # Seleccionar número
    try:
        number_index = int(input("\nSelecciona un número (número): ")) - 1
        selected_number = numbers[number_index]
        phone_number_id = selected_number["id"]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return
    
    # Configurar webhook
    print(f"\n3. Configurando webhook para {selected_number['display_phone_number']}...")
    webhook_url = input("Ingresa la URL de tu webhook (ej: https://tu-dominio.com/api/whatsapp/webhook): ").strip()
    verify_token = input("Ingresa un token de verificación (cualquier string): ").strip()
    
    if webhook_url and verify_token:
        webhook_success = setup.setup_webhook(phone_number_id, webhook_url, verify_token)
        if not webhook_success:
            print("Advertencia: No se pudo configurar el webhook automáticamente.")
            print("Deberás configurarlo manualmente en la consola de Facebook.")
    
    # Mensaje de prueba opcional
    test_message = input("\n4. ¿Quieres enviar un mensaje de prueba? (s/n): ").strip().lower()
    if test_message == 's':
        to_number = input("Ingresa el número de destino (con código de país, ej: 521234567890): ").strip()
        message = input("Ingresa el mensaje de prueba: ").strip()
        
        if to_number and message:
            setup.send_test_message(phone_number_id, to_number, message)
    
    # Generar archivo de configuración
    print("\n5. Generando archivo de configuración...")
    config = {
        "WHATSAPP_ACCESS_TOKEN": access_token,
        "WHATSAPP_PHONE_NUMBER_ID": phone_number_id,
        "WHATSAPP_VERIFY_TOKEN": verify_token,
        "WHATSAPP_BUSINESS_ACCOUNT_ID": business_account_id,
        "WEBHOOK_URL": webhook_url
    }
    
    with open(".env", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print("Archivo .env creado con la configuración.")
    print("\n=== Configuración completada ===")
    print("Pasos siguientes:")
    print("1. Verifica que tu webhook esté accesible públicamente")
    print("2. Configura el webhook en la consola de Facebook si no se hizo automáticamente")
    print("3. Inicia tu aplicación Flask")
    print("4. Envía un mensaje a tu número de WhatsApp Business para probar")

if __name__ == "__main__":
    interactive_setup()

