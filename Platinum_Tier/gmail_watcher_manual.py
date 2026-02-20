"""
Gmail Watcher - Manual Login Version (Windows Compatible)
Run this to establish browser session first
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio

# Load environment
load_dotenv()
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', 'your_gmail_email@gmail.com')
VAULT_PATH = Path("AI_Employee_Vault")

async def setup_gmail_session():
    """Setup Gmail session with manual login"""
    user_data_dir = Path("Platinum_Tier/browser_data/gmail")
    user_data_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("GMAIL WATCHER - MANUAL LOGIN SETUP")
    print("=" * 60)
    print()
    print("This will open Gmail in a browser window.")
    print("Please log in manually with your credentials:")
    print(f"Email: {GMAIL_EMAIL}")
    print()
    print("After logging in successfully:")
    print("1. Wait for your inbox to load completely")
    print("2. Press Enter in this terminal to continue")
    print()
    print("=" * 60)

    p = await async_playwright().start()
    context = await p.chromium.launch_persistent_context(
        user_data_dir=str(user_data_dir),
        headless=False,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage'
        ],
        viewport={'width': 1280, 'height': 720}
    )

    page = context.pages[0] if context.pages else await context.new_page()

    # Navigate to Gmail
    print("Opening Gmail...")
    await page.goto("https://mail.google.com/", wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)

    # Check if login needed
    if await page.query_selector('input[type="email"]'):
        print()
        print("[OK] Login page detected")
        print("[OK] Please complete login in the browser window")
        print()
    else:
        print()
        print("[OK] Already logged in!")
        print()

    # Wait for user confirmation
    input("Press Enter after you've logged in and see your inbox...")

    # Verify login
    try:
        await page.goto("https://mail.google.com/mail/u/0/#inbox", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Check for inbox
        if await page.query_selector('[role="main"]'):
            print()
            print("=" * 60)
            print("[SUCCESS] Gmail session established")
            print("=" * 60)
            print()
            print("Your browser session has been saved.")
            print("The watcher will now use this session automatically.")
            print()
            print("You can now run: python gmail_watcher_hackathon.py")
            print()
        else:
            print()
            print("[WARNING] Inbox not detected. Please try again.")
            print()
    except Exception as e:
        print(f"[ERROR] {e}")

    await page.wait_for_timeout(2000)
    await context.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(setup_gmail_session())
