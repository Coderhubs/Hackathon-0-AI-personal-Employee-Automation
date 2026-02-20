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
        self.user_data_dir = Path("Platinum_Tier/browser_data/linkedin")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self.setup_logging()
        self.last_post_ids = set()
        # Keywords for Agentic AI filtering
        self.agentic_keywords = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt', 'artificial intelligence', 'machine learning']

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
        """Login to LinkedIn - checks for existing session first"""
        try:
            self.logger.info("Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Check if already logged in (persistent session)
            try:
                feed_check = await page.query_selector('[data-id^="urn:li:activity"]')
                if feed_check or "feed" in page.url:
                    self.logger.info("✓ Already logged in via persistent session!")
                    return True
            except:
                pass

            # Not logged in - proceed with login
            self.logger.info("No active session found. Logging in...")
            await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Enter email
            self.logger.info("Entering email...")
            email_input = await page.wait_for_selector('input[name="session_key"]', timeout=10000)
            await email_input.fill(self.email)
            await page.wait_for_timeout(1000)

            # Enter password - type slowly to avoid detection
            self.logger.info("Entering password...")
            password_input = await page.wait_for_selector('input[name="session_password"]', timeout=10000)
            await password_input.type(self.password, delay=100)
            await page.wait_for_timeout(1000)

            # Click sign in
            self.logger.info("Clicking sign in...")
            sign_in_button = await page.query_selector('button[type="submit"]')
            if sign_in_button:
                await sign_in_button.click()
            await page.wait_for_timeout(8000)

            # Check if we need to handle verification
            if await page.query_selector('input[name="pin"]'):
                self.logger.warning("LinkedIn requires verification code. Please check your email/phone.")
                self.logger.info("Waiting 60 seconds for manual verification...")
                await page.wait_for_timeout(60000)

            # Wait for feed to load
            self.logger.info("Waiting for feed to load...")
            await page.wait_for_selector('[role="main"]', timeout=45000)
            self.logger.info("Successfully logged into LinkedIn!")
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            self.logger.info("Browser will stay open for 30 seconds for manual login if needed...")
            await page.wait_for_timeout(30000)
            return False

    async def fetch_feed_posts(self, page):
        """Fetch recent posts from LinkedIn feed, filter for Agentic AI content"""
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
            for post in posts[:10]:  # Check top 10 posts
                try:
                    # Extract post data
                    author_elem = await post.query_selector('.update-components-actor__name')
                    content_elem = await post.query_selector('.feed-shared-update-v2__description')

                    author = await author_elem.inner_text() if author_elem else "Unknown"
                    content = await content_elem.inner_text() if content_elem else "No content"

                    # Get post ID from data attribute
                    post_id = await post.get_attribute('data-id')

                    # Filter for Agentic AI content
                    text_to_check = content.lower()
                    is_agentic_ai = any(keyword in text_to_check for keyword in self.agentic_keywords)

                    if post_id and post_id not in self.last_post_ids and is_agentic_ai:
                        new_posts.append({
                            'author': author.strip(),
                            'content': content.strip()[:500],  # Limit content length
                            'post_id': post_id,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.last_post_ids.add(post_id)
                        self.logger.info(f"📱 Agentic AI post by: {author.strip()[:30]}")

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
        filename = f"LINKEDIN_AGENTIC_{timestamp}_{safe_author}.txt"
        filepath = self.inbox_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Author: {post_data['author']}\n")
            f.write(f"Date: {post_data['timestamp']}\n")
            f.write(f"Post ID: {post_data['post_id']}\n")
            f.write(f"Category: Agentic AI\n")
            f.write("-" * 40 + "\n")
            f.write(post_data['content'])

        self.logger.info(f"Saved LinkedIn post: {filepath}")

    async def create_post(self, page, content):
        """Create a LinkedIn post about Agentic AI"""
        try:
            self.logger.info("Creating LinkedIn post about Agentic AI...")

            # Navigate to feed
            await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
            await page.wait_for_timeout(2000)

            # Click "Start a post" button
            start_post_btn = await page.query_selector('button.artdeco-button:has-text("Start a post")')
            if not start_post_btn:
                # Try alternative selectors
                start_post_btn = await page.query_selector('[aria-label*="Start a post"]')
            if not start_post_btn:
                start_post_btn = await page.query_selector('button[aria-label*="post"]')

            if start_post_btn:
                await start_post_btn.click()
                await page.wait_for_timeout(2000)
            else:
                self.logger.error("Could not find 'Start a post' button")
                return False

            # Fill in post content
            editor = await page.query_selector('.ql-editor')
            if not editor:
                editor = await page.query_selector('[role="textbox"]')
            if not editor:
                editor = await page.query_selector('div[contenteditable="true"]')

            if editor:
                await editor.fill(content)
                await page.wait_for_timeout(1000)
            else:
                self.logger.error("Could not find post editor")
                return False

            # Click Post button
            post_btn = await page.query_selector('button.share-actions__primary-action')
            if not post_btn:
                post_btn = await page.query_selector('button:has-text("Post")')
            if not post_btn:
                post_btn = await page.query_selector('[aria-label*="Post"]')

            if post_btn:
                await post_btn.click()
                await page.wait_for_timeout(3000)
                self.logger.info("✓ LinkedIn post created successfully")
                return True
            else:
                self.logger.error("Could not find Post button")
                return False

        except Exception as e:
            self.logger.error(f"Failed to create post: {e}")
            return False

    async def run(self, create_demo_post=False):
        """Main run loop"""
        async with async_playwright() as p:
            # Launch persistent browser context - saves session for reuse
            self.logger.info(f"Using persistent session from: {self.user_data_dir}")
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.user_data_dir),
                headless=False,
                args=[
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ],
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.pages[0] if context.pages else await context.new_page()

            # Login
            if not await self.login_to_linkedin(page):
                self.logger.error("Failed to login. Exiting.")
                await browser.close()
                return

            # Create demo post if requested
            if create_demo_post:
                demo_content = f"""🤖 Agentic AI Technology Update - {datetime.now().strftime('%B %d, %Y')}

The landscape of Agentic AI is evolving rapidly. Here are today's key insights:

✨ Autonomous agents are transforming how we interact with AI systems
🔧 Tool-using LLMs are enabling practical real-world applications
🚀 Multi-agent systems are solving complex problems collaboratively
💡 Claude, GPT-4, and other models are powering intelligent workflows

The future of AI is not just about answering questions—it's about taking action autonomously.

#AgenticAI #ArtificialIntelligence #AI #MachineLearning #Automation #LLM #Claude #GPT

[Posted by AI Personal Employee System]"""

                self.logger.info("Creating demo post about Agentic AI...")
                await self.create_post(page, demo_content)

            # Main monitoring loop
            retry_count = 0
            max_retries = 5

            self.logger.info("Starting monitoring for Agentic AI posts...")
            while True:
                try:
                    self.logger.info("Checking for new Agentic AI posts...")
                    new_posts = await self.fetch_feed_posts(page)

                    if new_posts:
                        self.logger.info(f"Found {len(new_posts)} new Agentic AI post(s)")
                        for post in new_posts:
                            self.save_post_to_file(post)
                    else:
                        self.logger.info("No new Agentic AI posts")

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
                        browser = await p.chromium.launch(
                            headless=False,
                            args=[
                                '--disable-gpu',
                                '--no-sandbox',
                                '--disable-dev-shm-usage',
                                '--disable-blink-features=AutomationControlled'
                            ]
                        )
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

    # Set create_demo_post=True to test post creation
    asyncio.run(watcher.run(create_demo_post=True))

if __name__ == "__main__":
    main()
