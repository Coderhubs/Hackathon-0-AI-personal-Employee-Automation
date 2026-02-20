"""
Gmail Watcher with Persistent Session - Login once manually, then auto-monitor
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from datetime import datetime
import json

class GmailWatcherPersistent:
    def __init__(self, email, password, check_interval=180):
        self.email = email
        self.password = password
        self.check_interval = check_interval
        self.inbox_dir = Path("Inbox")
        self.inbox_dir.mkdir(exist_ok=True)
        self.user_data_dir = Path("Platinum_Tier/browser_data/gmail")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.seen_emails = set()
        self.agentic_keywords = ['agentic', 'ai agent', 'autonomous ai', 'llm', 'claude', 'gpt', 'artificial intelligence', 'machine learning']

    async def check_inbox(self, page):
        """Check for new emails about Agentic AI"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking inbox...")

        try:
            await page.goto("https://mail.google.com/mail/u/0/#inbox", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            email_rows = await page.query_selector_all('tr.zA')
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
                            'sender': sender,
                            'subject': subject,
                            'snippet': snippet,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.seen_emails.add(email_id)
                        print(f"  📧 Agentic AI email: {subject[:50]}")

                        # Save to file
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_subject = subject.replace(' ', '_').replace(':', '').replace('/', '_')[:50]
                        filename = f"GMAIL_AGENTIC_{timestamp}_{safe_subject}.txt"
                        filepath = self.inbox_dir / filename

                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"Subject: {subject}\n")
                            f.write(f"From: {sender}\n")
                            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Category: Agentic AI\n")
                            f.write("-" * 40 + "\n")
                            f.write(snippet)

                        print(f"  Saved: {filename}")

                except:
                    pass

            if not new_emails:
                print(f"  No new Agentic AI emails")

            return new_emails

        except Exception as e:
            print(f"  Error checking inbox: {e}")
            return []

    async def send_email(self, page, to_email, subject, body):
        """Send an email about Agentic AI"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Composing email to {to_email}...")

        try:
            await page.goto("https://mail.google.com/mail/u/0/#inbox", wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Click compose
            compose_btn = await page.query_selector('div[role="button"][gh="cm"]')
            if compose_btn:
                await compose_btn.click()
                await page.wait_for_timeout(2000)

            # Fill recipient
            to_field = await page.query_selector('input[aria-label*="To"]')
            if to_field:
                await to_field.fill(to_email)
                await page.wait_for_timeout(500)

            # Fill subject
            subject_field = await page.query_selector('input[name="subjectbox"]')
            if subject_field:
                await subject_field.fill(subject)
                await page.wait_for_timeout(500)

            # Fill body
            body_field = await page.query_selector('div[aria-label="Message Body"]')
            if body_field:
                await body_field.fill(body)
                await page.wait_for_timeout(1000)

            # Send
            send_btn = await page.query_selector('div[role="button"][aria-label*="Send"]')
            if send_btn:
                await send_btn.click()
                await page.wait_for_timeout(2000)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Email sent to {to_email}")
                return True

        except Exception as e:
            print(f"  Error sending email: {e}")
            return False

    async def run(self, send_demo_email=False):
        """Main run loop with persistent session"""
        print("=" * 70)
        print("Gmail Watcher - Agentic AI Monitor")
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
                viewport={'width': 1280, 'height': 720}
            )

            page = context.pages[0] if context.pages else await context.new_page()

            try:
                # Navigate to Gmail
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening Gmail...")
                await page.goto("https://mail.google.com/", wait_until="domcontentloaded")
                await page.wait_for_timeout(5000)

                # Check if already logged in
                if await page.query_selector('input[type="email"]'):
                    print("\n[!] Please login manually in the browser window.")
                    print("    Your session will be saved for future runs.")
                    print("    Waiting 60 seconds for you to complete login...\n")
                    await page.wait_for_timeout(60000)

                # Wait for inbox
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for inbox...")
                await page.wait_for_selector('[role="main"]', timeout=30000)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Logged in successfully!\n")

                # Send demo email if requested
                if send_demo_email:
                    demo_subject = f"Agentic AI Technology Update - {datetime.now().strftime('%Y-%m-%d')}"
                    demo_body = f"""Hello,

This is an automated update about Agentic AI technology for {datetime.now().strftime('%B %d, %Y')}.

🤖 Key Developments in Agentic AI:
• Autonomous agents with improved reasoning capabilities
• Multi-agent systems solving complex real-world problems
• Integration of LLMs with tool use enabling new applications
• Claude, GPT-4, and other models powering intelligent agents

📊 Today's Focus Areas:
- Tool-using AI agents for automation
- Collaborative multi-agent workflows
- Real-time decision making systems
- Agentic AI in enterprise applications

This email was sent by an automated Gmail watcher monitoring Agentic AI developments.

Best regards,
AI Personal Employee System"""

                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending demo email...")
                    await self.send_email(page, self.email, demo_subject, demo_body)
                    print()

                # Main monitoring loop
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting monitoring loop...")
                print("Press Ctrl+C to stop\n")

                while True:
                    await self.check_inbox(page)
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

    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')

    if not email or not password:
        print("ERROR: Please set GMAIL_EMAIL and GMAIL_PASSWORD in .env file")
        return

    watcher = GmailWatcherPersistent(
        email=email,
        password=password,
        check_interval=180
    )

    # Set send_demo_email=True to test email sending
    asyncio.run(watcher.run(send_demo_email=True))

if __name__ == "__main__":
    main()
