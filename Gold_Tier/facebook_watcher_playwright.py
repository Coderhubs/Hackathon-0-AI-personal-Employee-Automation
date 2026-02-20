#!/usr/bin/env python3
"""
Facebook Watcher - Playwright-based
Monitors Facebook notifications for business-related keywords
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

class FacebookWatcherPlaywright(BaseWatcher):
    """
    Watches Facebook for business-related notifications using Playwright.

    Features:
    - Persistent browser session (login once)
    - Monitors notifications for keywords
    - Creates action files for relevant items
    """

    def __init__(self):
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        super().__init__(vault_path=str(vault_path), check_interval=600)  # 10 minutes

        # Browser settings
        self.user_data_dir = Path(__file__).parent.parent / "browser_data" / "facebook"
        self.user_data_dir.mkdir(parents=True, exist_ok=True)

        # Business keywords to monitor
        self.business_keywords = [
            'inquiry', 'pricing', 'quote', 'order', 'purchase',
            'business', 'service', 'product', 'interested',
            'how much', 'cost', 'price', 'buy', 'hire'
        ]

        # Track seen notifications
        self.seen_notifications = set()

    def check_for_updates(self) -> list:
        """Check Facebook for new notifications"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async check for Facebook notifications"""
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

                # Navigate to Facebook
                await page.goto('https://www.facebook.com', wait_until='networkidle')

                # Check if logged in
                if 'login' in page.url.lower():
                    self.logger.warning("Not logged in to Facebook. Please login manually.")
                    self.logger.info("Browser will stay open for manual login. Close when done.")
                    await asyncio.sleep(60)  # Wait for manual login
                    await context.close()
                    return []

                self.logger.info("Logged in to Facebook")

                # Navigate to notifications
                await page.goto('https://www.facebook.com/notifications', wait_until='networkidle')
                await asyncio.sleep(3)

                # Get notifications
                notifications = await page.query_selector_all('[role="article"]')
                self.logger.info(f"Found {len(notifications)} notifications")

                for notification in notifications[:10]:  # Check last 10
                    try:
                        text = await notification.inner_text()
                        text_lower = text.lower()

                        # Check for business keywords
                        has_keyword = any(keyword in text_lower for keyword in self.business_keywords)

                        if has_keyword:
                            # Generate unique ID
                            notif_id = hash(text[:100])

                            if notif_id not in self.seen_notifications:
                                new_items.append({
                                    'id': notif_id,
                                    'text': text,
                                    'timestamp': datetime.now().isoformat(),
                                    'keywords_found': [kw for kw in self.business_keywords if kw in text_lower]
                                })
                                self.seen_notifications.add(notif_id)
                                self.logger.info(f"Found business notification: {text[:100]}...")

                    except Exception as e:
                        self.logger.error(f"Error processing notification: {e}")
                        continue

                await context.close()

        except Exception as e:
            self.logger.error(f"Error checking Facebook: {e}")

        return new_items

    def create_action_file(self, item) -> Path:
        """Create action file for Facebook notification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        content = f"""---
type: facebook_notification
received: {item['timestamp']}
priority: high
status: pending
keywords: {', '.join(item['keywords_found'])}
---

## Facebook Notification

**Received:** {item['timestamp']}

**Content:**
{item['text']}

**Keywords Detected:** {', '.join(item['keywords_found'])}

## Suggested Actions
- [ ] Review notification details
- [ ] Respond to inquiry (requires approval)
- [ ] Mark as handled

## Context
This notification was detected because it contains business-related keywords.
"""

        filename = f"FACEBOOK_{timestamp}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")

        # Also save to inbox
        inbox_content = f"Facebook Notification - {item['timestamp']}\n\n{item['text']}"
        self.save_to_inbox(item, f"FACEBOOK_{timestamp}.txt", inbox_content)

        return filepath

if __name__ == "__main__":
    watcher = FacebookWatcherPlaywright()
    watcher.run()
