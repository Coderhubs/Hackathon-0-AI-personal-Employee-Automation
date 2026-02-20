#!/usr/bin/env python3
"""
Gmail Login Setup - One-time login to save session
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def setup_gmail_login():
    """Setup Gmail login and save persistent session"""

    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')

    if not email or not password:
        print("[ERROR] GMAIL_EMAIL and GMAIL_PASSWORD not found in .env file")
        return False

    print("=" * 60)
    print("Gmail Login Setup")
    print("=" * 60)
    print(f"Email: {email}")
    print("=" * 60)

    # Create browser data directory
    browser_data_dir = Path(__file__).parent / "browser_data" / "gmail"
    browser_data_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[INFO] Browser data will be saved to: {browser_data_dir}")

    try:
        with sync_playwright() as p:
            print("\n[INFO] Launching browser...")

            # Launch browser with persistent context
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(browser_data_dir),
                headless=False,  # Show browser so you can see the login
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox'
                ]
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            print("[INFO] Navigating to Gmail login page...")
            page.goto('https://mail.google.com', wait_until='networkidle')

            # Check if already logged in
            if 'mail.google.com/mail' in page.url:
                print("\n[SUCCESS] Already logged in! Session is saved.")
                browser.close()
                return True

            print("[INFO] Filling in email...")

            # Wait for email input
            page.wait_for_selector('input[type="email"]', timeout=10000)
            page.fill('input[type="email"]', email)
            time.sleep(1)

            print("[INFO] Clicking Next...")
            page.click('button:has-text("Next"), div[role="button"]:has-text("Next")')
            time.sleep(3)

            print("[INFO] Filling in password...")

            # Wait for password input
            page.wait_for_selector('input[type="password"]', timeout=10000)
            page.fill('input[type="password"]', password)
            time.sleep(1)

            print("[INFO] Clicking Next...")
            page.click('button:has-text("Next"), div[role="button"]:has-text("Next")')

            # Wait for navigation
            print("[INFO] Waiting for login to complete...")
            time.sleep(10)

            # Check if login successful
            current_url = page.url

            if 'mail.google.com/mail' in current_url:
                print("\n[SUCCESS] Login successful! Session saved.")
                print(f"Current URL: {current_url}")

                # Keep browser open for 10 seconds so you can see it worked
                print("\n[INFO] Keeping browser open for 10 seconds...")
                time.sleep(10)

                browser.close()
                return True

            elif 'challenge' in current_url or 'signin/v2/challenge' in current_url:
                print("\n[WARNING] Google security challenge detected!")
                print("Please complete the challenge in the browser window.")
                print("This might be:")
                print("  - 2-Factor Authentication (2FA)")
                print("  - Phone verification")
                print("  - Security question")
                print("\nThe browser will stay open for 3 minutes.")
                print("After completing the challenge, the session will be saved.")

                # Wait 3 minutes for user to complete challenge
                time.sleep(180)

                # Check again
                if 'mail.google.com/mail' in page.url:
                    print("\n[SUCCESS] Challenge completed! Session saved.")
                    browser.close()
                    return True
                else:
                    print("\n[ERROR] Challenge not completed. Please try again.")
                    print(f"Current URL: {page.url}")
                    browser.close()
                    return False

            else:
                print(f"\n[ERROR] Login failed. Current URL: {current_url}")
                print("\nPossible issues:")
                print("1. Wrong password")
                print("2. 2FA enabled - you need an App Password")
                print("   Generate at: https://myaccount.google.com/apppasswords")
                print("3. Account locked or requires verification")

                # Keep browser open so you can see what happened
                print("\n[INFO] Keeping browser open for 30 seconds...")
                time.sleep(30)

                browser.close()
                return False

    except Exception as e:
        print(f"\n[ERROR] Error during login: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n[START] Starting Gmail login setup...\n")

    success = setup_gmail_login()

    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] Gmail login setup complete!")
        print("=" * 60)
        print("\nYou can now run the orchestrator.")
        print("The browser will automatically use this saved session.")
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Gmail login setup failed")
        print("=" * 60)
        print("\nPlease check:")
        print("1. Your credentials in .env file")
        print("2. If 2FA is enabled, use App Password instead")
        print("   Generate at: https://myaccount.google.com/apppasswords")
        print("3. Your internet connection")
        print("4. Google account status")
