#!/usr/bin/env python3
"""
Manual Gmail Test Script
Run this to test Gmail automation manually
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add Platinum_Tier to path
sys.path.insert(0, str(Path(__file__).parent / "Platinum_Tier"))

from gmail_sender_smtp import GmailSender

load_dotenv()

def main():
    print("="*70)
    print("MANUAL GMAIL TEST")
    print("="*70)

    email = os.getenv('GMAIL_ADDRESS')
    password = os.getenv('GMAIL_APP_PASSWORD')

    if not email or not password:
        print("\n❌ ERROR: Gmail credentials not found in .env")
        print("Required: GMAIL_ADDRESS and GMAIL_APP_PASSWORD")
        return 1

    print(f"\nSending test email to: {email}")
    print("Please wait...\n")

    sender = GmailSender(email, password)

    result = sender.send_email(
        to_email=email,
        subject='✅ Manual Test - AI Personal Employee',
        body='''This is a manual test of the AI Personal Employee system.

Gmail automation is working correctly!

Test Details:
- Sent via SMTP
- Using App Password authentication
- Automated by AI Employee system

If you received this email, Gmail automation is fully functional.
'''
    )

    if result:
        print("\n" + "="*70)
        print("✅ SUCCESS - Gmail Test Passed")
        print("="*70)
        print(f"\nCheck your inbox: {email}")
        print("\nGmail automation is working perfectly!")
        return 0
    else:
        print("\n" + "="*70)
        print("❌ FAILED - Gmail Test Failed")
        print("="*70)
        print("\nCheck the logs for error details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
