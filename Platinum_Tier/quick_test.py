"""
SIMPLE CLI TESTER - Create Fake Emails & Posts Instantly
=========================================================

This script lets you create fake Gmail emails and LinkedIn posts
from the command line to test your AI Employee system.

Usage: python quick_test.py
"""

from datetime import datetime
import os
import time

def create_fake_gmail(subject="Test Email", body="This is a test email."):
    """Create a fake Gmail email file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_subject = subject.replace(" ", "_").replace(":", "").replace("/", "_")
    filename = f"Inbox/GMAIL_{timestamp}_{safe_subject}.txt"

    content = f"""Subject: {subject}
From: sender@example.com
To: you@company.com
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
{body}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Created Gmail: {filename}")
    return filename

def create_fake_linkedin(content="Test LinkedIn post"):
    """Create a fake LinkedIn post file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Inbox/LINKEDIN_trend_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Created LinkedIn: {filename}")
    return filename

def show_stats():
    """Show current file statistics"""
    inbox_count = len([f for f in os.listdir('Inbox') if os.path.isfile(os.path.join('Inbox', f))])
    needs_action_count = len([f for f in os.listdir('Needs_Action') if os.path.isfile(os.path.join('Needs_Action', f))])
    done_count = len([f for f in os.listdir('Done') if os.path.isfile(os.path.join('Done', f))])

    print(f"\nCurrent Statistics:")
    print(f"  Inbox: {inbox_count} files")
    print(f"  Needs_Action: {needs_action_count} files")
    print(f"  Done: {done_count} files")

def main():
    """Main interactive menu"""
    print("=" * 60)
    print("FAKE GMAIL/LINKEDIN CLI TESTER")
    print("=" * 60)
    print()

    while True:
        print("\nChoose an option:")
        print("1. Create fake Gmail email")
        print("2. Create fake LinkedIn post")
        print("3. Create both (Gmail + LinkedIn)")
        print("4. Create 5 fake emails")
        print("5. Create 5 fake posts")
        print("6. Show statistics")
        print("7. Quick test (1 email + 1 post)")
        print("8. Exit")
        print()

        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            subject = input("Enter email subject (or press Enter for default): ").strip()
            if not subject:
                subject = "Test Email"
            body = input("Enter email body (or press Enter for default): ").strip()
            if not body:
                body = "This is a test email created from CLI."
            create_fake_gmail(subject, body)

        elif choice == "2":
            content = input("Enter LinkedIn post content (or press Enter for default): ").strip()
            if not content:
                content = "This is a test LinkedIn post"
            create_fake_linkedin(content)

        elif choice == "3":
            create_fake_gmail("Quick Test", "Testing both systems")
            time.sleep(0.5)
            create_fake_linkedin("Quick test post")

        elif choice == "4":
            print("\nCreating 5 fake emails...")
            for i in range(1, 6):
                create_fake_gmail(f"Test Email {i}", f"This is test email number {i}")
                time.sleep(0.5)
            print("Done!")

        elif choice == "5":
            print("\nCreating 5 fake posts...")
            for i in range(1, 6):
                create_fake_linkedin(f"Test LinkedIn post number {i}")
                time.sleep(0.5)
            print("Done!")

        elif choice == "6":
            show_stats()

        elif choice == "7":
            print("\nQuick test - creating 1 email and 1 post...")
            create_fake_gmail("Quick Test", "Quick test email")
            time.sleep(0.5)
            create_fake_linkedin("Quick test post")
            print("\nWaiting 3 seconds for processing...")
            time.sleep(3)
            show_stats()
            print("\nCheck Dashboard.md to see them being processed!")

        elif choice == "8":
            print("\nExiting...")
            break

        else:
            print("Invalid choice. Please enter 1-8.")

        print("\nFiles will be processed automatically by filesystem watcher!")

if __name__ == "__main__":
    main()
