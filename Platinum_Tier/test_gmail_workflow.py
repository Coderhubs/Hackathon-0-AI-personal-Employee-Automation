"""
Send a test email to trigger the Gmail watcher
"""
import os
from pathlib import Path
from gmail_sender_smtp import GmailSender
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(Path(__file__).parent.parent / '.env')

email = os.getenv("GMAIL_EMAIL")
password = os.getenv("GMAIL_PASSWORD")

sender = GmailSender(email, password)

# Send test email to yourself with Agentic AI keywords
result = sender.send_email(
    to_email=email,
    subject=f"Test: Agentic AI System Check - {datetime.now().strftime('%H:%M')}",
    body="""Hello!

This is a test email to trigger your AI Personal Employee system.

Keywords: Agentic AI, autonomous agent, LLM automation

The Gmail watcher should detect this email within 3 minutes and save it to:
AI_Employee_Vault/Needs_Action/

Then you can create a reply in:
AI_Employee_Vault/Approved/

And the system will automatically send it!

---
Test sent at: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
)

if result['success']:
    print("=" * 60)
    print("[SUCCESS] Test email sent!")
    print("=" * 60)
    print()
    print("What happens next:")
    print("1. Wait 3 minutes (or less)")
    print("2. Gmail watcher will detect the email")
    print("3. Email saved to: AI_Employee_Vault/Needs_Action/")
    print("4. Check the folder to see the detected email")
    print()
    print("To test sending:")
    print("1. Create a reply file in: AI_Employee_Vault/Approved/")
    print("2. System will automatically send it")
    print()
else:
    print(f"[ERROR] {result.get('error')}")
