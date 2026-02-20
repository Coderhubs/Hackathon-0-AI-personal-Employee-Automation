#!/usr/bin/env python3
"""
24/7 Orchestrator - Central automation system
Manages all watchers, approval processing, and task execution
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MasterOrchestrator:
    """
    Central orchestrator for 24/7 automation.

    Manages:
    - Gmail watcher (every 2 minutes)
    - Approval folder watcher (every 10 seconds)
    - Social media automation execution
    - LinkedIn, Facebook, Instagram, Twitter posting
    - Error handling and retries
    - Comprehensive logging
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.vault_path = self.base_dir / "AI_Employee_Vault"

        # Folders
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.approved = self.vault_path / "Approved"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"

        # Ensure directories exist
        for dir in [self.pending_approval, self.approved, self.done, self.logs]:
            dir.mkdir(parents=True, exist_ok=True)

        # Configuration
        self.gmail_check_interval = int(os.getenv('CHECK_INTERVAL', 120))  # 2 minutes
        self.approval_check_interval = int(os.getenv('APPROVAL_CHECK_INTERVAL', 10))  # 10 seconds
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('RETRY_DELAY', 5))

        # State tracking
        self.last_gmail_check = 0
        self.last_approval_check = 0
        self.running = True
        self.processed_files = set()

        # Setup logging
        self.setup_logging()

        # Process registry
        self.processes = {}

    def setup_logging(self):
        """Setup comprehensive logging"""
        log_file = self.logs / f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MasterOrchestrator')

    def log_status(self, message: str, level: str = "INFO"):
        """Log with status tracking"""
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)

        # Update status file
        status_file = self.vault_path / "orchestrator_status.txt"
        status_file.write_text(f"Last update: {datetime.now().isoformat()}\n{message}\n")

    def check_gmail(self):
        """Check Gmail every 2 minutes"""
        current_time = time.time()

        if current_time - self.last_gmail_check < self.gmail_check_interval:
            return

        self.last_gmail_check = current_time
        self.log_status("Checking Gmail...")

        try:
            # Run Gmail watcher
            gmail_watcher = self.base_dir / "Platinum_Tier" / "gmail_watcher_imap.py"

            if gmail_watcher.exists():
                result = subprocess.run(
                    [sys.executable, str(gmail_watcher)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    self.log_status("Gmail check completed successfully")
                else:
                    self.log_status(f"Gmail check failed: {result.stderr}", "ERROR")
            else:
                self.log_status("Gmail watcher not found", "WARNING")

        except Exception as e:
            self.log_status(f"Error checking Gmail: {e}", "ERROR")

    def check_approved_folder(self):
        """Check approved folder for new files"""
        current_time = time.time()

        if current_time - self.last_approval_check < self.approval_check_interval:
            return

        self.last_approval_check = current_time

        if not self.approved.exists():
            return

        # Get all files in approved folder
        approved_files = list(self.approved.glob("*.md"))

        if not approved_files:
            return

        self.log_status(f"Found {len(approved_files)} approved file(s)")

        for file in approved_files:
            if file.name in self.processed_files:
                continue

            self.log_status(f"Processing approved file: {file.name}")
            self.execute_approved_action(file)
            self.processed_files.add(file.name)

    def execute_approved_action(self, file: Path):
        """Execute action based on approved file"""
        try:
            # Read file content
            content = file.read_text(encoding='utf-8')

            # Determine action type and execute
            success = False
            if 'LINKEDIN' in file.name.upper():
                success = self.execute_linkedin_action(file, content)
            elif 'FACEBOOK' in file.name.upper():
                success = self.execute_facebook_action(file, content)
            elif 'INSTAGRAM' in file.name.upper():
                success = self.execute_instagram_action(file, content)
            elif 'TWITTER' in file.name.upper():
                success = self.execute_twitter_action(file, content)
            elif 'EMAIL' in file.name.upper() or 'GMAIL' in file.name.upper():
                success = self.execute_email_action(file, content)
            else:
                self.log_status(f"Unknown action type: {file.name}", "WARNING")
                return

            # Only move to done if successful
            if success:
                done_file = self.done / file.name
                file.rename(done_file)
                self.log_status(f"Completed and moved to Done: {file.name}")
            else:
                self.log_status(f"Action failed, keeping in Approved: {file.name}", "ERROR")

        except Exception as e:
            self.log_status(f"Error executing {file.name}: {e}", "ERROR")

    def execute_linkedin_action(self, file: Path, content: str) -> bool:
        """Execute LinkedIn posting"""
        self.log_status("Executing LinkedIn action...")

        automation_script = self.base_dir / "linkedin_post_simple.py"

        if automation_script.exists():
            result = subprocess.run(
                [sys.executable, str(automation_script), str(file)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                self.log_status("LinkedIn action completed successfully")
                return True
            else:
                self.log_status(f"LinkedIn action failed: {result.stderr}", "ERROR")
                return False
        else:
            self.log_status("LinkedIn automation script not found", "WARNING")
            return False

    def execute_facebook_action(self, file: Path, content: str):
        """Execute Facebook posting"""
        self.log_status("Executing Facebook action...")

        automation_script = self.base_dir / "Gold_Tier" / "facebook_automation.py"

        if automation_script.exists():
            result = subprocess.run(
                [sys.executable, str(automation_script)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log_status("Facebook action completed successfully")
            else:
                self.log_status(f"Facebook action failed: {result.stderr}", "ERROR")
        else:
            self.log_status("Facebook automation script not found", "WARNING")

    def execute_instagram_action(self, file: Path, content: str):
        """Execute Instagram posting"""
        self.log_status("Executing Instagram action...")

        automation_script = self.base_dir / "Gold_Tier" / "instagram_automation.py"

        if automation_script.exists():
            result = subprocess.run(
                [sys.executable, str(automation_script)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log_status("Instagram action completed successfully")
            else:
                self.log_status(f"Instagram action failed: {result.stderr}", "ERROR")
        else:
            self.log_status("Instagram automation script not found", "WARNING")

    def execute_twitter_action(self, file: Path, content: str):
        """Execute Twitter posting"""
        self.log_status("Executing Twitter action...")

        automation_script = self.base_dir / "Gold_Tier" / "twitter_automation.py"

        if automation_script.exists():
            result = subprocess.run(
                [sys.executable, str(automation_script)],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log_status("Twitter action completed successfully")
            else:
                self.log_status(f"Twitter action failed: {result.stderr}", "ERROR")
        else:
            self.log_status("Twitter automation script not found", "WARNING")

    def execute_email_action(self, file: Path, content: str):
        """Execute email sending"""
        self.log_status("Executing email action...")

        # In real implementation, would call email MCP server
        self.log_status("Email action completed (simulated)")

    def generate_status_report(self) -> Dict:
        """Generate status report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'running': self.running,
            'last_gmail_check': datetime.fromtimestamp(self.last_gmail_check).isoformat() if self.last_gmail_check > 0 else 'Never',
            'last_approval_check': datetime.fromtimestamp(self.last_approval_check).isoformat() if self.last_approval_check > 0 else 'Never',
            'processed_files_count': len(self.processed_files),
            'pending_approval_count': len(list(self.pending_approval.glob('*.md'))) if self.pending_approval.exists() else 0,
            'approved_count': len(list(self.approved.glob('*.md'))) if self.approved.exists() else 0,
            'done_count': len(list(self.done.glob('*.md'))) if self.done.exists() else 0
        }

    def save_status_report(self):
        """Save status report to file"""
        report = self.generate_status_report()
        report_file = self.vault_path / "orchestrator_report.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

    def run(self):
        """Main orchestrator loop - runs 24/7"""
        self.log_status("="*60)
        self.log_status("24/7 Master Orchestrator Started")
        self.log_status("="*60)
        self.log_status(f"Gmail check interval: {self.gmail_check_interval} seconds")
        self.log_status(f"Approval check interval: {self.approval_check_interval} seconds")
        self.log_status(f"Vault path: {self.vault_path}")
        self.log_status("="*60)

        iteration = 0

        while self.running:
            try:
                iteration += 1

                # Check Gmail (every 2 minutes)
                self.check_gmail()

                # Check approved folder (every 10 seconds)
                self.check_approved_folder()

                # Save status report every 10 iterations
                if iteration % 10 == 0:
                    self.save_status_report()
                    report = self.generate_status_report()
                    self.log_status(f"Status: {report['pending_approval_count']} pending, {report['approved_count']} approved, {report['done_count']} done")

                # Sleep for 1 second (main loop runs every second)
                time.sleep(1)

            except KeyboardInterrupt:
                self.log_status("Orchestrator stopped by user")
                self.running = False
                break
            except Exception as e:
                self.log_status(f"Error in main loop: {e}", "ERROR")
                time.sleep(5)  # Wait before retrying

        self.log_status("="*60)
        self.log_status("24/7 Master Orchestrator Stopped")
        self.log_status("="*60)

if __name__ == "__main__":
    orchestrator = MasterOrchestrator()
    orchestrator.run()
