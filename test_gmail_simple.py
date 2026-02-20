"""
Simple Gmail IMAP connection test - Windows compatible
"""
import os
import imaplib
from dotenv import load_dotenv

load_dotenv()

def test_gmail():
    print("=" * 60)
    print("Gmail IMAP Connection Test")
    print("=" * 60)
    print()

    email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        print("[ERROR] GMAIL_EMAIL or GMAIL_PASSWORD not found in .env file")
        return False

    print(f"Email: {email}")
    print(f"Password: {'*' * len(password)} ({len(password)} characters)")
    print()

    if len(password) != 16:
        print("[WARNING] App Password should be exactly 16 characters")
        print()

    print("Connecting to Gmail IMAP server...")

    try:
        # Connect
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        print("[OK] Connected to imap.gmail.com")

        # Login
        mail.login(email, password)
        print("[OK] Login successful!")

        # Select inbox
        mail.select("INBOX")
        print("[OK] Inbox accessed")

        # Get email count
        status, messages = mail.search(None, "ALL")
        email_count = len(messages[0].split())
        print(f"[OK] Found {email_count} total emails")

        # Check unread
        status, unread = mail.search(None, "UNSEEN")
        unread_count = len(unread[0].split()) if unread[0] else 0
        print(f"[OK] Found {unread_count} unread emails")

        # Logout
        mail.logout()
        print("[OK] Disconnected")

        print()
        print("=" * 60)
        print("[SUCCESS] Gmail IMAP is working perfectly!")
        print("=" * 60)
        print()
        print("You can now run: RUN_GMAIL_WATCHER.bat")
        print()
        return True

    except imaplib.IMAP4.error as e:
        print(f"[ERROR] IMAP Error: {e}")
        print()
        print("Common solutions:")
        print("1. Make sure you're using App Password (not regular password)")
        print("2. Generate new App Password at:")
        print("   https://myaccount.google.com/apppasswords")
        print("3. Enable IMAP in Gmail Settings")
        print()
        return False

    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print()
        return False

if __name__ == "__main__":
    test_gmail()
    input("\nPress Enter to exit...")
