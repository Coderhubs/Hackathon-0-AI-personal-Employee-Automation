"""
FULLY AUTOMATED Gmail Watcher using IMAP
NO browser, NO manual login, NO 2FA issues
Uses Gmail App Password for 24/7 autonomous operation
"""
import os
import imaplib
import email
from email.header import decode_header
import time
from datetime import datetime
from pathlib import Path
import logging
import json
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(Path(__file__).parent.parent / '.env')

class GmailWatcherIMAP:
    def __init__(self, email_address, app_password, check_interval=180):
        self.email_address = email_address
        self.app_password = app_password
        self.check_interval = check_interval  # seconds
        self.inbox_dir = Path("../AI_Employee_Vault/Needs_Action")
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self.setup_logging()
        self.processed_ids = self.load_processed_ids()

        # Keywords for Agentic AI filtering
        self.agentic_keywords = [
            'agentic', 'ai agent', 'autonomous ai', 'llm', 'claude',
            'gpt', 'artificial intelligence', 'machine learning', 'automation'
        ]

    def setup_logging(self):
        """Setup logging"""
        log_dir = Path("../AI_Employee_Vault/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'gmail_watcher_imap.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('GmailWatcherIMAP')

    def load_processed_ids(self):
        """Load previously processed email IDs"""
        cache_file = Path("../AI_Employee_Vault/Logs/processed_emails.json")
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def save_processed_ids(self):
        """Save processed email IDs"""
        cache_file = Path("../AI_Employee_Vault/Logs/processed_emails.json")
        with open(cache_file, 'w') as f:
            json.dump(list(self.processed_ids), f)

    def connect_to_gmail(self):
        """Connect to Gmail via IMAP - FULLY AUTOMATED"""
        try:
            self.logger.info("Connecting to Gmail IMAP server...")
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_address, self.app_password)
            self.logger.info("[OK] Connected to Gmail successfully!")
            return mail
        except Exception as e:
            self.logger.error(f"Failed to connect to Gmail: {e}")
            self.logger.error("Make sure you're using Gmail App Password, not regular password")
            self.logger.error("Generate one at: https://myaccount.google.com/apppasswords")
            return None

    def decode_email_subject(self, subject):
        """Decode email subject"""
        if subject is None:
            return "No Subject"

        decoded_parts = decode_header(subject)
        decoded_subject = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_subject += part.decode(encoding or 'utf-8')
                except:
                    decoded_subject += part.decode('utf-8', errors='ignore')
            else:
                decoded_subject += part

        return decoded_subject

    def extract_email_body(self, msg):
        """Extract email body text"""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())

        return body

    def contains_agentic_keywords(self, text):
        """Check if text contains agentic AI keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.agentic_keywords)

    def save_email_to_file(self, email_data):
        """Save email to Needs_Action folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize sender name for filename (remove invalid characters)
        sender_safe = email_data['from'][:30]
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '@']:
            sender_safe = sender_safe.replace(char, '_')
        filename = f"EMAIL_{timestamp}_{sender_safe}.md"
        filepath = self.inbox_dir / filename

        content = f"""---
type: email
from: {email_data['from']}
subject: {email_data['subject']}
date: {email_data['date']}
message_id: {email_data['message_id']}
status: needs_action
created: {datetime.now().isoformat()}
---

# Email from {email_data['from']}

## Subject
{email_data['subject']}

## Date
{email_data['date']}

## Body
{email_data['body']}

---
**Action Required:** Review and draft response
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"[SAVED] {filename}")
        return filepath

    def fetch_new_emails(self):
        """Fetch new emails - FULLY AUTOMATED"""
        mail = self.connect_to_gmail()
        if not mail:
            return []

        try:
            # Select inbox
            mail.select("INBOX")

            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')

            if status != "OK":
                self.logger.warning("No new emails found")
                return []

            email_ids = messages[0].split()
            new_emails = []

            self.logger.info(f"Found {len(email_ids)} unread email(s)")

            for email_id in email_ids:
                email_id_str = email_id.decode()

                # Skip if already processed
                if email_id_str in self.processed_ids:
                    continue

                # Fetch email
                status, msg_data = mail.fetch(email_id, "(RFC822)")

                if status != "OK":
                    continue

                # Parse email
                msg = email.message_from_bytes(msg_data[0][1])

                # Extract email data
                subject = self.decode_email_subject(msg.get("Subject"))
                from_addr = msg.get("From")
                date = msg.get("Date")
                body = self.extract_email_body(msg)

                # Check for agentic AI keywords (set to False to monitor ALL emails)
                filter_by_keywords = False  # Change to True to only detect AI-related emails

                if not filter_by_keywords or self.contains_agentic_keywords(subject + " " + body):
                    email_data = {
                        'from': from_addr,
                        'subject': subject,
                        'date': date,
                        'body': body,
                        'message_id': email_id_str
                    }

                    # Save to file
                    self.save_email_to_file(email_data)
                    new_emails.append(email_data)

                    keyword_tag = "[AGENTIC AI]" if self.contains_agentic_keywords(subject + " " + body) else "[ALL EMAILS]"
                    self.logger.info(f"{keyword_tag} Email from {from_addr}: {subject}")

                # Mark as processed
                self.processed_ids.add(email_id_str)

            # Save processed IDs
            self.save_processed_ids()

            # Logout
            mail.logout()

            return new_emails

        except Exception as e:
            self.logger.error(f"Error fetching emails: {e}")
            try:
                mail.logout()
            except:
                pass
            return []

    def run(self):
        """Run the watcher - FULLY AUTOMATED 24/7"""
        self.logger.info("=" * 80)
        self.logger.info("GMAIL WATCHER - FULLY AUTOMATED (IMAP)")
        self.logger.info("=" * 80)
        self.logger.info(f"Email: {self.email_address}")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info(f"Output directory: {self.inbox_dir}")
        self.logger.info("=" * 80)
        self.logger.info("")
        self.logger.info("[OK] Starting autonomous monitoring...")
        self.logger.info("[OK] NO manual login required!")
        self.logger.info("")

        while True:
            try:
                self.logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for new emails...")

                new_emails = self.fetch_new_emails()

                if new_emails:
                    self.logger.info(f"[OK] Found {len(new_emails)} new Agentic AI email(s)")
                else:
                    self.logger.info("No new Agentic AI emails")

                self.logger.info(f"Waiting {self.check_interval} seconds until next check...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\n[STOP] Watcher stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.info("Retrying in 60 seconds...")
                time.sleep(60)

def main():
    """Main entry point"""
    email_address = os.getenv("GMAIL_EMAIL")
    app_password = os.getenv("GMAIL_PASSWORD")

    if not email_address or not app_password:
        print("ERROR: GMAIL_EMAIL and GMAIL_PASSWORD must be set in .env file")
        print("Use Gmail App Password, not regular password")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        return

    watcher = GmailWatcherIMAP(email_address, app_password)
    watcher.run()

if __name__ == "__main__":
    main()
