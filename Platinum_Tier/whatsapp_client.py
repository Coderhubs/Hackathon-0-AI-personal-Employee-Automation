"""
Python Client for WhatsApp Automation API
Communicates with Node.js WhatsApp server
"""
import requests
import time
import logging
from typing import Dict, List, Optional

class WhatsAppClient:
    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url
        self.logger = logging.getLogger('WhatsAppClient')

    def initialize(self, timeout: int = 120) -> bool:
        """Initialize WhatsApp connection"""
        try:
            self.logger.info("Initializing WhatsApp...")
            response = requests.post(
                f"{self.base_url}/api/whatsapp/initialize",
                timeout=timeout
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.logger.info("[OK] WhatsApp initialized successfully")
                    return True

            self.logger.error(f"Failed to initialize WhatsApp: {response.text}")
            return False

        except Exception as e:
            self.logger.error(f"Error initializing WhatsApp: {e}")
            return False

    def send_message(self, contact: str, message: str) -> Dict:
        """Send WhatsApp message"""
        try:
            self.logger.info(f"Sending message to {contact}...")

            response = requests.post(
                f"{self.base_url}/api/whatsapp/send",
                json={
                    'contact': contact,
                    'message': message
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.logger.info(f"[OK] Message sent to {contact}")
                    return result
                else:
                    self.logger.error(f"Failed to send message: {result.get('error')}")
                    return result
            else:
                self.logger.error(f"HTTP error: {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return {'success': False, 'error': str(e)}

    def get_chats(self) -> List[Dict]:
        """Get list of WhatsApp chats"""
        try:
            response = requests.get(
                f"{self.base_url}/api/whatsapp/chats",
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return result.get('chats', [])

            return []

        except Exception as e:
            self.logger.error(f"Error getting chats: {e}")
            return []

    def get_status(self) -> Dict:
        """Get WhatsApp connection status"""
        try:
            response = requests.get(
                f"{self.base_url}/api/whatsapp/status",
                timeout=5
            )

            if response.status_code == 200:
                return response.json()

            return {'initialized': False, 'ready': False}

        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {'initialized': False, 'ready': False}

    def wait_for_ready(self, timeout: int = 120) -> bool:
        """Wait for WhatsApp to be ready"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_status()
            if status.get('ready'):
                self.logger.info("[OK] WhatsApp is ready")
                return True

            time.sleep(2)

        self.logger.error("Timeout waiting for WhatsApp to be ready")
        return False
