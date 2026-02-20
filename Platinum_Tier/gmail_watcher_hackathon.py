"""
Gmail Watcher - Hackathon Compliant
Monitors Gmail and writes to Needs_Action/ folder
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio
from base_watcher import BaseWatcher

class GmailWatcherHackathon(BaseWatcher):
    def __init__(self, vault_path: str, email: str, password: str):
        super().__init__(vault_path, check_interval=180)
        self.email = email
        self.password = password
        self.user_data_dir = Path("Platinum_Tier/browser_data/gmail")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_emails = set()
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
            viewport={'width': 1280, 'height': 720}
        )

        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()

        # Navigate to Gmail
        self.logger.info("Opening Gmail...")
        await self.page.goto("https://mail.google.com/", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(5000)

        # Check if login needed
        if await self.page.query_selector('input[type="email"]'):
            self.logger.info("Please login manually in the browser window")
            self.logger.info("Waiting 60 seconds for login...")
            await self.page.wait_for_timeout(60000)

        # Wait for inbox
        await self.page.wait_for_selector('[role="main"]', timeout=30000)
        self.logger.info("Logged into Gmail successfully")

    def check_for_updates(self) -> list:
        """Check Gmail inbox for new Agentic AI emails"""
        return asyncio.run(self._async_check_for_updates())

    async def _async_check_for_updates(self) -> list:
        """Async version of check_for_updates"""
        if not self.page:
            await self.initialize_browser()

        try:
            await self.page.goto("https://mail.google.com/mail/u/0/#inbox", wait_until="domcontentloaded")
            await self.page.wait_for_timeout(3000)

            email_rows = await self.page.query_selector_all('tr.zA')
            new_emails = []

            for row in email_rows[:10]:
                try:
                    sender_elem = await row.query_selector('.yW span')
                    subject_elem = await row.query_selector('.y6 span')
                    snippet_elem = await row.query_selector('.y2')

                    sender = await sender_elem.inner_text() if sender_elem else "Unknown"
                    subject = await subject_elem.inner_text() if subject_elem else "No Subject"
                    snippet = await snippet_elem.inner_text() if snippet_elem else ""

                    email_id = f"{sender}_{subject}_{snippet[:20]}"
                    text_to_check = f"{subject} {snippet}".lower()
                    is_agentic_ai = any(keyword in text_to_check for keyword in self.agentic_keywords)

                    if email_id not in self.seen_emails and is_agentic_ai:
                        new_emails.append({
                            'sender': sender.strip(),
                            'subject': subject.strip(),
                            'snippet': snippet.strip(),
                            'email_id': email_id,
                            'timestamp': datetime.now().isoformat()
                        })
                        self.seen_emails.add(email_id)
                        self.logger.info(f"Found Agentic AI email: {subject[:50]}")

                except Exception as e:
                    self.logger.warning(f"Error parsing email row: {e}")
                    continue

            return new_emails

        except Exception as e:
            self.logger.error(f"Error checking inbox: {e}")
            return []

    def create_action_file(self, email) -> Path:
        """Create action file in Needs_Action/ folder with proper format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subject = email['subject'].replace(' ', '_').replace(':', '').replace('/', '_')[:50]

        # Determine priority based on keywords
        priority = 'high' if any(kw in email['subject'].lower() for kw in ['urgent', 'asap', 'important']) else 'medium'

        # Create action file content with frontmatter
        content = f"""---
type: email
from: {email['sender']}
subject: {email['subject']}
received: {email['timestamp']}
priority: {priority}
status: pending
keywords: agentic_ai
---

## Email Content
{email['snippet']}

## Suggested Actions
- [ ] Read full email content
- [ ] Draft reply about Agentic AI
- [ ] Research relevant information
- [ ] Send reply (requires approval)
- [ ] Archive after processing
- [ ] Update Dashboard

## Context
This email was detected by Gmail watcher because it contains Agentic AI keywords.
Keywords matched: {', '.join([kw for kw in self.agentic_keywords if kw in f"{email['subject']} {email['snippet']}".lower()])}
"""

        # Save to Needs_Action folder
        filename = f"EMAIL_{timestamp}_{safe_subject}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")

        # Also save to Inbox for reference
        inbox_content = f"""Subject: {email['subject']}
From: {email['sender']}
Date: {email['timestamp']}
Category: Agentic AI

{email['snippet']}
"""
        self.save_to_inbox(email, f"GMAIL_AGENTIC_{timestamp}_{safe_subject}.txt", inbox_content)

        return filepath

def main():
    """Main entry point"""
    load_dotenv()

    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')

    if not email or not password:
        print("ERROR: Please set GMAIL_EMAIL and GMAIL_PASSWORD in .env file")
        return

    # Vault path
    vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"

    watcher = GmailWatcherHackathon(
        vault_path=str(vault_path),
        email=email,
        password=password
    )

    print("=" * 70)
    print("Gmail Watcher - Hackathon Compliant")
    print("=" * 70)
    print(f"Email: {email}")
    print(f"Vault: {vault_path}")
    print(f"Needs_Action: {vault_path / 'Needs_Action'}")
    print(f"Check interval: 180 seconds (3 minutes)")
    print("=" * 70)
    print()

    watcher.run()

if __name__ == "__main__":
    main()
