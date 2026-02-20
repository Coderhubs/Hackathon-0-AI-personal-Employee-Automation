"""
FULLY AUTOMATED Approval Handler
Executes approved actions with ZERO manual intervention
"""
import os
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import sys

# Add Platinum_Tier to path
sys.path.insert(0, str(Path(__file__).parent / "Platinum_Tier"))

from whatsapp_client import WhatsAppClient

load_dotenv()

class AutomatedApprovalHandler:
    def __init__(self):
        self.vault_dir = Path("AI_Employee_Vault")
        self.approved_dir = self.vault_dir / "Approved"
        self.done_dir = self.vault_dir / "Done"
        self.logs_dir = self.vault_dir / "Logs"

        # Create directories
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_logging()
        self.whatsapp_client = WhatsAppClient()

        # Check interval
        self.check_interval = 10  # seconds

    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs_dir / 'approval_handler.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('ApprovalHandler')

    def parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter from markdown file"""
        if not content.startswith('---'):
            return {}

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}

            frontmatter = parts[1].strip()
            metadata = {}

            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            return metadata
        except Exception as e:
            self.logger.error(f"Error parsing frontmatter: {e}")
            return {}

    def extract_body(self, content: str) -> str:
        """Extract body content from markdown"""
        try:
            # Remove frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = parts[2]

            # Extract content after ## Body or ## Message Content or ## Post Content
            for marker in ['## Body', '## Message Content', '## Post Content', '## Draft Reply']:
                if marker in content:
                    parts = content.split(marker, 1)
                    if len(parts) > 1:
                        body = parts[1].strip()
                        # Remove any subsequent ## sections
                        if '\n##' in body:
                            body = body.split('\n##')[0].strip()
                        return body

            return content.strip()
        except Exception as e:
            self.logger.error(f"Error extracting body: {e}")
            return content

    def execute_email_action(self, filepath: Path, metadata: dict, content: str) -> bool:
        """Execute email sending via MCP server - FULLY AUTOMATED"""
        try:
            to = metadata.get('to', metadata.get('from', ''))
            subject = metadata.get('subject', 'Re: Your message')
            body = self.extract_body(content)

            self.logger.info(f"[EMAIL] Sending to {to}...")
            self.logger.info(f"[EMAIL] Subject: {subject}")

            # Call MCP email server
            result = subprocess.run(
                ['node', 'mcp_servers/email-mcp/index.js'],
                input=json.dumps({
                    'method': 'send_email',
                    'params': {
                        'to': to,
                        'subject': subject,
                        'body': body
                    }
                }),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.logger.info(f"[OK] Email sent to {to}")
                return True
            else:
                self.logger.error(f"[ERROR] Email failed: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"[ERROR] Email execution error: {e}")
            return False

    def execute_linkedin_action(self, filepath: Path, metadata: dict, content: str) -> bool:
        """Execute LinkedIn posting - FULLY AUTOMATED"""
        try:
            post_content = self.extract_body(content)

            self.logger.info(f"[LINKEDIN] Posting content...")
            self.logger.info(f"[LINKEDIN] Content preview: {post_content[:100]}...")

            # Use LinkedIn API or automation
            # For now, create a marker file that LinkedIn automation will pick up
            linkedin_queue = Path("Platinum_Tier/linkedin_queue")
            linkedin_queue.mkdir(exist_ok=True)

            queue_file = linkedin_queue / f"POST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(queue_file, 'w', encoding='utf-8') as f:
                f.write(post_content)

            self.logger.info(f"[OK] LinkedIn post queued for publishing")
            return True

        except Exception as e:
            self.logger.error(f"[ERROR] LinkedIn execution error: {e}")
            return False

    def execute_whatsapp_action(self, filepath: Path, metadata: dict, content: str) -> bool:
        """Execute WhatsApp message sending - FULLY AUTOMATED"""
        try:
            contact = metadata.get('contact', metadata.get('from', ''))
            message = self.extract_body(content)

            self.logger.info(f"[WHATSAPP] Sending to {contact}...")
            self.logger.info(f"[WHATSAPP] Message preview: {message[:100]}...")

            # Send via WhatsApp API
            result = self.whatsapp_client.send_message(contact, message)

            if result.get('success'):
                self.logger.info(f"[OK] WhatsApp message sent to {contact}")
                return True
            else:
                self.logger.error(f"[ERROR] WhatsApp failed: {result.get('error')}")
                return False

        except Exception as e:
            self.logger.error(f"[ERROR] WhatsApp execution error: {e}")
            return False

    def process_approved_file(self, filepath: Path):
        """Process a single approved file - FULLY AUTOMATED"""
        try:
            self.logger.info(f"\n{'='*80}")
            self.logger.info(f"[PROCESS] {filepath.name}")
            self.logger.info(f"{'='*80}")

            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse metadata
            metadata = self.parse_frontmatter(content)
            action_type = metadata.get('type', 'unknown')

            self.logger.info(f"[TYPE] {action_type}")

            # Execute based on type
            success = False

            if action_type == 'email' or 'EMAIL' in filepath.name:
                success = self.execute_email_action(filepath, metadata, content)
            elif action_type == 'linkedin_post' or 'LINKEDIN' in filepath.name:
                success = self.execute_linkedin_action(filepath, metadata, content)
            elif action_type == 'whatsapp_message' or 'WHATSAPP' in filepath.name:
                success = self.execute_whatsapp_action(filepath, metadata, content)
            else:
                self.logger.warning(f"[WARN] Unknown action type: {action_type}")
                success = False

            # Move to Done folder
            done_file = self.done_dir / filepath.name
            filepath.rename(done_file)

            # Log execution
            log_entry = {
                'filename': filepath.name,
                'type': action_type,
                'success': success,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata
            }

            log_file = self.logs_dir / f"execution_{datetime.now().strftime('%Y%m%d')}.json"

            # Append to log
            logs = []
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)

            logs.append(log_entry)

            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)

            if success:
                self.logger.info(f"[OK] Action executed successfully")
            else:
                self.logger.error(f"[FAIL] Action execution failed")

            self.logger.info(f"{'='*80}\n")

        except Exception as e:
            self.logger.error(f"[ERROR] Failed to process {filepath.name}: {e}")

    def run(self):
        """Run the approval handler - FULLY AUTOMATED 24/7"""
        self.logger.info("\n" + "="*80)
        self.logger.info("APPROVAL HANDLER - FULLY AUTOMATED")
        self.logger.info("="*80)
        self.logger.info(f"Monitoring: {self.approved_dir}")
        self.logger.info(f"Check interval: {self.check_interval} seconds")
        self.logger.info("="*80)
        self.logger.info("")
        self.logger.info("[OK] Starting autonomous execution...")
        self.logger.info("[OK] NO manual intervention required!")
        self.logger.info("")

        # Initialize WhatsApp
        self.logger.info("[INIT] Initializing WhatsApp client...")
        status = self.whatsapp_client.get_status()
        if not status.get('ready'):
            self.logger.info("[WAIT] Waiting for WhatsApp to be ready...")
            self.whatsapp_client.wait_for_ready(timeout=120)

        while True:
            try:
                # Check for approved files
                approved_files = list(self.approved_dir.glob("*.md"))

                if approved_files:
                    self.logger.info(f"\n[FOUND] {len(approved_files)} approved action(s)")

                    for filepath in approved_files:
                        self.process_approved_file(filepath)

                # Wait before next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("\n[STOP] Handler stopped by user")
                break
            except Exception as e:
                self.logger.error(f"[ERROR] Error in main loop: {e}")
                time.sleep(60)

def main():
    """Main entry point"""
    handler = AutomatedApprovalHandler()
    handler.run()

if __name__ == "__main__":
    main()
