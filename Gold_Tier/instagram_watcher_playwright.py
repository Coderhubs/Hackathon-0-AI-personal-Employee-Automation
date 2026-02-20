#!/usr/bin/env python3
"""
Instagram Watcher - Playwright-based
Monitors Instagram DMs for business-related keywords
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

class InstagramWatcherPlaywright(BaseWatcher):
    """
    Watches Instagram for business-related DMs using Playwright.

    Features:
    - Persistent browser session (login once)
    - Monitors DMs for keywords
    - Creates action files for relevant messages
    """

    def __init__(self):
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        super().__init__(vault_path=str(vault_path), check_interval=600)  # 10 minutes

        # Browser settings
        self.user_data_dir = Path(__file__).parent.parent / "browser_data" / "instagram"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)

        # Business keywords to monitor
        self.business_keywords = [
            'inquiry', 'pricing', 'quote', 'order', 'purchase',
            'business', 'service', 'product', 'interested',
            'how much', 'cost', 'price', 'buy', 'hire',
            'collaboration', 'partnership', 'sponsor'
        ]

        # Track seen messages
        self.seen_messages = set()

    def check_for_updates(self) -> list:
        """Check Instagram for new DMs"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async check for Instagram DMs"""
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

                # Navigate to Instagram
                await page.goto('https://www.instagram.com', wait_until='networkidle')

                # Check if logged in
                if 'login' in page.url.lower() or await page.query_selector('input[name="username"]'):
                    self.logger.warning("Not logged in to Instagram. Please login manually.")
                    self.logger.info("Browser will stay open for manual login. Close when done.")
                    await asyncio.sleep(60)  # Wait for manual login
                    await context.close()
                    return []

                self.logger.info("Logged in to Instagram")

                # Navigate to DMs
                await page.goto('https://www.instagram.com/direct/inbox/', wait_until='networkidle')
                await asyncio.sleep(3)

                # Get message threads
                threads = await page.query_selector_all('[role="listitem"]')
                self.logger.info(f"Found {len(threads)} message threads")

                for thread in threads[:5]:  # Check last 5 threads
                    try:
                        # Click on thread to open
                        await thread.click()
                        await asyncio.sleep(2)

                        # Get messages in thread
                        messages = await page.query_selector_all('[role="row"]')

                        for message in messages[-3:]:  # Check last 3 messages
                            try:
                                text = await message.inner_text()
                                text_lower = text.lower()

                                # Check for business keywords
                                has_keyword = any(keyword in text_lower for keyword in self.business_keywords)

                                if has_keyword:
                                    # Generate unique ID
                                    msg_id = hash(text[:100])

                                    if msg_id not in self.seen_messages:
                                        # Get sender info
                                        sender = "Unknown"
                                        try:
                                            sender_elem = await page.query_selector('[role="heading"]')
                                            if sender_elem:
                                                sender = await sender_elem.inner_text()
                                        except:
                                            pass

                                        new_items.append({
                                            'id': msg_id,
                                            'sender': sender,
                                            'text': text,
                                            'timestamp': datetime.now().isoformat(),
                                            'keywords_found': [kw for kw in self.business_keywords if kw in text_lower]
                                        })
                                        self.seen_messages.add(msg_id)
                                        self.logger.info(f"Found business DM from {sender}: {text[:50]}...")

                            except Exception as e:
                                self.logger.error(f"Error processing message: {e}")
                                continue

                    except Exception as e:
                        self.logger.error(f"Error processing thread: {e}")
                        continue

                await context.close()

        except Exception as e:
            self.logger.error(f"Error checking Instagram: {e}")

        return new_items

    def create_action_file(self, item) -> Path:
        """Create action file for Instagram DM"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        content = f"""---
type: instagram_dm
sender: {item['sender']}
received: {item['timestamp']}
priority: high
status: pending
keywords: {', '.join(item['keywords_found'])}
---

## Instagram Direct Message

**From:** {item['sender']}
**Received:** {item['timestamp']}

**Message:**
{item['text']}

**Keywords Detected:** {', '.join(item['keywords_found'])}

## Suggested Actions
- [ ] Review message details
- [ ] Reply to inquiry (requires approval)
- [ ] Mark as handled

## Context
This message was detected because it contains business-related keywords.
"""

        filename = f"INSTAGRAM_{timestamp}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")

        # Also save to inbox
        inbox_content = f"Instagram DM from {item['sender']} - {item['timestamp']}\n\n{item['text']}"
        self.save_to_inbox(item, f"INSTAGRAM_{timestamp}.txt", inbox_content)

        return filepath

if __name__ == "__main__":
    watcher = InstagramWatcherPlaywright()
    watcher.run()
