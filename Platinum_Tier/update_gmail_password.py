"""
Quick Gmail App Password Setup
Run this after you generate your App Password
"""
import os
from pathlib import Path

def update_gmail_password():
    """Update Gmail password in .env file"""
    print("=" * 60)
    print("Gmail App Password Update")
    print("=" * 60)
    print("\nFirst, generate an App Password:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Sign in and generate a password for 'Mail'")
    print("3. Copy the 16-character password")
    print()

    app_password = input("Paste your App Password here (16 chars): ").strip().replace(" ", "")

    if len(app_password) != 16:
        print(f"\nError: App Password should be 16 characters (you entered {len(app_password)})")
        return

    # Read current .env
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path, 'r') as f:
        lines = f.readlines()

    # Update Gmail password line
    with open(env_path, 'w') as f:
        for line in lines:
            if line.startswith('GMAIL_PASSWORD='):
                f.write(f'GMAIL_PASSWORD={app_password}\n')
            else:
                f.write(line)

    print("\n[SUCCESS] Gmail App Password updated in .env file!")
    print("\nNow test it: python demo_gmail.py")

if __name__ == "__main__":
    try:
        update_gmail_password()
    except Exception as e:
        print(f"\nError: {e}")
