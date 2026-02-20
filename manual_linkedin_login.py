#!/usr/bin/env python3
"""
Manual LinkedIn Login - Simple and Reliable
Just opens browser, you login manually, session is saved automatically
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

async def manual_linkedin_login():
    """
    Opens LinkedIn in browser for manual login.
    Session is saved automatically for future automation.
    """

    print("="*80)
    print("LinkedIn Manual Login")
    print("="*80)
    print()
    print("This will:")
    print("1. Open LinkedIn in a browser")
    print("2. You login manually (with any verification needed)")
    print("3. Session is saved automatically")
    print("4. Future posts will use this saved session")
    print()
    print("="*80)
    print()

    input("Press Enter to open browser...")

    user_data_dir = Path(__file__).parent / "browser_data" / "linkedin"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    print("\n[INFO] Opening browser...")
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
        print("INSTRUCTIONS:")
        print("="*80)
        print()
        print("1. Complete the login in the browser window")
        print("2. Enter your email and password")
        print("3. Complete any verification (email code, SMS, CAPTCHA)")
        print("4. Wait until you see your LinkedIn FEED")
        print("5. Once you see your feed, come back here")
        print()
        print("="*80)
        print()

        input("Press Enter AFTER you see your LinkedIn feed...")

        # Verify login
        print("\n[INFO] Verifying login...")
        current_url = page.url

        if "linkedin.com/feed" in current_url:
            print("[SUCCESS] ✓ You are logged in!")
            print("[SUCCESS] ✓ Session saved successfully!")
            print()
            print("You can now close this window.")
            print("Your automation will use this saved session.")
        else:
            print(f"[WARNING] Current URL: {current_url}")
            print("[WARNING] You might not be on the feed page yet.")
            print("[WARNING] But session should still be saved.")

        print()
        print("="*80)
        print("Next Steps:")
        print("="*80)
        print()
        print("1. Close this browser window")
        print("2. Run: python linkedin_scheduler_complete.py post-now")
        print("3. Your post will be published automatically!")
        print()

        input("Press Enter to close browser...")

        await context.close()

        print("\n[DONE] Session saved. You can now use automation!")


if __name__ == "__main__":
    asyncio.run(manual_linkedin_login())
