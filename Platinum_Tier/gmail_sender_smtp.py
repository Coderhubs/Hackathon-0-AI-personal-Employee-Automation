"""
Gmail SMTP Email Sender
Sends emails using Gmail App Password
Works with the approval workflow
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(Path(__file__).parent.parent / '.env')

class GmailSender:
    def __init__(self, email_address, app_password):
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.logger = self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_dir = Path("../AI_Employee_Vault/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'gmail_sender.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('GmailSender')

    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        """
        Send email via Gmail SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)

        Returns:
            dict: Success status and message
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = cc
            if bcc:
                msg['Bcc'] = bcc

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Connect to Gmail SMTP
            self.logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

            # Login
            self.logger.info("Logging in...")
            server.login(self.email_address, self.app_password)

            # Send email
            self.logger.info(f"Sending email to {to_email}...")
            server.send_message(msg)
            server.quit()

            self.logger.info(f"[SUCCESS] Email sent to {to_email}")

            return {
                'success': True,
                'message': f'Email sent successfully to {to_email}',
                'timestamp': datetime.now().isoformat()
            }

        except smtplib.SMTPAuthenticationError:
            self.logger.error("Authentication failed - check App Password")
            return {
                'success': False,
                'error': 'Authentication failed. Make sure you are using Gmail App Password.',
                'help': 'Generate App Password at: https://myaccount.google.com/apppasswords'
            }

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_from_approved_file(self, approved_file_path):
        """
        Send email from an approved markdown file

        Expected format:
        ---
        to: recipient@example.com
        subject: Email subject
        cc: optional@example.com
        ---

        Email body here...
        """
        try:
            approved_path = Path(approved_file_path)

            if not approved_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {approved_file_path}'
                }

            # Read file
            with open(approved_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    body = parts[2].strip()
                else:
                    return {
                        'success': False,
                        'error': 'Invalid file format - missing frontmatter'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Invalid file format - no frontmatter found'
                }

            # Extract metadata
            metadata = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            to_email = metadata.get('to', '')
            subject = metadata.get('subject', 'No Subject')
            cc = metadata.get('cc', None)
            bcc = metadata.get('bcc', None)

            if not to_email:
                return {
                    'success': False,
                    'error': 'No recipient email found in file'
                }

            # Send email
            result = self.send_email(to_email, subject, body, cc, bcc)

            if result['success']:
                # Move to Done folder
                done_dir = Path("../AI_Employee_Vault/Done")
                done_dir.mkdir(parents=True, exist_ok=True)
                done_path = done_dir / approved_path.name
                approved_path.rename(done_path)
                self.logger.info(f"Moved to Done: {done_path}")

            return result

        except Exception as e:
            self.logger.error(f"Error processing approved file: {e}")
            return {
                'success': False,
                'error': str(e)
            }

def test_connection():
    """Test Gmail SMTP connection"""
    email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        print("[ERROR] GMAIL_EMAIL or GMAIL_PASSWORD not found in .env")
        return False

    print("=" * 60)
    print("Gmail SMTP Connection Test")
    print("=" * 60)
    print(f"Email: {email}")
    print()

    sender = GmailSender(email, password)

    # Send test email to yourself
    result = sender.send_email(
        to_email=email,
        subject=f"Test Email from AI Personal Employee - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        body="""Hello!

This is a test email from your AI Personal Employee system.

If you received this, your Gmail SMTP sending is working perfectly!

Features:
- Read emails via IMAP (monitoring)
- Send emails via SMTP (replies)
- Full automation with App Password
- Human-in-the-loop approval workflow

System Status: OPERATIONAL

---
Sent by AI Personal Employee
Powered by Claude Code"""
    )

    if result['success']:
        print("[SUCCESS] Test email sent!")
        print(f"Check your inbox: {email}")
        print()
        return True
    else:
        print(f"[ERROR] {result.get('error', 'Unknown error')}")
        print()
        return False

if __name__ == "__main__":
    test_connection()
    input("\nPress Enter to exit...")
