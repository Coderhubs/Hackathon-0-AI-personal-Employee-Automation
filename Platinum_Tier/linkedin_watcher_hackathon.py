"""
LinkedIn Watcher - Hackathon Compliant
Monitors LinkedIn and writes to Needs_Action/ folder
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio
from base_watcher import BaseWatcher

class LinkedInWatcherHackathon(BaseWatcher):
    def __init__(self, vault_path: str, email: str, password: str):
        super().__init__(vault_path, check_interval=120)
        self.email = email
        self.password = password
        self.user_data_dir = Path("Platinum_Tier/browser_data/linkedin")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_posts = set()
        self.agentic_keywords = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt', 'artificial intelligence', 'machine learning']
        self.page = None
        self.context = None

    async def initialize_browser(self):
        """Initialize browser with persistent session"""
        p = await async_playwright().start()
        self.context = await p.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage'
            ],
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

        # Navigate to LinkedIn
        self.logger.info("Opening LinkedIn...")
        await self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(5000)

        # Check if login needed
        if 'login' in self.page.url:
            self.logger.info("Please login manually in the browser window")
            self.logger.info("Waiting 60 seconds for login...")
            await self.page.wait_for_timeout(60000)
            await self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await self.page.wait_for_timeout(3000)

        # Wait for feed
        await self.page.wait_for_selector('[role="main"]', timeout=30000)
        self.logger.info("Logged into LinkedIn successfully")

    def check_for_updates(self) -> list:
        """Check LinkedIn feed for new Agentic AI posts"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async version of check_for_updates"""
        if not self.page:
            await self.initialize_browser()

        try:
            await self.page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
            await self.page.wait_for_timeout(3000)

            # Scroll to load posts
            await self.page.evaluate("window.scrollTo(0, 1000)")
            await self.page.wait_for_timeout(2000)

            posts = await self.page.query_selector_all('[data-id^="urn:li:activity"]')
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
                            'timestamp': datetime.now().isoformat()
                        })
                        self.seen_posts.add(post_id)
                        self.logger.info(f"Found Agentic AI post by: {author.strip()[:30]}")

                except Exception as e:
                    self.logger.warning(f"Error parsing post: {e}")
                    continue

            return new_posts

        except Exception as e:
            self.logger.error(f"Error checking feed: {e}")
            return []

    def create_action_file(self, post) -> Path:
        """Create action file in Needs_Action/ folder with proper format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_author = post['author'].replace(' ', '_').replace(':', '')[:30]

        # Determine priority based on content
        priority = 'high' if any(kw in post['content'].lower() for kw in ['breaking', 'new', 'announcement']) else 'medium'

        # Create action file content with frontmatter
        content = f"""---
type: linkedin_post
author: {post['author']}
post_id: {post['post_id']}
received: {post['timestamp']}
priority: {priority}
status: pending
keywords: agentic_ai
---

## Post Content
{post['content']}

## Suggested Actions
- [ ] Read full post
- [ ] Like the post
- [ ] Comment with insights about Agentic AI
- [ ] Share to network (requires approval)
- [ ] Save for reference
- [ ] Create related content
- [ ] Update Dashboard

## Context
This post was detected by LinkedIn watcher because it contains Agentic AI keywords.
Keywords matched: {', '.join([kw for kw in self.agentic_keywords if kw in post['content'].lower()])}

## Engagement Strategy
Consider engaging with this post to:
1. Build thought leadership in Agentic AI space
2. Connect with others interested in autonomous agents
3. Share insights from your AI Employee project
"""

        # Save to Needs_Action folder
        filename = f"LINKEDIN_{timestamp}_{safe_author}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")

        # Also save to Inbox for reference
        inbox_content = f"""Author: {post['author']}
Date: {post['timestamp']}
Post ID: {post['post_id']}
Category: Agentic AI

{post['content']}
"""
        self.save_to_inbox(post, f"LINKEDIN_AGENTIC_{timestamp}_{safe_author}.txt", inbox_content)

        return filepath

def main():
    """Main entry point"""
    load_dotenv()

    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')

    if not email or not password:
        print("ERROR: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        return

    # Vault path
    vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    watcher = LinkedInWatcherHackathon(
        vault_path=str(vault_path),
        email=email,
        password=password
    )

    print("=" * 70)
    print("LinkedIn Watcher - Hackathon Compliant")
    print("=" * 70)
    print(f"Email: {email}")
    print(f"Vault: {vault_path}")
    print(f"Needs_Action: {vault_path / 'Needs_Action'}")
    print(f"Check interval: 120 seconds (2 minutes)")
    print("=" * 70)
    print()

    watcher.run()

if __name__ == "__main__":
    main()
