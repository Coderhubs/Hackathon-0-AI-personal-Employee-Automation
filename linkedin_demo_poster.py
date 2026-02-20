#!/usr/bin/env python3
"""
LinkedIn Poster - Hackathon Demo Version
Uses your existing Chrome session (no verification needed)
"""

import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('LinkedInDemo')

async def post_to_linkedin_demo(content: str, image_path: Path = None):
    """
    Post to LinkedIn using existing Chrome session.
    No verification needed - just login to LinkedIn in Chrome first.
    """

    logger.info("="*80)
    logger.info("LinkedIn Demo Poster - Starting")
    logger.info("="*80)

    try:
        async with async_playwright() as p:
            # Connect to existing Chrome (no profile, no verification)
            logger.info("Launching browser...")
            browser = await p.chromium.launch(
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )

            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )

            page = await context.new_page()

            # Navigate to LinkedIn
            logger.info("Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/feed/")
            await page.wait_for_timeout(3000)

            # Check if logged in
            current_url = page.url
            if "login" in current_url or "checkpoint" in current_url:
                logger.error("Not logged in! Please login to LinkedIn in Chrome first.")
                logger.error("Then run this script again.")
                await browser.close()
                return False

            logger.info("[OK] Logged in")

            # Open post composer
            logger.info("Opening post composer...")
            start_button = await page.wait_for_selector('button:has-text("Start a post")', timeout=10000)
            await start_button.click()
            await page.wait_for_timeout(2000)

            # Enter content
            logger.info("Entering content...")
            editor = await page.wait_for_selector('[role="textbox"]', timeout=10000)
            await editor.click()
            await page.wait_for_timeout(500)
            await editor.type(content, delay=50)
            await page.wait_for_timeout(2000)

            # Upload image if provided
            if image_path and image_path.exists():
                logger.info("Uploading image...")
                file_input = await page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(str(image_path))
                    await page.wait_for_timeout(3000)

            # Click Post button
            logger.info("Clicking Post button...")
            post_button = await page.wait_for_selector('button:has-text("Post")', timeout=10000)
            await post_button.click()
            await page.wait_for_timeout(5000)

            # Take screenshot
            await page.screenshot(path="linkedin_demo_success.png")
            logger.info("Screenshot saved: linkedin_demo_success.png")

            await browser.close()

            logger.info("="*80)
            logger.info("[SUCCESS] Post published!")
            logger.info("="*80)
            return True

    except Exception as e:
        logger.error(f"Error: {e}")
        return False


async def main():
    # Read approved post
    vault_dir = Path(__file__).parent / "AI_Employee_Vault"
    approved_dir = vault_dir / "Approved"

    linkedin_files = list(approved_dir.glob("LINKEDIN_*.md"))

    if not linkedin_files:
        print("No approved posts found!")
        return

    # Read first approved post
    post_file = linkedin_files[0]
    print(f"Posting: {post_file.name}")

    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract content between ## Post Content and ## Posting Instructions
    start = content.find("## Post Content")
    end = content.find("## Posting Instructions")

    if start != -1 and end != -1:
        post_content = content[start:end].replace("## Post Content", "").strip()
    else:
        print("Could not extract post content!")
        return

    # Find image
    images_dir = vault_dir / "Generated_Images"
    image_files = list(images_dir.glob("linkedin_post_*.png"))
    image_path = image_files[-1] if image_files else None

    # Post to LinkedIn
    success = await post_to_linkedin_demo(post_content, image_path)

    if success:
        # Move to Done
        done_dir = vault_dir / "Done"
        done_dir.mkdir(exist_ok=True)
        post_file.rename(done_dir / post_file.name)
        print(f"\n[OK] Post moved to Done folder")


if __name__ == "__main__":
    print("="*80)
    print("LinkedIn Hackathon Demo Poster")
    print("="*80)
    print()
    print("IMPORTANT: Login to LinkedIn in Chrome FIRST, then run this script")
    print()
    print("="*80)
    print()

    asyncio.run(main())
