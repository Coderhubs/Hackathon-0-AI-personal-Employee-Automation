#!/usr/bin/env python3
"""
Local Agent - Executes approved actions
Runs on local machine with full capabilities
"""

import os
import time
from pathlib import Path
from datetime import datetime
import logging
import shutil

class LocalAgent:
    """
    Local agent for action execution.

    Responsibilities:
    - Process files from Pending_Approval/
    - Execute approved actions
    - Use MCP servers and Playwright
    - Write results to Done/
    """

    def __init__(self):
        self.vault_path = Path(os.getenv('VAULT_PATH', '/vault'))
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Ensure directories exist
        for dir in [self.pending_approval, self.approved, self.done, self.logs]:
            dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / 'local_agent.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('LocalAgent')

    def process_approved_files(self):
        """Process all approved files"""
        if not self.approved.exists():
            return

        approved_files = list(self.approved.glob('*.md'))

        if not approved_files:
            self.logger.info("No approved files to process")
            return

        self.logger.info(f"Found {len(approved_files)} approved file(s)")

        for file in approved_files:
            try:
                self.logger.info(f"Processing: {file.name}")

                # Read file content
                content = file.read_text(encoding='utf-8')

                # Execute action based on type
                if 'EMAIL' in file.name:
                    self.execute_email_action(file, content)
                elif 'FACEBOOK' in file.name:
                    self.execute_facebook_action(file, content)
                elif 'INSTAGRAM' in file.name:
                    self.execute_instagram_action(file, content)
                elif 'TWITTER' in file.name:
                    self.execute_twitter_action(file, content)
                else:
                    self.logger.warning(f"Unknown action type: {file.name}")

                # Move to Done
                done_file = self.done / file.name
                shutil.move(str(file), str(done_file))
                self.logger.info(f"Moved to Done: {file.name}")

            except Exception as e:
                self.logger.error(f"Error processing {file.name}: {e}")

    def execute_email_action(self, file, content):
        """Execute email action"""
        self.logger.info("Executing email action (simulated)")
        # In real implementation, would call email MCP server

    def execute_facebook_action(self, file, content):
        """Execute Facebook action"""
        self.logger.info("Executing Facebook action (simulated)")
        # In real implementation, would call Facebook automation

    def execute_instagram_action(self, file, content):
        """Execute Instagram action"""
        self.logger.info("Executing Instagram action (simulated)")
        # In real implementation, would call Instagram automation

    def execute_twitter_action(self, file, content):
        """Execute Twitter action"""
        self.logger.info("Executing Twitter action (simulated)")
        # In real implementation, would call Twitter automation

    def run(self):
        """Main run loop"""
        self.logger.info("Local Agent started")
        self.logger.info(f"Vault path: {self.vault_path}")

        while True:
            try:
                self.logger.info("Processing approved files...")
                self.process_approved_files()

                # Update status file
                status_file = self.vault_path / 'local_status.txt'
                status_file.write_text(f"Last check: {datetime.now().isoformat()}\n")

            except KeyboardInterrupt:
                self.logger.info("Local Agent stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")

            # Wait 1 minute before next check
            time.sleep(60)

if __name__ == "__main__":
    agent = LocalAgent()
    agent.run()
