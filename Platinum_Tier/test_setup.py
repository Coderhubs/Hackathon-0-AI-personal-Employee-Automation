"""
Quick test script to verify Playwright setup and credentials
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright

async def test_setup():
    """Test Playwright and credentials"""
    print("=" * 60)
    print("Playwright Setup Test")
    print("=" * 60)

    # Load environment variables
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

    # Check credentials
    print("\n1. Checking credentials...")
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    gmail_email = os.getenv('GMAIL_EMAIL')

    if linkedin_email and gmail_email:
        print(f"   [OK] LinkedIn: {linkedin_email}")
        print(f"   [OK] Gmail: {gmail_email}")
    else:
        print("   [ERROR] Credentials not found in .env file")
        return False

    # Test Playwright
    print("\n2. Testing Playwright browser...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://www.google.com")
            title = await page.title()
            await browser.close()
            print(f"   [OK] Playwright working! (Loaded: {title})")
    except Exception as e:
        print(f"   [ERROR] Playwright error: {e}")
        return False

    print("\n" + "=" * 60)
    print("[SUCCESS] All checks passed! Ready to run watchers.")
    print("=" * 60)
    print("\nTo run the watchers:")
    print("  Option 1: Run RUN_WATCHERS.bat")
    print("  Option 2: python linkedin_watcher_playwright.py")
    print("  Option 3: python gmail_watcher_playwright.py")
    print()
    return True

if __name__ == "__main__":
    asyncio.run(test_setup())
