#!/usr/bin/env python3
"""
LinkedIn Poster - Hackathon Demo (Fully Automated)
Opens browser, waits for you to login, then posts automatically
"""

import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('LinkedInDemo')

async def post_to_linkedin_hackathon():
    """
    Fully automated LinkedIn posting for hackathon demo.
    Opens browser, waits for login, then posts.
    """

    logger.info("="*80)
    logger.info("LinkedIn Hackathon Demo - Automated Posting")
    logger.info("="*80)
    logger.info("")

    # Read approved post
    vault_dir = Path(__file__).parent / "AI_Employee_Vault"
    approved_dir = vault_dir / "Approved"
    linkedin_files = list(approved_dir.glob("LINKEDIN_*.md"))

    if not linkedin_files:
        logger.error("No approved posts found!")
        return False

    post_file = linkedin_files[0]
    logger.info(f"Post to publish: {post_file.name}")

    # Read content
    with open(post_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract post content
    start = content.find("## Post Content")
    end = content.find("## Posting Instructions")

    if start != -1 and end != -1:
        post_content = content[start:end].replace("## Post Content", "").strip()
    else:
        logger.error("Could not extract post content!")
        return False

    logger.info(f"Content length: {len(post_content)} characters")

    # Find image
    images_dir = vault_dir / "Generated_Images"
    image_files = list(images_dir.glob("linkedin_post_*.png"))
    image_path = image_files[-1] if image_files else None

    if image_path:
        logger.info(f"Image: {image_path.name}")

    logger.info("")
    logger.info("="*80)
    logger.info("STEP 1: Opening browser...")
    logger.info("="*80)

    try:
        async with async_playwright() as p:
            # Launch browser
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
            await page.goto("https://www.linkedin.com/login")
            await page.wait_for_timeout(2000)

            logger.info("")
            logger.info("="*80)
            logger.info("STEP 2: LOGIN TO LINKEDIN NOW!")
            logger.info("="*80)
            logger.info("")
            logger.info("You have 60 seconds to:")
            logger.info("  1. Enter your email and password")
            logger.info("  2. Complete any verification")
            logger.info("  3. Wait until you see your LinkedIn feed")
            logger.info("")
            logger.info("Waiting 60 seconds...")
            logger.info("")

            # Wait 60 seconds for login
            for i in range(60, 0, -5):
                logger.info(f"[{i}s remaining] Complete login in browser...")
                await page.wait_for_timeout(5000)

            # Check if logged in
            current_url = page.url
            logger.info("")
            logger.info(f"Current URL: {current_url}")

            if "feed" not in current_url:
                logger.info("Navigating to feed...")
                await page.goto("https://www.linkedin.com/feed/")
                await page.wait_for_timeout(3000)

            current_url = page.url
            if "login" in current_url or "checkpoint" in current_url:
                logger.error("")
                logger.error("Still not logged in. Waiting additional 30 seconds...")
                logger.error("")

                for i in range(30, 0, -5):
                    logger.info(f"[{i}s remaining] Complete login...")
                    await page.wait_for_timeout(5000)

            logger.info("")
            logger.info("="*80)
            logger.info("STEP 3: Posting to LinkedIn...")
            logger.info("="*80)
            logger.info("")

            # Open post composer
            logger.info("Opening post composer...")
            try:
                start_button = await page.wait_for_selector('button:has-text("Start a post")', timeout=10000, state='visible')
                await start_button.click()
                await page.wait_for_timeout(2000)
                logger.info("[OK] Composer opened")
            except Exception as e:
                logger.error(f"Could not open composer: {e}")
                await page.screenshot(path="error_composer.png")
                await browser.close()
                return False

            # Enter content
            logger.info("Entering content...")
            try:
                editor = await page.wait_for_selector('[role="textbox"]', timeout=10000, state='visible')
                await editor.click()
                await page.wait_for_timeout(500)
                await editor.type(post_content, delay=50)
                await page.wait_for_timeout(2000)
                logger.info("[OK] Content entered")
            except Exception as e:
                logger.error(f"Could not enter content: {e}")
                await page.screenshot(path="error_content.png")
                await browser.close()
                return False

            # Upload image
            if image_path and image_path.exists():
                logger.info("Uploading image...")
                try:
                    file_input = await page.query_selector('input[type="file"]')
                    if file_input:
                        await file_input.set_input_files(str(image_path))
                        await page.wait_for_timeout(3000)
                        logger.info("[OK] Image uploaded")
                except Exception as e:
                    logger.warning(f"Image upload failed: {e}")

            # Click Post button
            logger.info("Clicking Post button...")
            try:
                post_button = await page.wait_for_selector('button:has-text("Post")', timeout=10000, state='visible')

                # Check if enabled
                is_disabled = await post_button.get_attribute('disabled')
                if is_disabled:
                    logger.error("Post button is disabled!")
                    await page.screenshot(path="error_button_disabled.png")
                    await browser.close()
                    return False

                await post_button.click()
                await page.wait_for_timeout(5000)
                logger.info("[OK] Post button clicked")
            except Exception as e:
                logger.error(f"Could not click Post button: {e}")
                await page.screenshot(path="error_post_button.png")
                await browser.close()
                return False

            # Wait for post to publish
            logger.info("Waiting for post to publish...")
            await page.wait_for_timeout(5000)

            # Take screenshot
            await page.screenshot(path="linkedin_hackathon_success.png")
            logger.info("[OK] Screenshot saved: linkedin_hackathon_success.png")

            # Close browser
            await browser.close()

            logger.info("")
            logger.info("="*80)
            logger.info("[SUCCESS] POST PUBLISHED TO LINKEDIN!")
            logger.info("="*80)
            logger.info("")

            # Move to Done
            done_dir = vault_dir / "Done"
            done_dir.mkdir(exist_ok=True)
            post_file.rename(done_dir / post_file.name)
            logger.info(f"[OK] Post moved to Done folder")

            return True

    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print()
    print("="*80)
    print("LinkedIn Hackathon Demo - Automated Posting")
    print("="*80)
    print()
    print("This script will:")
    print("  1. Open browser")
    print("  2. Wait for you to login (60 seconds)")
    print("  3. Post automatically")
    print()
    print("="*80)
    print()

    success = asyncio.run(post_to_linkedin_hackathon())

    if success:
        print()
        print("="*80)
        print("HACKATHON DEMO COMPLETE!")
        print("="*80)
        print()
        print("Your LinkedIn post is now live!")
        print("Screenshot saved: linkedin_hackathon_success.png")
        print()
    else:
        print()
        print("="*80)
        print("POSTING FAILED")
        print("="*80)
        print()
        print("Check error messages above")
        print()
