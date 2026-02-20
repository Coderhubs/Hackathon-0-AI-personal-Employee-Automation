"""
Gmail Approval Handler
Watches Approved folder and sends emails automatically
"""
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from gmail_sender_smtp import GmailSender
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(Path(__file__).parent.parent / '.env')

class ApprovalHandler(FileSystemEventHandler):
    def __init__(self, sender):
        self.sender = sender
        self.logger = logging.getLogger('ApprovalHandler')
        self.processed_files = set()

    def on_created(self, event):
        """Handle new files in Approved folder"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process .md files
        if file_path.suffix != '.md':
            return

        # Skip if already processed
        if str(file_path) in self.processed_files:
            return

        # Wait a moment for file to be fully written
        time.sleep(1)

        self.logger.info(f"New approved file detected: {file_path.name}")

        # Send email
        result = self.sender.send_from_approved_file(file_path)

        if result['success']:
            self.logger.info(f"[SUCCESS] Email sent from {file_path.name}")
            self.processed_files.add(str(file_path))
        else:
            self.logger.error(f"[FAILED] {result.get('error', 'Unknown error')}")

def main():
    """Main entry point"""
    # Setup logging
    log_dir = Path("../AI_Employee_Vault/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'gmail_approval_handler.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('ApprovalHandler')

    # Get credentials
    email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")

    if not email or not password:
        logger.error("GMAIL_EMAIL or GMAIL_PASSWORD not found in .env")
        return

    # Create sender
    sender = GmailSender(email, password)

    # Setup folder watching
    approved_dir = Path("../AI_Employee_Vault/Approved")
    approved_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 80)
    logger.info("GMAIL APPROVAL HANDLER - AUTOMATIC EMAIL SENDING")
    logger.info("=" * 80)
    logger.info(f"Email: {email}")
    logger.info(f"Watching: {approved_dir.absolute()}")
    logger.info("=" * 80)
    logger.info("")
    logger.info("[OK] Monitoring Approved folder for emails to send...")
    logger.info("")

    # Create event handler and observer
    event_handler = ApprovalHandler(sender)
    observer = Observer()
    observer.schedule(event_handler, str(approved_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("\n[STOP] Approval handler stopped by user")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
