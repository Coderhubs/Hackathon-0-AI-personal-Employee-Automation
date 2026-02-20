"""
WhatsApp System Launcher
Starts Flask webhook server with proper encoding
"""
import sys
import os
import subprocess
import time
import requests

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def check_ngrok():
    """Check if ngrok is running and get public URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
        data = response.json()
        if data.get('tunnels'):
            tunnel = data['tunnels'][0]
            return tunnel.get('public_url')
    except:
        return None

def start_flask_server():
    """Start Flask webhook server"""
    print("=" * 70)
    print("WhatsApp Webhook System - Starting")
    print("=" * 70)
    print()

    # Check if ngrok is running
    ngrok_url = check_ngrok()
    if ngrok_url:
        print(f"✓ ngrok is running")
        print(f"  Public URL: {ngrok_url}")
        print()
        print("Configure this URL in Twilio:")
        print(f"  {ngrok_url}/whatsapp")
        print()
    else:
        print("⚠ ngrok is NOT running")
        print("  Start ngrok first: ngrok http 5000")
        print()

    print("Starting Flask webhook server...")
    print("=" * 70)
    print()

    # Set environment variables for UTF-8 encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'

    # Start Flask server
    try:
        subprocess.run(
            [sys.executable, 'whatsapp_receive.py'],
            env=env,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        print("=" * 70)

if __name__ == "__main__":
    start_flask_server()
