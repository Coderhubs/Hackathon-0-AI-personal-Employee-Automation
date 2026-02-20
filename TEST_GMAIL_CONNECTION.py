"""
Quick test script to verify Gmail IMAP connection
"""
import os
import imaplib
from dotenv import load_dotenv

load_dotenv()

def test_gmail_connection():
    print("=" * 60)
    print("Gmail IMAP Connection Test")
    print("=" * 60)
    print()

    email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        print("❌ ERROR: GMAIL_EMAIL or GMAIL_PASSWORD not found in .env file")
        print()
        print("Please make sure your .env file contains:")
        print("  GMAIL_EMAIL=your_email@gmail.com")
        print("  GMAIL_PASSWORD=your_app_password")
        return False

    print(f"[*] Email: {email}")
    print(f"[*] Password: {'*' * len(password)} ({len(password)} characters)")
    print()

    # Check if it looks like an App Password (16 chars, no spaces)
    if len(password) != 16 or ' ' in password:
        print("[!] WARNING: This doesn't look like a Gmail App Password")
        print("   App Passwords are exactly 16 characters with no spaces")
        print("   Example: abcdefghijklmnop")
        print()
        print("   If you're using your regular Gmail password, you need to:")
        print("   1. Enable 2-Step Verification")
        print("   2. Generate an App Password at: https://myaccount.google.com/apppasswords")
        print()

    print("Attempting to connect to Gmail IMAP server...")
    print()

    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        print("✓ Connected to imap.gmail.com")

        # Login
        mail.login(email, password)
        print("✓ Login successful!")

        # Select inbox
        mail.select("INBOX")
        print("✓ Inbox accessed")

        # Get email count
        status, messages = mail.search(None, "ALL")
        email_count = len(messages[0].split())
        print(f"✓ Found {email_count} total emails in inbox")

        # Check for unread emails
        status, unread = mail.search(None, "UNSEEN")
        unread_count = len(unread[0].split()) if unread[0] else 0
        print(f"✓ Found {unread_count} unread emails")

        # Logout
        mail.logout()
        print("✓ Disconnected")

        print()
        print("=" * 60)
        print("✅ SUCCESS! Gmail IMAP connection is working!")
        print("=" * 60)
        print()
        print("You can now run the Gmail watcher with:")
        print("  RUN_GMAIL_WATCHER.bat")
        print()
        return True

    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP Error: {e}")
        print()
        print("Common causes:")
        print("  1. Wrong email or password")
        print("  2. Using regular password instead of App Password")
        print("  3. 2-Step Verification not enabled")
        print("  4. IMAP not enabled in Gmail settings")
        print()
        print("Solutions:")
        print("  1. Generate App Password: https://myaccount.google.com/apppasswords")
        print("  2. Enable IMAP: Gmail Settings → Forwarding and POP/IMAP → Enable IMAP")
        print()
        return False

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print()
        return False

if __name__ == "__main__":
    test_gmail_connection()
    input("\nPress Enter to exit...")
