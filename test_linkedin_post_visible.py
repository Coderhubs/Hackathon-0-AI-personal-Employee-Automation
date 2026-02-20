"""
Test LinkedIn posting with visible browser to debug the issue
"""
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def test_post_with_verification():
    """Test posting with visible browser and better verification"""

    base_dir = Path(__file__).parent
    user_data_dir = base_dir / "browser_data" / "linkedin"

    print("="*80)
    print("LinkedIn Post Test - Visible Browser")
    print("="*80)
    print("\nThis will open a visible browser so you can watch what happens.")
    print("Please observe carefully and report what you see.\n")

    async with async_playwright() as p:
        # Launch VISIBLE browser
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,  # VISIBLE BROWSER
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()

        try:
            # Navigate to LinkedIn
            print("1. Navigating to LinkedIn...")
            await page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            await page.wait_for_timeout(3000)

            # Check if logged in
            print("2. Checking login status...")
            if 'login' in page.url or 'authwall' in page.url:
                print("NOT LOGGED IN - Please login manually in the browser")
                input("Press Enter after you've logged in...")
                await page.goto('https://www.linkedin.com/feed/')
                await page.wait_for_timeout(3000)
            else:
                print("OK - Logged in")

            # Open post composer
            print("\n3. Opening post composer...")
            start_post = await page.query_selector('button:has-text("Start a post")')
            if not start_post:
                print("ERROR: Could not find 'Start a post' button")
                input("Press Enter to close...")
                return

            await start_post.click()
            await page.wait_for_timeout(2000)
            print("OK - Composer opened")

            # Type test content
            print("\n4. Typing test content...")
            test_content = f"Test post - {asyncio.get_event_loop().time()}\n\nThis is a test to verify posting works correctly."

            editor = await page.query_selector('.ql-editor')
            if not editor:
                print("ERROR: Could not find editor")
                input("Press Enter to close...")
                return

            await editor.click()
            await page.wait_for_timeout(500)
            await editor.fill(test_content)
            await page.wait_for_timeout(1000)
            print(f"OK - Content typed: {len(test_content)} characters")

            # Find Post button
            print("\n5. Looking for Post button...")
            post_button = await page.query_selector('button:has-text("Post")')
            if not post_button:
                print("ERROR: Could not find Post button")
                input("Press Enter to close...")
                return

            # Check if enabled
            is_disabled = await post_button.get_attribute('disabled')
            if is_disabled:
                print("ERROR: Post button is DISABLED")
                print("This means LinkedIn won't accept the post.")
                input("Press Enter to close...")
                return

            print("OK - Post button found and enabled")

            # PAUSE before clicking
            print("\n" + "="*80)
            print("READY TO POST")
            print("="*80)
            print("\nWatch carefully what happens after clicking Post:")
            print("- Does the modal close?")
            print("- Do you see any error messages?")
            print("- Does the post appear in your feed?")
            print("\nPress Enter to click the Post button...")
            input()

            # Click Post
            print("\n6. Clicking Post button...")
            await post_button.click()
            print("OK - Clicked")

            # Wait and observe
            print("\n7. Waiting 5 seconds to observe...")
            await page.wait_for_timeout(5000)

            # Check current URL
            current_url = page.url
            print(f"\nCurrent URL: {current_url}")

            # Check if modal is still visible
            modal = await page.query_selector('.share-box-footer')
            if modal:
                is_visible = await modal.is_visible()
                print(f"Modal still visible: {is_visible}")
            else:
                print("Modal not found (might have closed)")

            # Wait longer
            print("\n8. Waiting additional 10 seconds...")
            await page.wait_for_timeout(10000)

            # Try to find the post in feed
            print("\n9. Checking if post appears in feed...")
            await page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            await page.wait_for_timeout(3000)

            # Look for our test content
            page_content = await page.content()
            if "Test post -" in page_content:
                print("SUCCESS: POST FOUND IN FEED!")
            else:
                print("PROBLEM: POST NOT FOUND IN FEED")

            print("\n" + "="*80)
            print("TEST COMPLETE")
            print("="*80)
            print("\nPlease check your LinkedIn profile manually:")
            print("1. Go to your profile")
            print("2. Check your recent posts")
            print("3. Report if you see the test post or not")
            print("\nPress Enter to close browser...")
            input()

        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            input("Press Enter to close...")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_post_with_verification())
