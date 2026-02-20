#!/usr/bin/env python3
"""
Facebook Automation - Playwright-based
Executes approved Facebook actions
"""

import asyncio
import time
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

class FacebookAutomation:
    """
    Executes approved Facebook actions using Playwright.

    Features:
    - Posts status updates
    - Posts photos with captions
    - Rate limiting (max 5 posts per hour)
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.approved_dir = self.base_dir / "AI_Employee_Vault" / "Approved"
        self.done_dir = self.base_dir / "AI_Employee_Vault" / "Done"
        self.user_data_dir = self.base_dir / "browser_data" / "facebook"

        # Rate limiting
        self.posts_this_hour = []
        self.max_posts_per_hour = 5

    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        # Remove posts older than 1 hour
        self.posts_this_hour = [t for t in self.posts_this_hour if now - t < 3600]

        if len(self.posts_this_hour) >= self.max_posts_per_hour:
            print(f"Rate limit reached: {len(self.posts_this_hour)} posts in last hour")
            return False
        return True

    async def post_status(self, text: str) -> bool:
        """Post a status update to Facebook"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to Facebook
                await page.goto('https://www.facebook.com', wait_until='networkidle')
                await asyncio.sleep(2)

                # Click on "What's on your mind?" box
                await page.click('[aria-label*="What\'s on your mind"]', timeout=10000)
                await asyncio.sleep(1)

                # Type the status
                await page.keyboard.type(text, delay=50)
                await asyncio.sleep(1)

                # Click Post button
                await page.click('[aria-label="Post"]', timeout=10000)
                await asyncio.sleep(3)

                print(f"✓ Posted status to Facebook: {text[:50]}...")

                await context.close()

                # Update rate limit
                self.posts_this_hour.append(time.time())

                return True

        except Exception as e:
            print(f"✗ Error posting to Facebook: {e}")
            return False

    async def post_photo(self, image_path: str, caption: str) -> bool:
        """Post a photo with caption to Facebook"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to Facebook
                await page.goto('https://www.facebook.com', wait_until='networkidle')
                await asyncio.sleep(2)

                # Click on "Photo/video" button
                await page.click('[aria-label*="Photo/video"]', timeout=10000)
                await asyncio.sleep(1)

                # Upload photo
                file_input = await page.query_selector('input[type="file"]')
                await file_input.set_input_files(image_path)
                await asyncio.sleep(3)

                # Add caption
                await page.keyboard.type(caption, delay=50)
                await asyncio.sleep(1)

                # Click Post button
                await page.click('[aria-label="Post"]', timeout=10000)
                await asyncio.sleep(3)

                print(f"✓ Posted photo to Facebook with caption: {caption[:50]}...")

                await context.close()

                # Update rate limit
                self.posts_this_hour.append(time.time())

                return True

        except Exception as e:
            print(f"✗ Error posting photo to Facebook: {e}")
            return False

    def process_approved_files(self):
        """Process all approved Facebook files"""
        if not self.approved_dir.exists():
            print("Approved directory not found")
            return

        facebook_files = list(self.approved_dir.glob("FACEBOOK_*.md"))

        if not facebook_files:
            print("No approved Facebook actions found")
            return

        print(f"Found {len(facebook_files)} approved Facebook action(s)")

        for file in facebook_files:
            if not self.check_rate_limit():
                print("Rate limit reached. Waiting...")
                break

            print(f"\nProcessing: {file.name}")

            # Read file content
            content = file.read_text(encoding='utf-8')

            # Parse action type and content
            if 'post_status' in content.lower():
                # Extract text to post
                lines = content.split('\n')
                text = '\n'.join([l for l in lines if l and not l.startswith('#') and not l.startswith('-')])

                # Post status
                success = asyncio.run(self.post_status(text[:500]))  # Limit to 500 chars

                if success:
                    # Move to Done
                    done_file = self.done_dir / file.name
                    file.rename(done_file)
                    print(f"✓ Moved to Done: {file.name}")

            time.sleep(2)  # Delay between posts

if __name__ == "__main__":
    automation = FacebookAutomation()
    automation.process_approved_files()
