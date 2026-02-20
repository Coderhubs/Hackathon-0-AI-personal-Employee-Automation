"""
Real Gmail Watcher using Playwright
Automates browser to login and fetch real emails
"""
import os
import time
import asyncio
from datetime import datetime
from pathlib import Path
import logging
from playwright.async_api import async_playwright
import json

class GmailWatcherPlaywright:
    def __init__(self, email, password, check_interval=180):
        self.email = email
        self.password = password
        self.check_interval = check_interval  # seconds
        self.inbox_dir = Path("Inbox")
        self.inbox_dir.mkdir(exist_ok=True)
        self.user_data_dir = Path("Platinum_Tier/browser_data/gmail")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self.setup_logging()
        self.last_email_ids = set()
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
                logging.FileHandler(log_dir / 'gmail_watcher_playwright.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('GmailWatcherPlaywright')

    async def login_to_gmail(self, page):
        """Login to Gmail - checks for existing session first"""
        try:
            self.logger.info("Navigating to Gmail...")
            await page.goto("https://mail.google.com/", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            # Check if already logged in (persistent session)
            try:
                inbox_check = await page.query_selector('[role="main"]')
                if inbox_check:
                    self.logger.info("✓ Already logged in via persistent session!")
                    return True
            except:
                pass

            # Not logged in - proceed with login
            self.logger.info("No active session found. Logging in...")

            # Enter email
            self.logger.info("Entering email...")
            email_input = await page.wait_for_selector('input[type="email"]', timeout=10000)
            await email_input.fill(self.email)
            await page.wait_for_timeout(1000)

            next_button = await page.query_selector('button:has-text("Next")')
            if next_button:
                await next_button.click()
            await page.wait_for_timeout(5000)

            # Enter password - wait longer and handle different scenarios
            self.logger.info("Waiting for password field...")
            try:
                # Wait for password input to appear
                await page.wait_for_selector('input[type="password"]', state='visible', timeout=15000)
                await page.wait_for_timeout(2000)

                # Type password slowly to avoid detection
                self.logger.info("Entering password...")
                await page.type('input[type="password"]', self.password, delay=100)
                await page.wait_for_timeout(2000)

                # Click Next button
                next_button = await page.query_selector('button:has-text("Next")')
                if next_button:
                    await next_button.click()
                await page.wait_for_timeout(8000)

            except Exception as e:
                self.logger.warning(f"Password entry issue: {e}")
                self.logger.info("You may need to complete verification manually in the browser...")
                await page.wait_for_timeout(30000)  # Wait 30 seconds for manual intervention

            # Wait for inbox to load
            self.logger.info("Waiting for inbox to load...")
            await page.wait_for_selector('[role="main"]', timeout=45000)
            self.logger.info("Successfully logged into Gmail!")
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            self.logger.info("Browser will stay open for 30 seconds for manual login if needed...")
            await page.wait_for_timeout(30000)
            return False

    async def fetch_emails(self, page):
        """Fetch recent emails from inbox, filter for Agentic AI content"""
        try:
            # Get email rows
            email_rows = await page.query_selector_all('tr.zA')

            new_emails = []
            for row in email_rows[:10]:  # Check top 10 emails
                try:
                    # Extract email data
                    sender_elem = await row.query_selector('.yW span')
                    subject_elem = await row.query_selector('.y6 span')
                    snippet_elem = await row.query_selector('.y2')

                    sender = await sender_elem.inner_text() if sender_elem else "Unknown"
                    subject = await subject_elem.inner_text() if subject_elem else "No Subject"
                    snippet = await snippet_elem.inner_text() if snippet_elem else ""

                    # Create unique ID
                    email_id = f"{sender}_{subject}_{snippet[:20]}"

                    # Filter for Agentic AI content
                    text_to_check = f"{subject} {snippet}".lower()
                    is_agentic_ai = any(keyword in text_to_check for keyword in self.agentic_keywords)

                    if email_id not in self.last_email_ids and is_agentic_ai:
                        new_emails.append({
                            'sender': sender,
                            'subject': subject,
                            'snippet': snippet,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.last_email_ids.add(email_id)
                        self.logger.info(f"📧 Agentic AI email: {subject[:50]}")

                except Exception as e:
                    self.logger.warning(f"Error parsing email row: {e}")
                    continue

            return new_emails

        except Exception as e:
            self.logger.error(f"Error fetching emails: {e}")
            return []

    def save_email_to_file(self, email_data):
        """Save email to Inbox folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subject = email_data['subject'].replace(' ', '_').replace(':', '').replace('/', '_')[:50]
        filename = f"GMAIL_AGENTIC_{timestamp}_{safe_subject}.txt"
        filepath = self.inbox_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Subject: {email_data['subject']}\n")
            f.write(f"From: {email_data['sender']}\n")
            f.write(f"Date: {email_data['timestamp']}\n")
            f.write(f"Category: Agentic AI\n")
            f.write("-" * 40 + "\n")
            f.write(email_data['snippet'])

        self.logger.info(f"Saved email: {filepath}")

    async def send_email(self, page, to_email, subject, body):
        """Send an email about Agentic AI"""
        try:
            self.logger.info(f"Composing email to {to_email}...")

            # Click compose button
            compose_btn = await page.query_selector('div[role="button"][gh="cm"]')
            if not compose_btn:
                # Try alternative selector
                compose_btn = await page.query_selector('div.T-I.T-I-KE')

            if compose_btn:
                await compose_btn.click()
                await page.wait_for_timeout(2000)
            else:
                self.logger.error("Could not find compose button")
                return False

            # Fill recipient
            to_field = await page.query_selector('input[aria-label*="To"]')
            if not to_field:
                to_field = await page.query_selector('textarea[name="to"]')

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
            if not body_field:
                body_field = await page.query_selector('div[role="textbox"]')

            if body_field:
                await body_field.fill(body)
                await page.wait_for_timeout(1000)

            # Send email
            send_btn = await page.query_selector('div[role="button"][aria-label*="Send"]')
            if not send_btn:
                send_btn = await page.query_selector('div.T-I.J-J5-Ji')

            if send_btn:
                await send_btn.click()
                await page.wait_for_timeout(2000)
                self.logger.info(f"✓ Email sent to {to_email}")
                return True
            else:
                self.logger.error("Could not find send button")
                return False

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    async def run(self, send_demo_email=False):
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
                viewport={'width': 1280, 'height': 720}
            )
            page = context.pages[0] if context.pages else await context.new_page()

            # Login
            if not await self.login_to_gmail(page):
                self.logger.error("Failed to login. Exiting.")
                await browser.close()
                return

            # Send demo email if requested
            if send_demo_email:
                demo_subject = f"Agentic AI Technology Update - {datetime.now().strftime('%Y-%m-%d')}"
                demo_body = f"""Hello,

This is an automated update about Agentic AI technology for {datetime.now().strftime('%B %d, %Y')}.

🤖 Key Developments in Agentic AI:
• Autonomous agents are becoming more capable with improved reasoning
• Multi-agent systems are solving complex real-world problems
• Integration of LLMs with tool use is enabling new applications
• Claude, GPT-4, and other models are powering intelligent agents

📊 Today's Focus Areas:
- Tool-using AI agents for automation
- Collaborative multi-agent workflows
- Real-time decision making systems
- Agentic AI in enterprise applications

This email was sent by an automated Gmail watcher monitoring Agentic AI developments.

Best regards,
AI Personal Employee System"""

                self.logger.info("Sending demo email about Agentic AI...")
                await self.send_email(page, self.email, demo_subject, demo_body)

            # Main monitoring loop
            retry_count = 0
            max_retries = 5

            self.logger.info("Starting monitoring for Agentic AI emails...")
            while True:
                try:
                    self.logger.info("Checking for new Agentic AI emails...")
                    new_emails = await self.fetch_emails(page)

                    if new_emails:
                        self.logger.info(f"Found {len(new_emails)} new Agentic AI email(s)")
                        for email in new_emails:
                            self.save_email_to_file(email)
                    else:
                        self.logger.info("No new Agentic AI emails")

                    retry_count = 0  # Reset on success
                    await asyncio.sleep(self.check_interval)

                except KeyboardInterrupt:
                    self.logger.info("Gmail Watcher stopped by user.")
                    break

                except Exception as e:
                    retry_count += 1
                    self.logger.error(f"Error in Gmail Watcher: {e}")

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
                            viewport={'width': 1280, 'height': 720}
                        )
                        page = await context.new_page()
                        await self.login_to_gmail(page)
                        retry_count = 0

            await browser.close()

def main():
    """Main entry point"""
    # Load credentials from environment
    from dotenv import load_dotenv
    load_dotenv()

    email = os.getenv('GMAIL_EMAIL')
    password = os.getenv('GMAIL_PASSWORD')

    if not email or not password:
        print("ERROR: Please set GMAIL_EMAIL and GMAIL_PASSWORD in .env file")
        return

    watcher = GmailWatcherPlaywright(
        email=email,
        password=password,
        check_interval=180  # Check every 3 minutes
    )

    # Set send_demo_email=True to test email sending
    asyncio.run(watcher.run(send_demo_email=True))

if __name__ == "__main__":
    main()
