"""
Real LinkedIn Watcher using Playwright
Automates browser to login and fetch real LinkedIn feed posts
"""
import os
import time
import asyncio
from datetime import datetime
from pathlib import Path
import logging
from playwright.async_api import async_playwright
import json

class LinkedInWatcherPlaywright:
    def __init__(self, email, password, check_interval=120):
        self.email = email
        self.password = password
        self.check_interval = check_interval  # seconds
        self.inbox_dir = Path("Inbox")
        self.inbox_dir.mkdir(exist_ok=True)
        self.logger = self.setup_logging()
        self.last_post_ids = set()

    def setup_logging(self):
        """Setup logging to file"""
        log_dir = Path("Gold_Tier/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'linkedin_watcher_playwright.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedInWatcherPlaywright')

    async def login_to_linkedin(self, page):
        """Login to LinkedIn"""
        try:
            self.logger.info("Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/login", wait_until="networkidle")

            # Enter email
            self.logger.info("Entering email...")
            await page.fill('input[name="session_key"]', self.email)

            # Enter password
            self.logger.info("Entering password...")
            await page.fill('input[name="session_password"]', self.password)

            # Click sign in
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)

            # Check if we need to handle verification
            if await page.query_selector('input[name="pin"]'):
                self.logger.warning("LinkedIn requires verification code. Please check your email/phone.")
                # Wait for manual verification (60 seconds)
                await page.wait_for_timeout(60000)

            # Wait for feed to load
            self.logger.info("Waiting for feed to load...")
            await page.wait_for_selector('[role="main"]', timeout=30000)
            self.logger.info("Successfully logged into LinkedIn!")
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False

    async def fetch_feed_posts(self, page):
        """Fetch recent posts from LinkedIn feed"""
        try:
            # Navigate to feed if not already there
            current_url = page.url
            if 'feed' not in current_url:
                await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
                await page.wait_for_timeout(3000)

            # Scroll to load more posts
            await page.evaluate("window.scrollTo(0, 1000)")
            await page.wait_for_timeout(2000)

            # Get post containers
            posts = await page.query_selector_all('[data-id^="urn:li:activity"]')

            new_posts = []
            for post in posts[:5]:  # Get top 5 posts
                try:
                    # Extract post data
                    author_elem = await post.query_selector('.update-components-actor__name')
                    content_elem = await post.query_selector('.feed-shared-update-v2__description')

                    author = await author_elem.inner_text() if author_elem else "Unknown"
                    content = await content_elem.inner_text() if content_elem else "No content"

                    # Get post ID from data attribute
                    post_id = await post.get_attribute('data-id')

                    if post_id and post_id not in self.last_post_ids:
                        new_posts.append({
                            'author': author.strip(),
                            'content': content.strip()[:500],  # Limit content length
                            'post_id': post_id,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.last_post_ids.add(post_id)

                except Exception as e:
                    self.logger.warning(f"Error parsing post: {e}")
                    continue

            return new_posts

        except Exception as e:
            self.logger.error(f"Error fetching posts: {e}")
            return []

    def save_post_to_file(self, post_data):
        """Save LinkedIn post to Inbox folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_author = post_data['author'].replace(' ', '_').replace(':', '')[:30]
        filename = f"LINKEDIN_{timestamp}_{safe_author}.txt"
        filepath = self.inbox_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Author: {post_data['author']}\n")
            f.write(f"Date: {post_data['timestamp']}\n")
            f.write(f"Post ID: {post_data['post_id']}\n")
            f.write("-" * 40 + "\n")
            f.write(post_data['content'])

        self.logger.info(f"Saved LinkedIn post: {filepath}")

    async def run(self):
        """Main run loop"""
        async with async_playwright() as p:
            # Launch browser (headless=False to see what's happening)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()

            # Login
            if not await self.login_to_linkedin(page):
                self.logger.error("Failed to login. Exiting.")
                await browser.close()
                return

            # Main monitoring loop
            retry_count = 0
            max_retries = 5

            while True:
                try:
                    self.logger.info("Checking for new LinkedIn posts...")
                    new_posts = await self.fetch_feed_posts(page)

                    if new_posts:
                        self.logger.info(f"Found {len(new_posts)} new post(s)")
                        for post in new_posts:
                            self.save_post_to_file(post)
                    else:
                        self.logger.info("No new posts")

                    retry_count = 0  # Reset on success
                    await asyncio.sleep(self.check_interval)

                except KeyboardInterrupt:
                    self.logger.info("LinkedIn Watcher stopped by user.")
                    break

                except Exception as e:
                    retry_count += 1
                    self.logger.error(f"Error in LinkedIn Watcher: {e}")

                    if retry_count <= max_retries:
                        delay = 2 ** (retry_count - 1)
                        self.logger.warning(f"Retry {retry_count}/{max_retries} in {delay} seconds...")
                        await asyncio.sleep(delay)
                    else:
                        self.logger.critical(f"Max retries reached. Restarting browser...")
                        await browser.close()
                        browser = await p.chromium.launch(headless=False)
                        context = await browser.new_context(
                            viewport={'width': 1280, 'height': 720},
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        )
                        page = await context.new_page()
                        await self.login_to_linkedin(page)
                        retry_count = 0

            await browser.close()

def main():
    """Main entry point"""
    # Load credentials from environment
    from dotenv import load_dotenv
    load_dotenv()

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("ERROR: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        return

    watcher = LinkedInWatcherPlaywright(
        email=email,
        password=password,
        check_interval=120  # Check every 2 minutes
    )

    asyncio.run(watcher.run())

if __name__ == "__main__":
    main()
