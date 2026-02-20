#!/usr/bin/env python3
"""
Twitter/X Watcher - Playwright-based
Monitors Twitter mentions and DMs for business-related keywords
"""

import asyncio
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Add parent directory to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from Platinum_Tier.base_watcher import BaseWatcher

class TwitterWatcherPlaywright(BaseWatcher):
    """
    Watches Twitter/X for business-related mentions and DMs using Playwright.

    Features:
    - Persistent browser session (login once)
    - Monitors mentions and DMs for keywords
    - Creates action files for relevant interactions
    """

    def __init__(self):
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        super().__init__(vault_path=str(vault_path), check_interval=600)  # 10 minutes

        # Browser settings
        self.user_data_dir = Path(__file__).parent.parent / "browser_data" / "twitter"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)

        # Business keywords to monitor
        self.business_keywords = [
            'inquiry', 'pricing', 'quote', 'order', 'purchase',
            'business', 'service', 'product', 'interested',
            'how much', 'cost', 'price', 'buy', 'hire',
            'collaboration', 'partnership', 'sponsor'
        ]

        # Track seen items
        self.seen_mentions = set()
        self.seen_dms = set()

    def check_for_updates(self) -> list:
        """Check Twitter for new mentions and DMs"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async check for Twitter mentions and DMs"""
        new_items = []

        try:
            async with async_playwright() as p:
                # Launch persistent browser context
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage'
                    ],
                    viewport={'width': 1280, 'height': 720}
                )

                page = context.pages[0] if context.pages else await context.new_page()

                # Navigate to Twitter
                await page.goto('https://twitter.com', wait_until='networkidle')

                # Check if logged in
                if 'login' in page.url.lower() or await page.query_selector('input[name="text"]'):
                    self.logger.warning("Not logged in to Twitter. Please login manually.")
                    self.logger.info("Browser will stay open for manual login. Close when done.")
                    await asyncio.sleep(60)  # Wait for manual login
                    await context.close()
                    return []

                self.logger.info("Logged in to Twitter")

                # Check mentions
                await page.goto('https://twitter.com/notifications/mentions', wait_until='networkidle')
                await asyncio.sleep(3)

                # Get mentions
                mentions = await page.query_selector_all('[data-testid="tweet"]')
                self.logger.info(f"Found {len(mentions)} mentions")

                for mention in mentions[:10]:  # Check last 10
                    try:
                        text = await mention.inner_text()
                        text_lower = text.lower()

                        # Check for business keywords
                        has_keyword = any(keyword in text_lower for keyword in self.business_keywords)

                        if has_keyword:
                            # Generate unique ID
                            mention_id = hash(text[:100])

                            if mention_id not in self.seen_mentions:
                                # Get author
                                author = "Unknown"
                                try:
                                    author_elem = await mention.query_selector('[data-testid="User-Name"]')
                                    if author_elem:
                                        author = await author_elem.inner_text()
                                except:
                                    pass

                                new_items.append({
                                    'id': mention_id,
                                    'type': 'mention',
                                    'author': author,
                                    'text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'keywords_found': [kw for kw in self.business_keywords if kw in text_lower]
                                })
                                self.seen_mentions.add(mention_id)
                                self.logger.info(f"Found business mention from {author}: {text[:50]}...")

                    except Exception as e:
                        self.logger.error(f"Error processing mention: {e}")
                        continue

                # Check DMs
                await page.goto('https://twitter.com/messages', wait_until='networkidle')
                await asyncio.sleep(3)

                # Get message threads
                threads = await page.query_selector_all('[data-testid="conversation"]')
                self.logger.info(f"Found {len(threads)} DM threads")

                for thread in threads[:5]:  # Check last 5 threads
                    try:
                        text = await thread.inner_text()
                        text_lower = text.lower()

                        # Check for business keywords
                        has_keyword = any(keyword in text_lower for keyword in self.business_keywords)

                        if has_keyword:
                            # Generate unique ID
                            dm_id = hash(text[:100])

                            if dm_id not in self.seen_dms:
                                new_items.append({
                                    'id': dm_id,
                                    'type': 'dm',
                                    'text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'keywords_found': [kw for kw in self.business_keywords if kw in text_lower]
                                })
                                self.seen_dms.add(dm_id)
                                self.logger.info(f"Found business DM: {text[:50]}...")

                    except Exception as e:
                        self.logger.error(f"Error processing DM: {e}")
                        continue

                await context.close()

        except Exception as e:
            self.logger.error(f"Error checking Twitter: {e}")

        return new_items

    def create_action_file(self, item) -> Path:
        """Create action file for Twitter mention or DM"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        item_type = item.get('type', 'mention')

        content = f"""---
type: twitter_{item_type}
author: {item.get('author', 'Unknown')}
received: {item['timestamp']}
priority: high
status: pending
keywords: {', '.join(item['keywords_found'])}
---

## Twitter {item_type.title()}

**From:** {item.get('author', 'Unknown')}
**Received:** {item['timestamp']}

**Content:**
{item['text']}

**Keywords Detected:** {', '.join(item['keywords_found'])}

## Suggested Actions
- [ ] Review {item_type} details
- [ ] Reply to inquiry (requires approval)
- [ ] Mark as handled

## Context
This {item_type} was detected because it contains business-related keywords.
"""

        filename = f"TWITTER_{item_type.upper()}_{timestamp}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")

        # Also save to inbox
        inbox_content = f"Twitter {item_type.title()} - {item['timestamp']}\n\n{item['text']}"
        self.save_to_inbox(item, f"TWITTER_{timestamp}.txt", inbox_content)

        return filepath

if __name__ == "__main__":
    watcher = TwitterWatcherPlaywright()
    watcher.run()
