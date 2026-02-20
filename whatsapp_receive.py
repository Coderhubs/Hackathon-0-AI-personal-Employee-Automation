"""
WhatsApp Message Receiver using Twilio Webhook
Flask server to receive incoming WhatsApp messages
"""
from flask import Flask, request
from datetime import datetime
from pathlib import Path
import logging

app = Flask(__name__)

# Setup logging
log_dir = Path("AI_Employee_Vault/Logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'whatsapp_receiver.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WhatsAppReceiver')

# Create inbox directory
inbox_dir = Path("WhatsApp_Vault/Inbox")
inbox_dir.mkdir(parents=True, exist_ok=True)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get message data from Twilio
        from_number = request.form.get('From', '')
        message_body = request.form.get('Body', '')
        message_sid = request.form.get('MessageSid', '')

        logger.info(f"[RECEIVED] Message from {from_number}")
        logger.info(f"Content: {message_body}")

        # Save to file
        save_incoming_message(from_number, message_body, message_sid)

        # Print to console
        print("\n" + "=" * 60)
        print(f"📱 NEW WHATSAPP MESSAGE")
        print("=" * 60)
        print(f"From: {from_number}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nMessage:")
        print(message_body)
        print("=" * 60 + "\n")

        return '', 200

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return str(e), 500

def save_incoming_message(from_number, message_body, sid):
    """Save incoming message to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"MSG_{timestamp}.txt"
    filepath = inbox_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"=== WhatsApp Message Received ===\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"From: {from_number}\n")
        f.write(f"Message SID: {sid}\n")
        f.write(f"\n--- Message ---\n")
        f.write(message_body)
        f.write(f"\n\n--- End ---\n")

    logger.info(f"Saved to: {filepath}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {'status': 'running', 'timestamp': datetime.now().isoformat()}

if __name__ == "__main__":
    print("=" * 60)
    print("WhatsApp Receiver - Webhook Server")
    print("=" * 60)
    print()
    print("Server starting on: http://localhost:5000")
    print("Webhook URL: http://localhost:5000/whatsapp")
    print()
    print("IMPORTANT: To receive messages, you need to:")
    print("1. Expose this server using ngrok:")
    print("   ngrok http 5000")
    print()
    print("2. Set webhook URL in Twilio Console:")
    print("   Messaging → Settings → WhatsApp Sandbox")
    print("   When a message comes in: https://your-ngrok-url.ngrok.io/whatsapp")
    print()
    print("Waiting for incoming messages...")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=False)
