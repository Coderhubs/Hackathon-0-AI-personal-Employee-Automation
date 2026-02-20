#!/usr/bin/env python3
"""
LinkedIn Hackathon Demo - Fully Automated
Waits 90 seconds for login, then posts automatically
"""

import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('LinkedInDemo')

async def post_to_linkedin_auto():
    """
    Fully automated LinkedIn posting for hackathon demo.
    Opens browser, waits 90 seconds for login, then posts automatically.
    """

    logger.info("="*80)
    logger.info("LinkedIn Hackathon Demo - Fully Automated")
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

    logger.info(f"Content: {post_content[:50]}...")
    logger.info(f"Length: {len(post_content)} characters")

    # Find image
    images_dir = vault_dir / "Generated_Images"
    image_files = list(images_dir.glob("linkedin_post_*.png"))
    image_path = image_files[-1] if image_files else None

    if image_path:
        logger.info(f"Image: {image_path.name}")

    logger.info("")
    logger.info("="*80)
    logger.info("Opening browser in 3 seconds...")
    logger.info("="*80)
    await asyncio.sleep(3)

    try:
        async with async_playwright() as p:
            # Launch browser
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
            await page.goto("https://www.linkedin.com/login")
            await page.wait_for_timeout(2000)

            logger.info("")
            logger.info("="*80)
            logger.info("LOGIN TO LINKEDIN NOW!")
            logger.info("="*80)
            logger.info("")
            logger.info("You have 90 seconds to:")
            logger.info("  1. Enter your email and password")
            logger.info("  2. Complete any verification")
            logger.info("  3. Wait until you see your LinkedIn feed")
            logger.info("")
            logger.info("Script will automatically post after 90 seconds")
            logger.info("")

            # Wait 90 seconds for login
            for i in range(90, 0, -10):
                logger.info(f"[{i}s remaining] Complete login in browser...")
                await page.wait_for_timeout(10000)

            logger.info("")
            logger.info("="*80)
            logger.info("Starting automated posting...")
            logger.info("="*80)
            logger.info("")

            # Navigate to feed
            logger.info("Step 1: Navigating to feed...")
            await page.goto("https://www.linkedin.com/feed/")
            await page.wait_for_timeout(3000)

            current_url = page.url
            logger.info(f"Current URL: {current_url}")

            if "login" in current_url or "checkpoint" in current_url:
                logger.error("Not logged in! Please login and run script again.")
                await page.screenshot(path="error_not_logged_in.png")
                await browser.close()
                return False

            # Open post composer
            logger.info("Step 2: Opening post composer...")
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
            logger.info("Step 3: Entering content...")
            try:
                editor = await page.wait_for_selector('[role="textbox"]', timeout=10000, state='visible')
                await editor.click()
                await page.wait_for_timeout(500)

                # Type with human-like delay
                logger.info("Typing content (human-like speed)...")
                await editor.type(post_content, delay=50)
                await page.wait_for_timeout(2000)

                # Verify content entered
                editor_text = await editor.inner_text()
                logger.info(f"[OK] Content entered ({len(editor_text)} characters)")
            except Exception as e:
                logger.error(f"Could not enter content: {e}")
                await page.screenshot(path="error_content.png")
                await browser.close()
                return False

            # Upload image
            if image_path and image_path.exists():
                logger.info("Step 4: Uploading image...")
                try:
                    file_input = await page.query_selector('input[type="file"]')
                    if file_input:
                        await file_input.set_input_files(str(image_path))
                        await page.wait_for_timeout(3000)
                        logger.info("[OK] Image uploaded")
                    else:
                        logger.warning("Could not find image upload input")
                except Exception as e:
                    logger.warning(f"Image upload failed: {e}")

            # Click Post button
            logger.info("Step 5: Publishing post...")
            try:
                post_button = await page.wait_for_selector('button:has-text("Post")', timeout=10000, state='visible')

                # Check if enabled
                is_disabled = await post_button.get_attribute('disabled')
                aria_disabled = await post_button.get_attribute('aria-disabled')

                if is_disabled or aria_disabled == 'true':
                    logger.error("Post button is disabled!")
                    await page.screenshot(path="error_button_disabled.png")
                    await browser.close()
                    return False

                logger.info("Clicking Post button...")
                await post_button.click()
                await page.wait_for_timeout(5000)
                logger.info("[OK] Post button clicked")
            except Exception as e:
                logger.error(f"Could not click Post button: {e}")
                await page.screenshot(path="error_post_button.png")
                await browser.close()
                return False

            # Wait for post to publish
            logger.info("Step 6: Waiting for post to publish...")
            await page.wait_for_timeout(5000)

            # Take screenshot
            await page.screenshot(path="linkedin_hackathon_success.png")
            logger.info("[OK] Screenshot saved: linkedin_hackathon_success.png")

            # Close browser
            logger.info("Closing browser in 3 seconds...")
            await page.wait_for_timeout(3000)
            await browser.close()

            logger.info("")
            logger.info("="*80)
            logger.info("SUCCESS! POST PUBLISHED TO LINKEDIN!")
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
    print("LinkedIn Hackathon Demo - Fully Automated")
    print("="*80)
    print()
    print("This script will:")
    print("  1. Open browser")
    print("  2. Wait 90 seconds for you to login")
    print("  3. Post automatically")
    print()
    print("="*80)
    print()

    success = asyncio.run(post_to_linkedin_auto())

    if success:
        print()
        print("="*80)
        print("HACKATHON DEMO COMPLETE!")
        print("="*80)
        print()
        print("Your LinkedIn post is now live!")
        print("Screenshot: linkedin_hackathon_success.png")
        print()
    else:
        print()
        print("="*80)
        print("POSTING FAILED")
        print("="*80)
        print()
        print("Check error messages above")
        print()
