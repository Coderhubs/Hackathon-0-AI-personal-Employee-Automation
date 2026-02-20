"""
WhatsApp Watcher - Hackathon Compliant
Monitors WhatsApp Web and writes to Needs_Action/ folder
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio
from base_watcher import BaseWatcher

class WhatsAppWatcherHackathon(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=30)
        self.user_data_dir = Path("Platinum_Tier/browser_data/whatsapp")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_messages = set()
        self.urgent_keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 'important']
        self.agentic_keywords = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt']
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
            viewport={'width': 1280, 'height': 720}
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

        # Navigate to WhatsApp Web
        self.logger.info("Opening WhatsApp Web...")
        await self.page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

        # Wait for QR code scan or existing session
        self.logger.info("Please scan QR code if needed...")
        self.logger.info("Waiting for WhatsApp to load...")

        try:
            # Wait for chat list to appear (means logged in)
            await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=120000)
            self.logger.info("Logged into WhatsApp successfully")
        except Exception as e:
            self.logger.error(f"Failed to login to WhatsApp: {e}")
            self.logger.info("Please scan QR code and restart the watcher")
            raise

    def check_for_updates(self) -> list:
        """Check WhatsApp for new urgent messages"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async version of check_for_updates"""
        if not self.page:
            await self.initialize_browser()

        try:
            # Refresh to get latest messages
            await self.page.reload(wait_until="domcontentloaded")
            await self.page.wait_for_timeout(3000)

            # Find unread chats
            unread_chats = await self.page.query_selector_all('[aria-label*="unread"]')
            new_messages = []

            for chat in unread_chats[:10]:
                try:
                    # Get chat name
                    name_elem = await chat.query_selector('[dir="auto"]')
                    name = await name_elem.inner_text() if name_elem else "Unknown"

                    # Get message preview
                    message_elem = await chat.query_selector('.matched-text')
                    if not message_elem:
                        message_elem = await chat.query_selector('[dir="ltr"]')

                    message = await message_elem.inner_text() if message_elem else ""

                    # Create unique ID
                    message_id = f"{name}_{message[:30]}_{datetime.now().strftime('%H%M%S')}"

                    if message_id not in self.seen_messages:
                        # Check if message contains urgent or agentic keywords
                        text_lower = f"{name} {message}".lower()
                        is_urgent = any(kw in text_lower for kw in self.urgent_keywords)
                        is_agentic = any(kw in text_lower for kw in self.agentic_keywords)

                        if is_urgent or is_agentic:
                            new_messages.append({
                                'name': name.strip(),
                                'message': message.strip(),
                                'message_id': message_id,
                                'is_urgent': is_urgent,
                                'is_agentic': is_agentic,
                                'timestamp': datetime.now().isoformat()
                            })
                            self.seen_messages.add(message_id)

                            if is_urgent:
                                self.logger.info(f"Found URGENT message from: {name[:30]}")
                            if is_agentic:
                                self.logger.info(f"Found Agentic AI message from: {name[:30]}")

                except Exception as e:
                    self.logger.warning(f"Error parsing chat: {e}")
                    continue

            return new_messages

        except Exception as e:
            self.logger.error(f"Error checking WhatsApp: {e}")
            return []

    def create_action_file(self, msg) -> Path:
        """Create action file in Needs_Action/ folder with proper format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = msg['name'].replace(' ', '_').replace(':', '')[:30]

        # Determine priority
        if msg['is_urgent']:
            priority = 'high'
        elif msg['is_agentic']:
            priority = 'medium'
        else:
            priority = 'low'

        # Determine category
        category = []
        if msg['is_urgent']:
            category.append('urgent')
        if msg['is_agentic']:
            category.append('agentic_ai')

        # Create action file content with frontmatter
        content = f"""---
type: whatsapp_message
from: {msg['name']}
message_id: {msg['message_id']}
received: {msg['timestamp']}
priority: {priority}
status: pending
category: {', '.join(category)}
---

## Message Content
{msg['message']}

## Suggested Actions
- [ ] Read full conversation
- [ ] Draft reply
- [ ] Check if invoice/payment needed
- [ ] Escalate if urgent
- [ ] Send reply (requires approval)
- [ ] Mark as resolved
- [ ] Update Dashboard

## Context
This message was detected by WhatsApp watcher.

**Urgency:** {'YES - Contains urgent keywords' if msg['is_urgent'] else 'No'}
**Agentic AI Related:** {'YES - Contains Agentic AI keywords' if msg['is_agentic'] else 'No'}

Urgent keywords matched: {', '.join([kw for kw in self.urgent_keywords if kw in f"{msg['name']} {msg['message']}".lower()])}
Agentic keywords matched: {', '.join([kw for kw in self.agentic_keywords if kw in f"{msg['name']} {msg['message']}".lower()])}

## Response Guidelines
1. If urgent: Respond within 1 hour
2. If invoice/payment: Check Company_Handbook.md for approval rules
3. If Agentic AI question: Provide detailed technical response
4. Always be professional and helpful
"""

        # Save to Needs_Action folder
        filename = f"WHATSAPP_{timestamp}_{safe_name}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")

        # Also save to Inbox for reference
        inbox_content = f"""From: {msg['name']}
Date: {msg['timestamp']}
Priority: {priority}
Category: {', '.join(category)}

{msg['message']}
"""
        self.save_to_inbox(msg, f"WHATSAPP_{timestamp}_{safe_name}.txt", inbox_content)

        return filepath

def main():
    """Main entry point"""
    load_dotenv()

    # Vault path
    vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    watcher = WhatsAppWatcherHackathon(vault_path=str(vault_path))

    print("=" * 70)
    print("WhatsApp Watcher - Hackathon Compliant")
    print("=" * 70)
    print(f"Vault: {vault_path}")
    print(f"Needs_Action: {vault_path / 'Needs_Action'}")
    print(f"Check interval: 30 seconds")
    print()
    print("IMPORTANT: Please scan QR code in the browser window")
    print("Your session will be saved for future runs")
    print("=" * 70)
    print()

    watcher.run()

if __name__ == "__main__":
    main()
