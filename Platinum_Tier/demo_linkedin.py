"""
Demo script - runs LinkedIn watcher once and exits
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime

async def demo_linkedin():
    """Demo LinkedIn watcher - runs once"""
    # Load credentials
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    print("=" * 60)
    print("LinkedIn Watcher Demo - Single Run")
    print("=" * 60)
    print(f"\nLogging in as: {email}")
    print("Browser will open in 3 seconds...\n")
    await asyncio.sleep(3)

    async with async_playwright() as p:
        # Launch browser (visible so you can see what's happening)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()

        try:
            # Navigate to LinkedIn
            print("[1/4] Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/login", wait_until="networkidle")

            # Enter credentials
            print("[2/4] Entering credentials...")
            await page.fill('input[name="session_key"]', email)
            await page.fill('input[name="session_password"]', password)

            # Click sign in
            print("[3/4] Signing in...")
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)

            # Check for verification
            if await page.query_selector('input[name="pin"]'):
                print("\n[!] LinkedIn requires verification code!")
                print("    Please check your email/phone and enter the code in the browser.")
                print("    Waiting 60 seconds for manual verification...")
                await page.wait_for_timeout(60000)

            # Wait for feed
            print("[4/4] Loading feed...")
            await page.wait_for_selector('[role="main"]', timeout=30000)
            print("\n[SUCCESS] Logged into LinkedIn!")

            # Navigate to feed
            await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
            await page.wait_for_timeout(3000)

            # Scroll to load posts
            print("\nChecking for posts...")
            await page.evaluate("window.scrollTo(0, 1000)")
            await page.wait_for_timeout(2000)

            # Get posts
            posts = await page.query_selector_all('[data-id^="urn:li:activity"]')
            print(f"Found {len(posts)} posts in feed")

            # Parse first few posts
            if posts:
                print("\nSample posts:")
                for i, post in enumerate(posts[:3], 1):
                    try:
                        author_elem = await post.query_selector('.update-components-actor__name')
                        author = await author_elem.inner_text() if author_elem else "Unknown"
                        print(f"  {i}. {author.strip()}")
                    except:
                        pass

            print("\n" + "=" * 60)
            print("Demo complete! Browser will close in 5 seconds...")
            print("=" * 60)
            await page.wait_for_timeout(5000)

        except Exception as e:
            print(f"\n[ERROR] {e}")
            print("\nBrowser will stay open for 10 seconds so you can see the error...")
            await page.wait_for_timeout(10000)

        finally:
            await browser.close()
            print("\nTo run the full watcher: python linkedin_watcher_playwright.py")

if __name__ == "__main__":
    asyncio.run(demo_linkedin())
