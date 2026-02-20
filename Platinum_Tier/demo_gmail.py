"""
Demo script - runs Gmail watcher once and exits
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime

async def demo_gmail():
    """Demo Gmail watcher - runs once"""
    # Load credentials
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')

    print("=" * 60)
    print("Gmail Watcher Demo - Single Run")
    print("=" * 60)
    print(f"\nLogging in as: {email}")
    print("Browser will open in 3 seconds...\n")
    await asyncio.sleep(3)

    async with async_playwright() as p:
        # Launch browser (visible so you can see what's happening)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to Gmail
            print("[1/4] Navigating to Gmail...")
            await page.goto("https://mail.google.com/", wait_until="networkidle")

            # Enter email
            print("[2/4] Entering email...")
            await page.fill('input[type="email"]', email)
            await page.click('button:has-text("Next")')
            await page.wait_for_timeout(3000)

            # Enter password
            print("[3/4] Entering password...")
            try:
                await page.fill('input[type="password"]', password, timeout=10000)
                await page.click('button:has-text("Next")')
                await page.wait_for_timeout(5000)
            except Exception as e:
                print(f"    Note: {e}")
                print("    Gmail might require manual verification...")

            # Wait for inbox
            print("[4/4] Loading inbox...")
            try:
                await page.wait_for_selector('[role="main"]', timeout=30000)
                print("\n[SUCCESS] Logged into Gmail!")

                # Get email rows
                print("\nChecking for emails...")
                await page.wait_for_timeout(2000)
                email_rows = await page.query_selector_all('tr.zA')
                print(f"Found {len(email_rows)} emails in inbox")

                # Parse first few emails
                if email_rows:
                    print("\nSample emails:")
                    for i, row in enumerate(email_rows[:3], 1):
                        try:
                            sender_elem = await row.query_selector('.yW span')
                            subject_elem = await row.query_selector('.y6 span')
                            sender = await sender_elem.inner_text() if sender_elem else "Unknown"
                            subject = await subject_elem.inner_text() if subject_elem else "No Subject"
                            print(f"  {i}. From: {sender.strip()[:30]} | Subject: {subject.strip()[:40]}")
                        except:
                            pass

                print("\n" + "=" * 60)
                print("Demo complete! Browser will close in 5 seconds...")
                print("=" * 60)
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"\n[ERROR] Could not load inbox: {e}")
                print("\nThis might be due to:")
                print("  1. 2FA enabled - you need an App Password")
                print("  2. Google security blocking automated login")
                print("  3. Manual verification required")
                print("\nBrowser will stay open for 15 seconds...")
                await page.wait_for_timeout(15000)

        except Exception as e:
            print(f"\n[ERROR] {e}")
            print("\nBrowser will stay open for 15 seconds so you can see the error...")
            await page.wait_for_timeout(15000)

        finally:
            await browser.close()
            print("\nTo run the full watcher: python gmail_watcher_playwright.py")

if __name__ == "__main__":
    asyncio.run(demo_gmail())
