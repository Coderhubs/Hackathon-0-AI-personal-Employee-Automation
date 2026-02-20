"""
WhatsApp Auto-Reply Bot using Twilio
Receives messages and sends intelligent auto-replies
"""
from flask import Flask, request
from datetime import datetime
from pathlib import Path
import logging
from whatsapp_send import WhatsAppSender

app = Flask(__name__)

# Setup logging
log_dir = Path("AI_Employee_Vault/Logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'whatsapp_autoreply.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WhatsAppAutoReply')

# Create directories
conversations_dir = Path("WhatsApp_Vault/Conversations")
conversations_dir.mkdir(parents=True, exist_ok=True)

# Initialize sender
sender = WhatsAppSender()

def generate_reply(message_body):
    """Generate intelligent auto-reply based on message content"""
    message_lower = message_body.lower()

    # Rule-based responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'salam']):
        return "Hello! 👋 I am an AI assistant. How can I help you today?"

    elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'kitna']):
        return "Please contact us at business@email.com for pricing details. 💰"

    elif any(word in message_lower for word in ['time', 'hours', 'timing', 'kab']):
        return "We are available Monday-Friday, 9am-6pm. 🕐"

    elif any(word in message_lower for word in ['help', 'support', 'madad']):
        return "I can help you with:\n1) Product info\n2) Pricing\n3) Support\n\nWhat do you need? 🤔"

    elif any(word in message_lower for word in ['demo', 'test', 'hackathon']):
        return "This is an AI automation system demo for the hackathon! 🚀\n\nIt can:\n- Monitor WhatsApp 24/7\n- Auto-reply to messages\n- Log all conversations\n\nPretty cool, right? 😎"

    else:
        return "Thank you for your message! Our team will get back to you soon. 🙏"

def log_conversation(from_number, incoming_message, outgoing_reply):
    """Log conversation to daily file"""
    today = datetime.now().strftime("%Y%m%d")
    filename = f"CONV_{today}.txt"
    filepath = conversations_dir / filename

    # Append to daily conversation log
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"From: {from_number}\n")
        f.write(f"\n[INCOMING]\n{incoming_message}\n")
        f.write(f"\n[AUTO-REPLY]\n{outgoing_reply}\n")
        f.write(f"{'=' * 60}\n")

    logger.info(f"Conversation logged to: {filepath}")

@app.route('/whatsapp', methods=['POST'])
def whatsapp_autoreply():
    """Handle incoming messages and send auto-replies"""
    try:
        # Get message data
        from_number = request.form.get('From', '')
        message_body = request.form.get('Body', '')
        message_sid = request.form.get('MessageSid', '')

        logger.info(f"[RECEIVED] Message from {from_number}")
        logger.info(f"Content: {message_body}")

        # Print incoming message
        print("\n" + "=" * 60)
        print(f"📱 INCOMING MESSAGE")
        print("=" * 60)
        print(f"From: {from_number}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"\nMessage: {message_body}")
        print("=" * 60)

        # Generate auto-reply
        reply_message = generate_reply(message_body)

        # Send auto-reply
        logger.info(f"[AUTO-REPLY] Sending reply to {from_number}")
        result = sender.send_message(from_number, reply_message)

        if result['success']:
            print(f"\n✅ AUTO-REPLY SENT")
            print(f"Reply: {reply_message}")
            print("=" * 60 + "\n")
        else:
            print(f"\n❌ FAILED TO SEND REPLY")
            print(f"Error: {result.get('error')}")
            print("=" * 60 + "\n")

        # Log conversation
        log_conversation(from_number, message_body, reply_message)

        return '', 200

    except Exception as e:
        logger.error(f"Error in auto-reply: {e}")
        return str(e), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return {
        'status': 'running',
        'mode': 'auto-reply',
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    import sys
    import io

    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    print("=" * 60)
    print("WhatsApp Auto-Reply Bot - ACTIVE")
    print("=" * 60)
    print()
    print("Bot Features:")
    print("  - Receives WhatsApp messages")
    print("  - Generates intelligent replies")
    print("  - Responds within 5 seconds")
    print("  - Logs all conversations")
    print()
    print("Server: http://localhost:5000")
    print("Webhook: http://localhost:5000/whatsapp")
    print()
    print("SETUP REQUIRED:")
    print("1. Run: ngrok http 5000")
    print("2. Copy ngrok URL (https://xxxx.ngrok.io)")
    print("3. Set in Twilio Console:")
    print("   Messaging -> WhatsApp Sandbox -> Webhook URL")
    print("   https://your-ngrok-url.ngrok.io/whatsapp")
    print()
    print("Waiting for messages...")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=5000, debug=False)
