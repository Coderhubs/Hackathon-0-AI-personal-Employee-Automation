#!/usr/bin/env python3
"""
Automatic LinkedIn Login - No Input Required
Opens browser, waits 60 seconds for you to login, then saves session
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def auto_linkedin_login():
    """
    Opens LinkedIn in browser for manual login.
    Waits 60 seconds for you to complete login.
    Session is saved automatically.
    """

    print("="*80)
    print("LinkedIn Automatic Login")
    print("="*80)
    print()
    print("Opening browser in 3 seconds...")
    print("You will have 60 seconds to:")
    print("  1. Login to LinkedIn")
    print("  2. Complete any verification")
    print("  3. Wait until you see your feed")
    print()
    print("="*80)
    print()

    await asyncio.sleep(3)

    user_data_dir = Path(__file__).parent / "browser_data" / "linkedin"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    print("[INFO] Opening browser...")
    print("[INFO] Browser data will be saved to:", user_data_dir)
    print()

    async with async_playwright() as p:
        # Launch browser with persistent session
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ],
            viewport={'width': 1280, 'height': 720}
        )

        page = context.pages[0] if context.pages else await context.new_page()

        # Navigate to LinkedIn
        print("[INFO] Navigating to LinkedIn...")
        await page.goto("https://www.linkedin.com/login")
        await page.wait_for_timeout(2000)

        print()
        print("="*80)
        print("COMPLETE LOGIN IN THE BROWSER NOW!")
        print("="*80)
        print()
        print("You have 60 seconds to:")
        print("  1. Enter your email and password")
        print("  2. Complete any verification (email code, SMS, CAPTCHA)")
        print("  3. Wait until you see your LinkedIn FEED")
        print()
        print("Waiting 60 seconds...")
        print()

        # Wait 60 seconds for user to login
        for i in range(60, 0, -5):
            print(f"[{i}s remaining] Complete login in browser...")
            await page.wait_for_timeout(5000)

        # Verify login
        print()
        print("[INFO] Verifying login...")
        current_url = page.url

        if "linkedin.com/feed" in current_url:
            print()
            print("="*80)
            print("[SUCCESS] You are logged in!")
            print("[SUCCESS] Session saved successfully!")
            print("="*80)
            print()
        elif "checkpoint" in current_url or "challenge" in current_url:
            print()
            print("="*80)
            print("[WARNING] Still on verification page")
            print("[INFO] Waiting additional 30 seconds...")
            print("="*80)
            print()

            for i in range(30, 0, -5):
                print(f"[{i}s remaining] Complete verification...")
                await page.wait_for_timeout(5000)

            current_url = page.url
            if "linkedin.com/feed" in current_url:
                print()
                print("[SUCCESS] Login completed!")
                print()
        else:
            print()
            print(f"[WARNING] Current URL: {current_url}")
            print("[INFO] Session should still be saved")
            print()

        print("="*80)
        print("Closing browser in 5 seconds...")
        print("="*80)
        await page.wait_for_timeout(5000)

        await context.close()

        print()
        print("[DONE] Session saved!")
        print()
        print("Next: Run 'python linkedin_scheduler_complete.py post-now'")
        print()


if __name__ == "__main__":
    asyncio.run(auto_linkedin_login())
