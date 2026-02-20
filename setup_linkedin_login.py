#!/usr/bin/env python3
"""
LinkedIn Login Setup - One-time login to save session
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def setup_linkedin_login():
    """Setup LinkedIn login and save persistent session"""

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("[ERROR] LINKEDIN_EMAIL and LINKEDIN_PASSWORD not found in .env file")
        return False

    print("=" * 60)
    print("LinkedIn Login Setup")
    print("=" * 60)
    print(f"Email: {email}")
    print("=" * 60)

    # Create browser data directory
    browser_data_dir = Path(__file__).parent / "browser_data" / "linkedin"
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

            print("[INFO] Navigating to LinkedIn login page...")
            page.goto('https://www.linkedin.com/login', wait_until='networkidle')

            # Check if already logged in
            if 'feed' in page.url or 'mynetwork' in page.url:
                print("\n[SUCCESS] Already logged in! Session is saved.")
                browser.close()
                return True

            print("[INFO] Filling in credentials...")

            # Fill in email
            page.fill('input[name="session_key"]', email)
            time.sleep(1)

            # Fill in password
            page.fill('input[name="session_password"]', password)
            time.sleep(1)

            print("[INFO] Clicking login button...")
            page.click('button[type="submit"]')

            # Wait for navigation
            print("[INFO] Waiting for login to complete...")
            time.sleep(5)

            # Check if login successful
            current_url = page.url

            if 'feed' in current_url or 'mynetwork' in current_url:
                print("\n[SUCCESS] Login successful! Session saved.")
                print(f"Current URL: {current_url}")

                # Keep browser open for 10 seconds so you can see it worked
                print("\n[INFO] Keeping browser open for 10 seconds...")
                time.sleep(10)

                browser.close()
                return True

            elif 'checkpoint' in current_url or 'challenge' in current_url:
                print("\n[WARNING] LinkedIn security challenge detected!")
                print("Please complete the challenge in the browser window.")
                print("The browser will stay open for 2 minutes.")
                print("After completing the challenge, the session will be saved.")

                # Wait 2 minutes for user to complete challenge
                time.sleep(120)

                # Check again
                if 'feed' in page.url or 'mynetwork' in page.url:
                    print("\n[SUCCESS] Challenge completed! Session saved.")
                    browser.close()
                    return True
                else:
                    print("\n[ERROR] Challenge not completed. Please try again.")
                    browser.close()
                    return False

            else:
                print(f"\n[ERROR] Login failed. Current URL: {current_url}")
                print("Please check your credentials in .env file")

                # Keep browser open so you can see what happened
                print("\n[INFO] Keeping browser open for 30 seconds...")
                time.sleep(30)

                browser.close()
                return False

    except Exception as e:
        print(f"\n[ERROR] Error during login: {e}")
        return False

if __name__ == "__main__":
    print("\n[START] Starting LinkedIn login setup...\n")

    success = setup_linkedin_login()

    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] LinkedIn login setup complete!")
        print("=" * 60)
        print("\nYou can now run the orchestrator.")
        print("The browser will automatically use this saved session.")
    else:
        print("\n" + "=" * 60)
        print("[ERROR] LinkedIn login setup failed")
        print("=" * 60)
        print("\nPlease check:")
        print("1. Your credentials in .env file")
        print("2. Your internet connection")
        print("3. LinkedIn account status")
