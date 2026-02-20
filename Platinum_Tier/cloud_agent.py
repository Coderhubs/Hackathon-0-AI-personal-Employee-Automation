#!/usr/bin/env python3
"""
Cloud Agent - Runs 24/7 monitoring
Lightweight agent for cloud deployment
"""

import os
import time
import imaplib
import email
from pathlib import Path
from datetime import datetime
import logging

class CloudAgent:
    """
    Cloud agent for 24/7 monitoring.

    Responsibilities:
    - Monitor Gmail via IMAP (no browser needed)
    - Create action files in vault
    - Lightweight and efficient
    """

    def __init__(self):
        self.vault_path = Path(os.getenv('VAULT_PATH', '/vault'))
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Gmail credentials
        self.gmail_email = os.getenv('GMAIL_EMAIL', '')
        self.gmail_password = os.getenv('GMAIL_PASSWORD', '')

        # Setup logging
        self.setup_logging()

        # Track processed emails
        self.processed_emails = set()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / 'cloud_agent.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CloudAgent')

    def check_gmail(self):
        """Check Gmail for new emails via IMAP"""
        try:
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.gmail_email, self.gmail_password)
            mail.select('inbox')

            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')

            if status != 'OK':
                self.logger.error("Failed to search emails")
                return

            email_ids = messages[0].split()
            self.logger.info(f"Found {len(email_ids)} unread emails")

            for email_id in email_ids[:10]:  # Process max 10 at a time
                if email_id in self.processed_emails:
                    continue

                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')

                if status != 'OK':
                    continue

                # Parse email
                msg = email.message_from_bytes(msg_data[0][1])

                subject = msg['subject']
                from_addr = msg['from']
                date = msg['date']

                # Get email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                # Create action file
                self.create_action_file({
                    'type': 'email',
                    'from': from_addr,
                    'subject': subject,
                    'date': date,
                    'body': body[:500]  # First 500 chars
                })

                self.processed_emails.add(email_id)

            mail.close()
            mail.logout()

        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")

    def create_action_file(self, data):
        """Create action file in vault"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        content = f"""---
type: {data['type']}
from: {data['from']}
subject: {data['subject']}
received: {data['date']}
priority: high
status: pending
source: cloud_agent
---

## Email from Cloud Agent

**From:** {data['from']}
**Subject:** {data['subject']}
**Date:** {data['date']}

**Body Preview:**
{data['body']}

## Suggested Actions
- [ ] Review email content
- [ ] Draft reply (requires local approval)
- [ ] Mark as handled

## Context
This email was detected by the cloud agent running 24/7.
"""

        filename = f"CLOUD_EMAIL_{timestamp}.md"
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')

        self.logger.info(f"Created action file: {filename}")

    def run(self):
        """Main run loop"""
        self.logger.info("Cloud Agent started - Running 24/7")
        self.logger.info(f"Vault path: {self.vault_path}")

        while True:
            try:
                self.logger.info("Checking Gmail...")
                self.check_gmail()

                # Update status file
                status_file = self.vault_path / 'cloud_status.txt'
                status_file.write_text(f"Last check: {datetime.now().isoformat()}\n")

            except KeyboardInterrupt:
                self.logger.info("Cloud Agent stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")

            # Wait 5 minutes before next check
            time.sleep(300)

if __name__ == "__main__":
    agent = CloudAgent()
    agent.run()
