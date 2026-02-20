"""
LinkedIn Watcher with Persistent Session - Login once manually, then auto-monitor
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import json

class LinkedInWatcherPersistent:
    def __init__(self, email, password, check_interval=120):
        self.email = email
        self.password = password
        self.check_interval = check_interval
        self.inbox_dir = Path("Inbox")
        self.inbox_dir.mkdir(exist_ok=True)
        self.user_data_dir = Path("Platinum_Tier/browser_data/linkedin")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_posts = set()
        self.agentic_keywords = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt', 'artificial intelligence', 'machine learning']

    async def check_feed(self, page):
        """Check for new posts about Agentic AI"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking feed...")

        try:
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Scroll to load posts
            await page.evaluate("window.scrollTo(0, 1000)")
            await page.wait_for_timeout(2000)

            posts = await page.query_selector_all('[data-id^="urn:li:activity"]')
            new_posts = []

            for post in posts[:10]:
                try:
                    author_elem = await post.query_selector('.update-components-actor__name')
                    content_elem = await post.query_selector('.feed-shared-update-v2__description')

                    author = await author_elem.inner_text() if author_elem else "Unknown"
                    content = await content_elem.inner_text() if content_elem else ""

                    post_id = await post.get_attribute('data-id')
                    text_to_check = content.lower()
                    is_agentic_ai = any(keyword in text_to_check for keyword in self.agentic_keywords)

                    if post_id and post_id not in self.seen_posts and is_agentic_ai:
                        new_posts.append({
                            'author': author.strip(),
                            'content': content.strip()[:500],
                            'post_id': post_id,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.seen_posts.add(post_id)
                        print(f"  📱 Agentic AI post by: {author.strip()[:30]}")

                        # Save to file
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_author = author.replace(' ', '_').replace(':', '')[:30]
                        filename = f"LINKEDIN_AGENTIC_{timestamp}_{safe_author}.txt"
                        filepath = self.inbox_dir / filename

                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"Author: {author}\n")
                            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Post ID: {post_id}\n")
                            f.write(f"Category: Agentic AI\n")
                            f.write("-" * 40 + "\n")
                            f.write(content.strip()[:500])

                        print(f"  Saved: {filename}")

                except:
                    pass

            if not new_posts:
                print(f"  No new Agentic AI posts")

            return new_posts

        except Exception as e:
            print(f"  Error checking feed: {e}")
            return []

    async def create_post(self, page, content):
        """Create a LinkedIn post about Agentic AI"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Creating LinkedIn post...")

        try:
            await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Click "Start a post"
            start_post_btn = await page.query_selector('button:has-text("Start a post")')
            if start_post_btn:
                await start_post_btn.click()
                await page.wait_for_timeout(2000)

            # Fill content
            editor = await page.query_selector('.ql-editor')
            if not editor:
                editor = await page.query_selector('[role="textbox"]')

            if editor:
                await editor.fill(content)
                await page.wait_for_timeout(1000)

            # Click Post
            post_btn = await page.query_selector('button:has-text("Post")')
            if post_btn:
                await post_btn.click()
                await page.wait_for_timeout(3000)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Post created successfully")
                return True

        except Exception as e:
            print(f"  Error creating post: {e}")
            return False

    async def run(self, create_demo_post=False):
        """Main run loop with persistent session"""
        print("=" * 70)
        print("LinkedIn Watcher - Agentic AI Monitor")
        print("=" * 70)
        print(f"Email: {self.email}")
        print(f"Check interval: {self.check_interval} seconds")
        print(f"Keywords: {', '.join(self.agentic_keywords)}")
        print("=" * 70)
        print("\nIMPORTANT: Browser will open. Please login manually if needed.")
        print("Your session will be saved for future runs.\n")

        async with async_playwright() as p:
            # Launch with persistent context
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.user_data_dir),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ],
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            page = context.pages[0] if context.pages else await context.new_page()

            try:
                # Navigate to LinkedIn
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening LinkedIn...")
                await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                await page.wait_for_timeout(5000)

                # Check if already logged in
                if 'login' in page.url:
                    print("\n[!] Please login manually in the browser window.")
                    print("    Your session will be saved for future runs.")
                    print("    Waiting 60 seconds for you to complete login...\n")
                    await page.wait_for_timeout(60000)
                    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)

                # Wait for feed
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for feed...")
                await page.wait_for_selector('[role="main"]', timeout=30000)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Logged in successfully!\n")

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

                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Creating demo post...")
                    await self.create_post(page, demo_content)
                    print()

                # Main monitoring loop
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting monitoring loop...")
                print("Press Ctrl+C to stop\n")

                while True:
                    await self.check_feed(page)
                    await asyncio.sleep(self.check_interval)

            except KeyboardInterrupt:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Watcher stopped by user")
            except Exception as e:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            finally:
                await context.close()

def main():
    """Main entry point"""
    from dotenv import load_dotenv
    load_dotenv()

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("ERROR: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        return

    watcher = LinkedInWatcherPersistent(
        email=email,
        password=password,
        check_interval=120
    )

    # Set create_demo_post=True to test post creation
    asyncio.run(watcher.run(create_demo_post=True))

if __name__ == "__main__":
    main()
