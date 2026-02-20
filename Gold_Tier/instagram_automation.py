#!/usr/bin/env python3
"""
Instagram Automation - Playwright-based
Executes approved Instagram actions
"""

import asyncio
import time
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

class InstagramAutomation:
    """
    Executes approved Instagram actions using Playwright.

    Features:
    - Posts photos with captions
    - Posts stories
    - Rate limiting (max 3 posts per hour)
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.approved_dir = self.base_dir / "AI_Employee_Vault" / "Approved"
        self.done_dir = self.base_dir / "AI_Employee_Vault" / "Done"
        self.user_data_dir = self.base_dir / "browser_data" / "instagram"

        # Rate limiting
        self.posts_this_hour = []
        self.max_posts_per_hour = 3

    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        # Remove posts older than 1 hour
        self.posts_this_hour = [t for t in self.posts_this_hour if now - t < 3600]

        if len(self.posts_this_hour) >= self.max_posts_per_hour:
            print(f"Rate limit reached: {len(self.posts_this_hour)} posts in last hour")
            return False
        return True

    async def post_photo(self, image_path: str, caption: str, hashtags: list = None) -> bool:
        """Post a photo with caption to Instagram"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to Instagram
                await page.goto('https://www.instagram.com', wait_until='networkidle')
                await asyncio.sleep(2)

                # Click on "Create" button (+ icon)
                await page.click('[aria-label="New post"]', timeout=10000)
                await asyncio.sleep(1)

                # Select "Post" option
                try:
                    await page.click('text=Post', timeout=5000)
                except:
                    pass  # May already be on post screen

                await asyncio.sleep(1)

                # Upload photo
                file_input = await page.query_selector('input[type="file"]')
                await file_input.set_input_files(image_path)
                await asyncio.sleep(3)

                # Click Next
                await page.click('text=Next', timeout=10000)
                await asyncio.sleep(2)

                # Click Next again (filters screen)
                await page.click('text=Next', timeout=10000)
                await asyncio.sleep(2)

                # Add caption
                full_caption = caption
                if hashtags:
                    full_caption += '\n\n' + ' '.join([f'#{tag}' for tag in hashtags])

                caption_area = await page.query_selector('[aria-label="Write a caption..."]')
                await caption_area.fill(full_caption)
                await asyncio.sleep(1)

                # Click Share
                await page.click('text=Share', timeout=10000)
                await asyncio.sleep(5)

                print(f"✓ Posted photo to Instagram: {caption[:50]}...")

                await context.close()

                # Update rate limit
                self.posts_this_hour.append(time.time())

                return True

        except Exception as e:
            print(f"✗ Error posting to Instagram: {e}")
            return False

    async def reply_to_dm(self, user: str, message: str) -> bool:
        """Reply to Instagram DM"""
        try:
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to DMs
                await page.goto('https://www.instagram.com/direct/inbox/', wait_until='networkidle')
                await asyncio.sleep(2)

                # Search for user
                search_box = await page.query_selector('[placeholder="Search..."]')
                await search_box.fill(user)
                await asyncio.sleep(2)

                # Click on first result
                await page.click('[role="listitem"]', timeout=10000)
                await asyncio.sleep(1)

                # Type message
                message_box = await page.query_selector('[aria-label="Message"]')
                await message_box.fill(message)
                await asyncio.sleep(1)

                # Send message
                await page.click('[type="submit"]', timeout=10000)
                await asyncio.sleep(2)

                print(f"✓ Sent DM to {user}: {message[:50]}...")

                await context.close()

                return True

        except Exception as e:
            print(f"✗ Error sending Instagram DM: {e}")
            return False

    def process_approved_files(self):
        """Process all approved Instagram files"""
        if not self.approved_dir.exists():
            print("Approved directory not found")
            return

        instagram_files = list(self.approved_dir.glob("INSTAGRAM_*.md"))

        if not instagram_files:
            print("No approved Instagram actions found")
            return

        print(f"Found {len(instagram_files)} approved Instagram action(s)")

        for file in instagram_files:
            if not self.check_rate_limit():
                print("Rate limit reached. Waiting...")
                break

            print(f"\nProcessing: {file.name}")

            # Read file content
            content = file.read_text(encoding='utf-8')

            # Parse action type and content
            if 'post_photo' in content.lower():
                # Extract image path and caption
                lines = content.split('\n')
                image_path = None
                caption = ""
                hashtags = []

                for line in lines:
                    if 'image_path:' in line.lower():
                        image_path = line.split(':', 1)[1].strip()
                    elif 'caption:' in line.lower():
                        caption = line.split(':', 1)[1].strip()
                    elif 'hashtags:' in line.lower():
                        hashtags = [tag.strip() for tag in line.split(':', 1)[1].split(',')]

                if image_path:
                    # Post photo
                    success = asyncio.run(self.post_photo(image_path, caption, hashtags))

                    if success:
                        # Move to Done
                        done_file = self.done_dir / file.name
                        file.rename(done_file)
                        print(f"✓ Moved to Done: {file.name}")

            time.sleep(3)  # Delay between posts

if __name__ == "__main__":
    automation = InstagramAutomation()
    automation.process_approved_files()
