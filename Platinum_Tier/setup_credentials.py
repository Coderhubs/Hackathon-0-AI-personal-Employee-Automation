"""
Interactive script to set up credentials for LinkedIn and Gmail watchers
"""
import os
from pathlib import Path
import getpass

def setup_credentials():
    """Interactive credential setup"""
    print("=" * 60)
    print("LinkedIn & Gmail Watcher - Credential Setup")
    print("=" * 60)
    print("\nThis script will help you set up your credentials securely.")
    print("Your credentials will be stored in a .env file (NOT committed to git).\n")

    # Get project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    # Check if .env already exists
    if env_file.exists():
        overwrite = input("\n.env file already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return

    print("\n" + "-" * 60)
    print("LINKEDIN CREDENTIALS")
    print("-" * 60)
    linkedin_email = input("Enter your LinkedIn email: ").strip()
    linkedin_password = getpass.getpass("Enter your LinkedIn password: ").strip()

    print("\n" + "-" * 60)
    print("GMAIL CREDENTIALS")
    print("-" * 60)
    print("\nIMPORTANT: If you have 2FA enabled on Gmail, you MUST use an App Password.")
    print("Generate one at: https://myaccount.google.com/apppasswords\n")

    gmail_email = input("Enter your Gmail address: ").strip()
    gmail_password = getpass.getpass("Enter your Gmail password (or App Password): ").strip()

    # Write to .env file
    with open(env_file, 'w') as f:
        f.write("# LinkedIn Credentials\n")
        f.write(f"LINKEDIN_EMAIL={linkedin_email}\n")
        f.write(f"LINKEDIN_PASSWORD={linkedin_password}\n")
        f.write("\n")
        f.write("# Gmail Credentials\n")
        f.write(f"GMAIL_EMAIL={gmail_email}\n")
        f.write(f"GMAIL_PASSWORD={gmail_password}\n")

    print("\n" + "=" * 60)
    print("✓ Credentials saved successfully to .env file")
    print("=" * 60)
    print("\nIMPORTANT SECURITY NOTES:")
    print("1. Never commit the .env file to git")
    print("2. Keep your credentials secure")
    print("3. Use App Passwords for Gmail (not your main password)")
    print("4. LinkedIn may require verification on first login")
    print("\nYou can now run the watchers:")
    print("  python Platinum_Tier/linkedin_watcher_playwright.py")
    print("  python Platinum_Tier/gmail_watcher_playwright.py")
    print()

if __name__ == "__main__":
    try:
        setup_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
