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
        self.logger = self.setup_logging()
        self.last_email_ids = set()

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
        """Login to Gmail"""
        try:
            self.logger.info("Navigating to Gmail...")
            await page.goto("https://mail.google.com/", wait_until="networkidle")

            # Enter email
            self.logger.info("Entering email...")
            await page.fill('input[type="email"]', self.email)
            await page.click('button:has-text("Next")')
            await page.wait_for_timeout(2000)

            # Enter password
            self.logger.info("Entering password...")
            await page.fill('input[type="password"]', self.password)
            await page.click('button:has-text("Next")')
            await page.wait_for_timeout(5000)

            # Wait for inbox to load
            self.logger.info("Waiting for inbox to load...")
            await page.wait_for_selector('[role="main"]', timeout=30000)
            self.logger.info("Successfully logged into Gmail!")
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False

    async def fetch_emails(self, page):
        """Fetch recent emails from inbox"""
        try:
            # Get email rows
            email_rows = await page.query_selector_all('tr.zA')

            new_emails = []
            for row in email_rows[:5]:  # Get top 5 emails
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

                    if email_id not in self.last_email_ids:
                        new_emails.append({
                            'sender': sender,
                            'subject': subject,
                            'snippet': snippet,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        self.last_email_ids.add(email_id)

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
        filename = f"GMAIL_{timestamp}_{safe_subject}.txt"
        filepath = self.inbox_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Subject: {email_data['subject']}\n")
            f.write(f"From: {email_data['sender']}\n")
            f.write(f"Date: {email_data['timestamp']}\n")
            f.write("-" * 40 + "\n")
            f.write(email_data['snippet'])

        self.logger.info(f"Saved email: {filepath}")

    async def run(self):
        """Main run loop"""
        async with async_playwright() as p:
            # Launch browser (headless=False to see what's happening)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Login
            if not await self.login_to_gmail(page):
                self.logger.error("Failed to login. Exiting.")
                await browser.close()
                return

            # Main monitoring loop
            retry_count = 0
            max_retries = 5

            while True:
                try:
                    self.logger.info("Checking for new emails...")
                    new_emails = await self.fetch_emails(page)

                    if new_emails:
                        self.logger.info(f"Found {len(new_emails)} new email(s)")
                        for email in new_emails:
                            self.save_email_to_file(email)
                    else:
                        self.logger.info("No new emails")

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
                        browser = await p.chromium.launch(headless=False)
                        context = await browser.new_context()
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

    asyncio.run(watcher.run())

if __name__ == "__main__":
    main()
