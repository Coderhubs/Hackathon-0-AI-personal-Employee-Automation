"""
WhatsApp Message Sender using Twilio
Sends WhatsApp messages and logs them
"""
import sys
import os
from datetime import datetime
from pathlib import Path
from twilio.rest import Client
import logging

class WhatsAppSender:
    def __init__(self, config_file='.whatsapp_config'):
        self.config = self.load_config(config_file)
        self.client = Client(
            self.config['TWILIO_ACCOUNT_SID'],
            self.config['TWILIO_AUTH_TOKEN']
        )
        self.sent_dir = Path("WhatsApp_Vault/Sent")
        self.sent_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()

    def load_config(self, config_file):
        """Load Twilio credentials from config file"""
        config = {}
        config_path = Path(config_file)

        if not config_path.exists():
            print(f"[ERROR] Config file not found: {config_file}")
            print("Please create .whatsapp_config file with your Twilio credentials")
            sys.exit(1)

        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

        # Validate required fields
        required = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_WHATSAPP_NUMBER']
        for field in required:
            if field not in config or config[field] == 'your_auth_token_here':
                print(f"[ERROR] {field} not configured in .whatsapp_config")
                sys.exit(1)

        return config

    def setup_logging(self):
        """Setup logging"""
        log_dir = Path("AI_Employee_Vault/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'whatsapp_sender.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('WhatsAppSender')

    def send_message(self, to_number, message_body):
        """
        Send WhatsApp message via Twilio

        Args:
            to_number: Recipient number (format: whatsapp:+923001234567)
            message_body: Message text to send

        Returns:
            dict: Success status and message SID
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'

            self.logger.info(f"Sending WhatsApp message to {to_number}...")

            # Send message via Twilio
            message = self.client.messages.create(
                from_=self.config['TWILIO_WHATSAPP_NUMBER'],
                body=message_body,
                to=to_number
            )

            self.logger.info(f"[SUCCESS] Message sent! SID: {message.sid}")

            # Log to file
            self.log_sent_message(to_number, message_body, message.sid)

            return {
                'success': True,
                'sid': message.sid,
                'to': to_number,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"[FAILED] Error sending message: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def log_sent_message(self, to_number, message_body, sid):
        """Log sent message to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SENT_{timestamp}.txt"
        filepath = self.sent_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== WhatsApp Message Sent ===\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"To: {to_number}\n")
            f.write(f"Message SID: {sid}\n")
            f.write(f"Status: Sent\n")
            f.write(f"\n--- Message ---\n")
            f.write(message_body)
            f.write(f"\n\n--- End ---\n")

        self.logger.info(f"Logged to: {filepath}")

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python whatsapp_send.py <to_number> <message>")
        print("Example: python whatsapp_send.py '+923001234567' 'Hello from AI!'")
        sys.exit(1)

    to_number = sys.argv[1]
    message = ' '.join(sys.argv[2:])

    sender = WhatsAppSender()
    result = sender.send_message(to_number, message)

    if result['success']:
        print(f"\n[OK] Message sent successfully!")
        print(f"SID: {result['sid']}")
    else:
        print(f"\n[ERROR] Failed to send message")
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    main()
