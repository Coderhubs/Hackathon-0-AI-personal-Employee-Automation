"""
LinkedIn Automation - Posts content from approved files
Works with orchestrator - accepts file path as argument
"""
import os
import sys
import time
import asyncio
from pathlib import Path
import logging
import re
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

class LinkedInAutomation:
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.base_dir = Path(__file__).parent.parent
        self.user_data_dir = self.base_dir / "browser_data" / "linkedin"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_dir = self.base_dir / "AI_Employee_Vault" / "Logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'linkedin_automation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedInAutomation')

    def extract_post_content(self, file_path: Path) -> str:
        """Extract post content from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for content between "## Post Content" and next "##" or end
            match = re.search(r'## Post Content\s*\n\n(.*?)(?:\n\n##|\Z)', content, re.DOTALL)
            if match:
                post_content = match.group(1).strip()
                self.logger.info(f"Extracted post content ({len(post_content)} chars)")
                return post_content
            else:
                self.logger.error("Could not find '## Post Content' section in file")
                return None

        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            return None

    async def check_login(self, page):
        """Check if already logged in"""
        try:
            self.logger.info("Checking login status...")
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            # Check if feed is visible
            feed_check = await page.query_selector('[aria-label="Main Feed"]')
            if feed_check:
                self.logger.info("[SUCCESS] Already logged in via saved session")
                return True

            # Check if we're on login page
            if 'login' in page.url:
                self.logger.error("[ERROR] Not logged in - session expired")
                self.logger.error("Please run: python setup_linkedin_login.py")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error checking login: {e}")
            return False

    async def post_content(self, page, content: str) -> bool:
        """Post content to LinkedIn"""
        try:
            self.logger.info("[POST] Creating LinkedIn post...")

            # Navigate to feed
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2000)

            # Click "Start a post" button
            self.logger.info("[POST] Looking for 'Start a post' button...")
            start_post_selectors = [
                'button:has-text("Start a post")',
                '[aria-label="Start a post"]',
                'button[aria-label="Start a post"]',
                '.share-box-feed-entry__trigger'
            ]

            start_post_button = None
            for selector in start_post_selectors:
                try:
                    start_post_button = await page.query_selector(selector)
                    if start_post_button:
                        self.logger.info(f"[POST] Found button with selector: {selector}")
                        break
                except:
                    continue

            if start_post_button:
                await start_post_button.click()
                await page.wait_for_timeout(2000)
            else:
                self.logger.error("[ERROR] Could not find 'Start a post' button")
                return False

            # Wait for editor to appear
            self.logger.info("[POST] Waiting for editor...")
            editor_selectors = [
                '[role="textbox"]',
                '.ql-editor',
                '[contenteditable="true"]'
            ]

            editor = None
            for selector in editor_selectors:
                try:
                    editor = await page.wait_for_selector(selector, timeout=10000)
                    if editor:
                        self.logger.info(f"[POST] Found editor with selector: {selector}")
                        break
                except:
                    continue

            if not editor:
                self.logger.error("[ERROR] Could not find editor")
                return False

            await page.wait_for_timeout(1000)

            # Type content
            self.logger.info("[POST] Typing content...")
            await editor.fill(content)
            await page.wait_for_timeout(2000)

            # Click Post button
            self.logger.info("[POST] Looking for 'Post' button...")
            post_button_selectors = [
                'button:has-text("Post")',
                '[aria-label="Post"]',
                'button[aria-label="Post"]'
            ]

            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = await page.query_selector(selector)
                    if post_button:
                        self.logger.info(f"[POST] Found button with selector: {selector}")
                        break
                except:
                    continue

            if post_button:
                await post_button.click()

                # CRITICAL: Wait for post to actually upload
                self.logger.info("[POST] Waiting for post to upload...")
                await page.wait_for_timeout(3000)

                # Wait for modal to close (indicates post published)
                try:
                    self.logger.info("[POST] Verifying post published...")
                    await page.wait_for_selector('.share-box-footer', state='hidden', timeout=15000)
                    self.logger.info("[POST] ✓ Post modal closed")
                except:
                    self.logger.warning("[POST] Could not verify modal closed, waiting longer...")
                    await page.wait_for_timeout(5000)

                # Additional wait to ensure upload completes
                self.logger.info("[POST] Ensuring upload completes...")
                await page.wait_for_timeout(5000)

                # Verify we're back on feed
                current_url = page.url
                if 'linkedin.com/feed' in current_url:
                    self.logger.info("[SUCCESS] ✓ Returned to feed")
                else:
                    self.logger.warning(f"[POST] Not on feed page: {current_url}")
                    self.logger.info("[POST] Waiting additional 5 seconds...")
                    await page.wait_for_timeout(5000)

                self.logger.info("[SUCCESS] LinkedIn post published successfully!")
                return True
            else:
                self.logger.error("[ERROR] Could not find 'Post' button")
                return False

        except Exception as e:
            self.logger.error(f"[ERROR] Failed to post: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def post_from_file(self, file_path: Path) -> bool:
        """Post content from approved file"""
        self.logger.info("="*80)
        self.logger.info("LinkedIn Automation - Post from File")
        self.logger.info("="*80)
        self.logger.info(f"File: {file_path}")
        self.logger.info(f"Email: {self.email}")
        self.logger.info("="*80)

        # Extract content
        content = self.extract_post_content(file_path)
        if not content:
            self.logger.error("[ERROR] Failed to extract post content")
            return False

        self.logger.info(f"Post preview: {content[:100]}...")

        async with async_playwright() as p:
            # Launch persistent browser context
            self.logger.info("[INIT] Launching browser with saved session...")
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox'
                    ],
                    timeout=60000
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Check if logged in
                if not await self.check_login(page):
                    await context.close()
                    return False

                # Post content
                success = await self.post_content(page, content)

                # Close browser
                await context.close()

                return success

            except Exception as e:
                self.logger.error(f"[ERROR] Browser error: {e}")
                import traceback
                traceback.print_exc()
                return False

def main():
    """Main entry point"""
    # Check if file path provided
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python linkedin_automation.py <file_path>")
        print("[ERROR] Or run without arguments to process Approved folder")

        # Process all files in Approved folder
        base_dir = Path(__file__).parent.parent
        approved_dir = base_dir / "AI_Employee_Vault" / "Approved"

        if not approved_dir.exists():
            print(f"[ERROR] Approved folder not found: {approved_dir}")
            sys.exit(1)

        linkedin_files = list(approved_dir.glob("LINKEDIN_*.md"))
        if not linkedin_files:
            print("[INFO] No LinkedIn files found in Approved folder")
            sys.exit(0)

        print(f"[INFO] Found {len(linkedin_files)} LinkedIn file(s) to process")

        automation = LinkedInAutomation()
        success_count = 0

        for file_path in linkedin_files:
            print(f"\n[PROCESS] {file_path.name}")
            success = asyncio.run(automation.post_from_file(file_path))

            if success:
                success_count += 1
                # Move to Done
                done_dir = base_dir / "AI_Employee_Vault" / "Done"
                done_dir.mkdir(parents=True, exist_ok=True)
                done_file = done_dir / file_path.name
                file_path.rename(done_file)
                print(f"[SUCCESS] Moved to Done: {file_path.name}")
            else:
                print(f"[FAILED] {file_path.name}")

        print(f"\n[SUMMARY] Posted {success_count}/{len(linkedin_files)} successfully")
        sys.exit(0 if success_count == len(linkedin_files) else 1)

    # Process specific file
    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    linkedin_email = os.getenv("LINKEDIN_EMAIL")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    if not linkedin_email or not linkedin_password:
        print("[ERROR] LINKEDIN_EMAIL and LINKEDIN_PASSWORD must be set in .env file")
        sys.exit(1)

    automation = LinkedInAutomation()
    success = asyncio.run(automation.post_from_file(file_path))

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
