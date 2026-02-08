"""
Quick Demo Script - Test Both Mock and Real Watchers
This script demonstrates the difference between mock and real implementations
"""
import os
import sys
from pathlib import Path
import time

def demo_mock_watchers():
    """Demonstrate mock watchers"""
    print("=" * 70)
    print("DEMO: MOCK WATCHERS (Fake Data)")
    print("=" * 70)
    print("\nMock watchers create fake emails and LinkedIn posts for testing.")
    print("They work immediately without any credentials.\n")

    print("To run mock watchers:")
    print("  python gmail_watcher.py")
    print("  python linkedin_watcher.py")
    print("\nThey will create files like:")
    print("  Inbox/GMAIL_20260208_123456_Subject.txt")
    print("  Inbox/LINKEDIN_trend_20260208_123456.txt")
    print("\n" + "=" * 70)

def demo_real_watchers():
    """Demonstrate real Playwright watchers"""
    print("\n" + "=" * 70)
    print("DEMO: REAL PLAYWRIGHT WATCHERS (Actual Data)")
    print("=" * 70)
    print("\nReal watchers use browser automation to fetch actual emails/posts.")
    print("They require your credentials in the .env file.\n")

    # Check if credentials are configured
    from dotenv import load_dotenv
    load_dotenv()

    gmail_email = os.getenv('GMAIL_EMAIL')
    linkedin_email = os.getenv('LINKEDIN_EMAIL')

    if gmail_email and gmail_email != 'your_gmail_email@gmail.com':
        print(f"[OK] Gmail configured: {gmail_email}")
    else:
        print("[NOT CONFIGURED] Gmail NOT configured (edit .env file)")

    if linkedin_email and linkedin_email != 'your_linkedin_email@example.com':
        print(f"[OK] LinkedIn configured: {linkedin_email}")
    else:
        print("[NOT CONFIGURED] LinkedIn NOT configured (edit .env file)")

    print("\nTo run real watchers (after configuring .env):")
    print("  python gmail_watcher_playwright.py")
    print("  python linkedin_watcher_playwright.py")
    print("\nThey will:")
    print("  1. Open a Chrome browser window")
    print("  2. Login to Gmail/LinkedIn automatically")
    print("  3. Fetch real emails/posts every 2-3 minutes")
    print("  4. Save them to Inbox/ folder")
    print("\n" + "=" * 70)

def show_inbox_samples():
    """Show sample files from Inbox"""
    print("\n" + "=" * 70)
    print("CURRENT INBOX CONTENTS")
    print("=" * 70)

    inbox_dir = Path("Inbox")
    if not inbox_dir.exists():
        print("\nInbox directory doesn't exist yet.")
        return

    files = sorted(inbox_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)

    if not files:
        print("\nNo files in Inbox yet.")
        return

    print(f"\nTotal files: {len(files)}")
    print("\nMost recent 5 files:")
    print("-" * 70)

    for i, file in enumerate(files[:5], 1):
        size = file.stat().st_size
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file.stat().st_mtime))
        print(f"{i}. {file.name}")
        print(f"   Size: {size} bytes | Modified: {mtime}")

        # Show first 2 lines of content
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:2]
                for line in lines:
                    print(f"   {line.strip()}")
        except:
            pass
        print()

    print("=" * 70)

def show_next_steps():
    """Show what to do next"""
    print("\n" + "=" * 70)
    print("WHAT TO DO NEXT")
    print("=" * 70)

    print("\nOption 1: Test with Mock Watchers (Recommended First)")
    print("-" * 70)
    print("1. Open a terminal")
    print("2. Run: python gmail_watcher.py")
    print("3. Watch as it creates fake emails every 3 minutes")
    print("4. Press Ctrl+C to stop")
    print("5. Check Inbox/ folder for new files")

    print("\nOption 2: Use Real Playwright Watchers")
    print("-" * 70)
    print("1. Edit .env file and add your credentials:")
    print("   GMAIL_EMAIL=your_email@gmail.com")
    print("   GMAIL_PASSWORD=your_app_password")
    print("   LINKEDIN_EMAIL=your_email@example.com")
    print("   LINKEDIN_PASSWORD=your_password")
    print()
    print("2. For Gmail, use App Password (not main password):")
    print("   https://myaccount.google.com/apppasswords")
    print()
    print("3. Run: python gmail_watcher_playwright.py")
    print("4. A Chrome window will open and login automatically")
    print("5. Watch as it fetches real emails")
    print("6. Press Ctrl+C to stop")

    print("\nOption 3: Run Both in Background")
    print("-" * 70)
    print("# Windows")
    print("start /B python gmail_watcher_playwright.py")
    print("start /B python linkedin_watcher_playwright.py")
    print()
    print("# Or use PM2")
    print("pm2 start gmail_watcher_playwright.py --name gmail")
    print("pm2 start linkedin_watcher_playwright.py --name linkedin")
    print("pm2 list")

    print("\n" + "=" * 70)

def main():
    """Main demo function"""
    print("\n")
    print("=" * 70)
    print(" " * 15 + "GMAIL & LINKEDIN WATCHERS - DEMO")
    print("=" * 70)

    demo_mock_watchers()
    demo_real_watchers()
    show_inbox_samples()
    show_next_steps()

    print("\n" + "=" * 70)
    print("SETUP COMPLETE! Choose your path and start watching!")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
