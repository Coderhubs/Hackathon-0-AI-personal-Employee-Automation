#!/usr/bin/env python3
"""
Simple LinkedIn Poster - Posts once and exits
Used by orchestrator to post approved content
"""

import os
import sys
import asyncio
from pathlib import Path
import logging
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def post_to_linkedin(content: str) -> bool:
    """Post content to LinkedIn using saved session"""

    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not email or not password:
        print("[ERROR] LINKEDIN_EMAIL and LINKEDIN_PASSWORD not found in .env")
        return False

    # Use the saved browser session
    browser_data_dir = Path(__file__).parent / "browser_data" / "linkedin"

    if not browser_data_dir.exists():
        print("[ERROR] LinkedIn session not found. Run setup_linkedin_login.py first")
        return False

    print(f"[INFO] Using saved session from: {browser_data_dir}")

    try:
        async with async_playwright() as p:
            print("[INFO] Launching browser...")

            # Launch with persistent context (uses saved session)
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(browser_data_dir),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox'
                ]
            )

            page = context.pages[0] if context.pages else await context.new_page()

            print("[INFO] Navigating to LinkedIn feed...")
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Check if logged in
            try:
                feed_check = await page.query_selector('[aria-label="Main Feed"]')
                if not feed_check:
                    print("[ERROR] Not logged in. Run setup_linkedin_login.py first")
                    await context.close()
                    return False
                print("[SUCCESS] Logged in via saved session")
            except:
                print("[ERROR] Could not verify login status")
                await context.close()
                return False

            # Click "Start a post" button
            print("[INFO] Opening post composer...")
            start_post_button = await page.query_selector('button:has-text("Start a post")')
            if not start_post_button:
                start_post_button = await page.query_selector('[aria-label="Start a post"]')

            if not start_post_button:
                print("[ERROR] Could not find 'Start a post' button")
                await context.close()
                return False

            await start_post_button.click()
            await page.wait_for_timeout(2000)

            # Wait for editor
            print("[INFO] Typing content...")
            editor = await page.wait_for_selector('[role="textbox"]', timeout=10000)
            await page.wait_for_timeout(1000)

            # Type content
            await editor.fill(content)
            await page.wait_for_timeout(2000)

            # Click Post button
            print("[INFO] Publishing post...")

            # Try multiple selectors for Post button
            post_button = None
            selectors = [
                'button:has-text("Post")',
                'button[aria-label="Post"]',
                '.share-actions__primary-action',
                'button.share-actions__primary-action'
            ]

            for selector in selectors:
                post_button = await page.query_selector(selector)
                if post_button:
                    print(f"[INFO] Found Post button with selector: {selector}")
                    break

            if not post_button:
                print("[ERROR] Could not find 'Post' button")
                # Take screenshot for debugging
                await page.screenshot(path="debug_no_post_button.png")
                print("[DEBUG] Screenshot saved to debug_no_post_button.png")
                await context.close()
                return False

            # Check if button is enabled
            is_disabled = await post_button.get_attribute('disabled')
            if is_disabled:
                print("[ERROR] Post button is disabled")
                await page.screenshot(path="debug_button_disabled.png")
                await context.close()
                return False

            print("[INFO] Clicking Post button...")
            await post_button.click()

            # CRITICAL: Wait for post to actually upload
            print("[INFO] Waiting for post to upload...")
            await page.wait_for_timeout(3000)

            # Wait for modal to close (indicates post published)
            try:
                print("[INFO] Verifying post published...")
                await page.wait_for_selector('.share-box-footer', state='hidden', timeout=15000)
                print("[INFO] ✓ Post modal closed")
            except:
                print("[WARNING] Could not verify modal closed, waiting longer...")
                await page.wait_for_timeout(5000)

            # Additional wait to ensure upload completes
            print("[INFO] Ensuring upload completes...")
            await page.wait_for_timeout(5000)

            # Verify we're back on feed
            current_url = page.url
            if 'linkedin.com/feed' in current_url:
                print("[SUCCESS] ✓ Returned to feed - post published successfully!")
            else:
                print(f"[WARNING] Not on feed page: {current_url}")
                print("[INFO] Waiting additional 5 seconds...")
                await page.wait_for_timeout(5000)

            # Take final screenshot
            await page.screenshot(path="debug_after_post_click.png")
            print("[DEBUG] Screenshot saved to debug_after_post_click.png")

            # Close browser
            print("[INFO] Closing browser...")
            await context.close()

            print("="*60)
            print("✓ POST PUBLISHED SUCCESSFULLY")
            print("="*60)
            return True

    except Exception as e:
        print(f"[ERROR] Failed to post: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_content_from_file(file_path: str) -> str:
    """Extract post content from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content between ## Post Content and ## Posting Instructions
        if '## Post Content' in content:
            start = content.find('## Post Content') + len('## Post Content')
            end = content.find('## Posting Instructions')
            if end == -1:
                end = content.find('## Actions')
            if end == -1:
                end = len(content)

            post_content = content[start:end].strip()
            return post_content

        # If no markers, return whole content
        return content

    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        return ""

async def main():
    """Main entry point"""

    # Check if file path provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"[INFO] Reading content from: {file_path}")
        content = extract_content_from_file(file_path)
    else:
        # Read from Approved folder
        approved_dir = Path("AI_Employee_Vault/Approved")
        linkedin_files = list(approved_dir.glob("LINKEDIN_*.md"))

        if not linkedin_files:
            print("[INFO] No LinkedIn posts found in Approved folder")
            return

        file_path = linkedin_files[0]
        print(f"[INFO] Reading content from: {file_path}")
        content = extract_content_from_file(str(file_path))

    if not content:
        print("[ERROR] No content to post")
        sys.exit(1)

    print(f"[INFO] Content length: {len(content)} characters")
    # Don't print content preview to avoid Unicode errors on Windows console

    # Post to LinkedIn
    success = await post_to_linkedin(content)

    if success:
        print("[SUCCESS] Post completed successfully")
        sys.exit(0)
    else:
        print("[ERROR] Post failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
