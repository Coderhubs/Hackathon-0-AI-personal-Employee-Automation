"""
HITL (Human-in-the-Loop) Approval Handler
Monitors Pending_Approval folder and executes approved actions
"""
import os
import time
import json
import logging
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

# Add Platinum_Tier to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Platinum_Tier"))

try:
    from Platinum_Tier.mcp_client import send_email_via_mcp, check_mcp_server_available
    from Platinum_Tier.execution_engine import LinkedInExecutor, WhatsAppExecutor
    MCP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import execution modules: {e}")
    MCP_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

class ApprovalHandler(FileSystemEventHandler):
    """Handles approval workflow for sensitive actions"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create directories if they don't exist
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.rejected.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        self.logger = logging.getLogger('ApprovalHandler')
        self.logger.info(f"Monitoring: {self.pending_approval}")
        self.logger.info(f"Approved folder: {self.approved}")

    def on_created(self, event):
        """Handle new files in Approved folder"""
        if event.is_directory:
            return

        # Only process files in Approved folder
        file_path = Path(event.src_path)
        if file_path.parent.name != 'Approved':
            return

        self.logger.info(f"Approval detected: {file_path.name}")
        self.process_approval(file_path)

    def on_moved(self, event):
        """Handle files moved to Approved folder"""
        if event.is_directory:
            return

        dest_path = Path(event.dest_path)
        if dest_path.parent.name != 'Approved':
            return

        self.logger.info(f"File moved to Approved: {dest_path.name}")
        self.process_approval(dest_path)

    def process_approval(self, file_path: Path):
        """Process an approved action"""
        try:
            # Read the approval file
            content = file_path.read_text(encoding='utf-8')

            # Parse frontmatter
            if not content.startswith('---'):
                self.logger.error(f"Invalid format: {file_path.name}")
                return

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.logger.error(f"Invalid frontmatter: {file_path.name}")
                return

            frontmatter = parts[1].strip()
            metadata = self.parse_frontmatter(frontmatter)

            # Get action type
            action_type = metadata.get('action', 'unknown')

            self.logger.info(f"Processing action: {action_type}")

            # Execute action based on type
            success = False
            if action_type == 'send_email':
                success = self.execute_email_action(metadata, content)
            elif action_type == 'post_linkedin':
                success = self.execute_linkedin_action(metadata, content)
            elif action_type == 'send_whatsapp':
                success = self.execute_whatsapp_action(metadata, content)
            elif action_type == 'payment':
                success = self.execute_payment_action(metadata, content)
            else:
                self.logger.warning(f"Unknown action type: {action_type}")
                success = False

            # Log the approval
            status = 'executed' if success else 'failed'
            self.log_approval(file_path, metadata, status)

            # Move to Done
            done_path = self.done / file_path.name
            shutil.move(str(file_path), str(done_path))
            self.logger.info(f"Moved to Done: {file_path.name}")

        except Exception as e:
            self.logger.error(f"Error processing approval: {e}")
            self.log_approval(file_path, {}, f'error: {e}')

    def parse_frontmatter(self, frontmatter: str) -> dict:
        """Parse YAML-like frontmatter"""
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        return metadata

    def execute_email_action(self, metadata: dict, content: str) -> bool:
        """Execute email sending action"""
        to = metadata.get('to', '')
        subject = metadata.get('subject', '')

        # Extract body from content
        body = self.extract_body(content)

        self.logger.info(f"Sending email to: {to}")
        self.logger.info(f"Subject: {subject}")

        if not MCP_AVAILABLE:
            self.logger.error("MCP client not available. Cannot send email.")
            return False

        try:
            # Call MCP email server
            result = send_email_via_mcp(to, subject, body)

            if result.get('success'):
                self.logger.info(f"✓ Email sent successfully to {to}")
                return True
            else:
                error = result.get('error', 'Unknown error')
                self.logger.error(f"✗ Email failed: {error}")
                return False

        except Exception as e:
            self.logger.error(f"✗ Email execution error: {e}")
            return False

    def execute_linkedin_action(self, metadata: dict, content: str) -> bool:
        """Execute LinkedIn posting action"""
        post_content = self.extract_body(content)

        self.logger.info(f"Posting to LinkedIn: {post_content[:50]}...")

        if not MCP_AVAILABLE:
            self.logger.error("Execution engine not available. Cannot post to LinkedIn.")
            return False

        try:
            # Use LinkedInExecutor
            executor = LinkedInExecutor()
            result = asyncio.run(executor.post_content(post_content))

            if result:
                self.logger.info("✓ LinkedIn post created successfully")
                return True
            else:
                self.logger.error("✗ LinkedIn post failed")
                return False

        except Exception as e:
            self.logger.error(f"✗ LinkedIn execution error: {e}")
            return False

    def execute_whatsapp_action(self, metadata: dict, content: str) -> bool:
        """Execute WhatsApp message sending action"""
        contact = metadata.get('contact', metadata.get('to', ''))
        message = self.extract_body(content)

        self.logger.info(f"Sending WhatsApp message to: {contact}")

        if not MCP_AVAILABLE:
            self.logger.error("Execution engine not available. Cannot send WhatsApp message.")
            return False

        try:
            # Use WhatsAppExecutor
            executor = WhatsAppExecutor()
            result = asyncio.run(executor.send_message(contact, message))

            if result:
                self.logger.info(f"✓ WhatsApp message sent to {contact}")
                return True
            else:
                self.logger.error("✗ WhatsApp message failed")
                return False

        except Exception as e:
            self.logger.error(f"✗ WhatsApp execution error: {e}")
            return False

    def execute_payment_action(self, metadata: dict, content: str) -> bool:
        """Execute payment action"""
        amount = metadata.get('amount', '0')
        recipient = metadata.get('recipient', '')

        self.logger.info(f"Processing payment: ${amount} to {recipient}")

        # TODO: Call MCP payment server here
        self.logger.info("⚠ Payment execution not yet implemented")
        return False

    def extract_body(self, content: str) -> str:
        """Extract body content from markdown file"""
        # Remove frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return content.strip()

        body = parts[2].strip()

        # Extract content between ## Draft Reply or ## Post Content markers
        lines = body.split('\n')
        content_lines = []
        capturing = False

        for line in lines:
            # Start capturing after these headers
            if line.startswith('## Draft Reply') or line.startswith('## Post Content'):
                capturing = True
                continue

            # Stop capturing at these headers
            if line.startswith('## Original Email') or line.startswith('## Actions') or line.startswith('## Instructions'):
                break

            # Capture content
            if capturing and line.strip():
                # Skip markdown headers and separators
                if not line.startswith('#') and not line.startswith('---') and not line.startswith('**'):
                    content_lines.append(line)

        # If we captured specific content, return it
        if content_lines:
            return '\n'.join(content_lines).strip()

        # Otherwise return everything after frontmatter
        return body

    def log_approval(self, file_path: Path, metadata: dict, status: str):
        """Log approval action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'file': file_path.name,
            'action': metadata.get('action', 'unknown'),
            'status': status,
            'metadata': metadata
        }

        # Append to daily log file
        log_file = self.logs / f"{datetime.now().strftime('%Y-%m-%d')}.json"

        # Read existing logs
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []

        # Append new log
        logs.append(log_entry)

        # Write back
        log_file.write_text(json.dumps(logs, indent=2))
        self.logger.info(f"Logged to: {log_file.name}")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent / "AI_Employee_Vault"

    if not vault_path.exists():
        print(f"Error: Vault not found at {vault_path}")
        return

    print("=" * 70)
    print("HITL Approval Handler - Silver Tier")
    print("=" * 70)
    print(f"Vault: {vault_path}")
    print(f"Monitoring: {vault_path / 'Approved'}")
    print()
    print("Waiting for approvals...")
    print("Move files from Pending_Approval/ to Approved/ to execute actions")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()

    # Create handler and observer
    handler = ApprovalHandler(str(vault_path))
    observer = Observer()

    # Watch both Approved folder (for new files) and Pending_Approval (for moves)
    observer.schedule(handler, str(vault_path / 'Approved'), recursive=False)
    observer.schedule(handler, str(vault_path / 'Pending_Approval'), recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping approval handler...")
        observer.stop()

    observer.join()
    print("Approval handler stopped")

if __name__ == "__main__":
    main()
