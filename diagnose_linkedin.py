"""
Diagnose LinkedIn posting issue - saves screenshots and logs
"""
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def diagnose_linkedin():
    """Diagnose what's happening with LinkedIn posts"""

    base_dir = Path(__file__).parent
    user_data_dir = base_dir / "browser_data" / "linkedin"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = base_dir / f"linkedin_diagnosis_{timestamp}.txt"

    def log(msg):
        print(msg)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    log("="*80)
    log("LinkedIn Posting Diagnosis")
    log("="*80)

    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()

        try:
            # Navigate to LinkedIn
            log("\n1. Navigating to LinkedIn...")
            await page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            await page.wait_for_timeout(3000)

            # Check login
            log(f"Current URL: {page.url}")
            if 'login' in page.url or 'authwall' in page.url:
                log("ERROR: Not logged in!")
                await page.screenshot(path=f"diagnosis_not_logged_in_{timestamp}.png")
                await browser.close()
                return

            log("OK - Logged in")
            await page.screenshot(path=f"diagnosis_step1_feed_{timestamp}.png")

            # Open composer
            log("\n2. Opening post composer...")
            start_post_selectors = [
                'button:has-text("Start a post")',
                'button[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger'
            ]

            start_post = None
            for selector in start_post_selectors:
                start_post = await page.query_selector(selector)
                if start_post:
                    log(f"Found start button with: {selector}")
                    break

            if not start_post:
                log("ERROR: Could not find 'Start a post' button")
                await page.screenshot(path=f"diagnosis_no_start_button_{timestamp}.png")
                await browser.close()
                return

            await start_post.click()
            await page.wait_for_timeout(2000)
            log("OK - Clicked start post")
            await page.screenshot(path=f"diagnosis_step2_composer_{timestamp}.png")

            # Find editor - try multiple selectors
            log("\n3. Looking for editor...")
            editor_selectors = [
                '.ql-editor',
                '[contenteditable="true"]',
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"]',
                '.share-creation-state__text-editor'
            ]

            editor = None
            for selector in editor_selectors:
                editor = await page.query_selector(selector)
                if editor:
                    log(f"Found editor with: {selector}")
                    break

            if not editor:
                log("ERROR: Could not find editor with any selector")
                log("Available elements:")
                # Get page HTML to see what's there
                html = await page.content()
                with open(f"diagnosis_page_html_{timestamp}.html", 'w', encoding='utf-8') as f:
                    f.write(html)
                log(f"Saved page HTML to diagnosis_page_html_{timestamp}.html")
                await page.screenshot(path=f"diagnosis_no_editor_{timestamp}.png")
                await browser.close()
                return

            # Type content
            log("\n4. Typing test content...")
            test_content = f"Test post {timestamp}\n\nDiagnosing LinkedIn posting issue."

            await editor.click()
            await page.wait_for_timeout(500)
            await editor.fill(test_content)
            await page.wait_for_timeout(1000)
            log(f"OK - Typed {len(test_content)} characters")
            await page.screenshot(path=f"diagnosis_step3_content_{timestamp}.png")

            # Find Post button
            log("\n5. Looking for Post button...")
            post_button_selectors = [
                'button:has-text("Post")',
                'button[aria-label="Post"]',
                '.share-actions__primary-action',
                'button.share-actions__primary-action'
            ]

            post_button = None
            for selector in post_button_selectors:
                post_button = await page.query_selector(selector)
                if post_button:
                    log(f"Found Post button with: {selector}")
                    break

            if not post_button:
                log("ERROR: Could not find Post button")
                await page.screenshot(path=f"diagnosis_no_post_button_{timestamp}.png")
                await browser.close()
                return

            # Check if enabled
            is_disabled = await post_button.get_attribute('disabled')
            log(f"Post button disabled: {is_disabled}")

            if is_disabled:
                log("ERROR: Post button is disabled!")
                await page.screenshot(path=f"diagnosis_button_disabled_{timestamp}.png")
                await browser.close()
                return

            log("OK - Post button is enabled")
            await page.screenshot(path=f"diagnosis_step4_ready_{timestamp}.png")

            # Click Post
            log("\n6. Clicking Post button...")
            await post_button.click()
            log("OK - Clicked Post button")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"diagnosis_step5_after_click_{timestamp}.png")

            # Wait and check
            log("\n7. Waiting 5 seconds...")
            await page.wait_for_timeout(5000)
            await page.screenshot(path=f"diagnosis_step6_after_5sec_{timestamp}.png")

            log(f"Current URL: {page.url}")

            # Check if modal closed
            modal = await page.query_selector('.share-box-footer')
            if modal:
                is_visible = await modal.is_visible()
                log(f"Modal still visible: {is_visible}")
            else:
                log("Modal not found (might have closed)")

            # Wait more
            log("\n8. Waiting additional 10 seconds...")
            await page.wait_for_timeout(10000)
            await page.screenshot(path=f"diagnosis_step7_after_15sec_{timestamp}.png")

            # Go to feed and check
            log("\n9. Navigating to feed to check for post...")
            await page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            await page.wait_for_timeout(3000)
            await page.screenshot(path=f"diagnosis_step8_feed_check_{timestamp}.png")

            # Check if post is there
            page_content = await page.content()
            if f"Test post {timestamp}" in page_content:
                log("SUCCESS: Post found in feed!")
            else:
                log("PROBLEM: Post NOT found in feed")
                log("Checking for any recent posts...")
                if "Test post" in page_content:
                    log("Found 'Test post' text but not our specific one")
                else:
                    log("No test posts found at all")

            # Check profile
            log("\n10. Checking profile...")
            await page.goto('https://www.linkedin.com/in/me/', wait_until='networkidle')
            await page.wait_for_timeout(3000)
            await page.screenshot(path=f"diagnosis_step9_profile_{timestamp}.png")

            profile_content = await page.content()
            if f"Test post {timestamp}" in profile_content:
                log("SUCCESS: Post found on profile!")
            else:
                log("PROBLEM: Post NOT found on profile")

            log("\n" + "="*80)
            log("DIAGNOSIS COMPLETE")
            log("="*80)
            log(f"\nLog saved to: {log_file}")
            log(f"Screenshots saved with timestamp: {timestamp}")
            log("\nPlease check:")
            log("1. The screenshots to see what happened")
            log("2. Your LinkedIn profile manually")
            log("3. Report what you see")

        except Exception as e:
            log(f"\nERROR: {e}")
            import traceback
            log(traceback.format_exc())
            await page.screenshot(path=f"diagnosis_error_{timestamp}.png")

        finally:
            await page.wait_for_timeout(5000)  # Keep browser open for 5 more seconds
            await browser.close()
            log("\nBrowser closed")

if __name__ == "__main__":
    asyncio.run(diagnose_linkedin())
