#!/usr/bin/env python3
"""
Base Watcher Class
Template for creating new watchers with standardized interface
"""

import os
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

class BaseWatcher(ABC):
    """
    Abstract base class for all watchers.

    To create a new watcher:
    1. Inherit from BaseWatcher
    2. Implement watch() method
    3. Implement create_task_file() method
    4. Save as {name}_watcher.py
    5. Add to Config/watchers_config.json (optional - auto-discovery enabled)
    """

    def __init__(self, name, interval_seconds=60, base_dir="Gold_Tier"):
        """
        Initialize base watcher.

        Args:
            name: Watcher name (e.g., "Gmail", "LinkedIn")
            interval_seconds: How often to check (None for event-driven)
            base_dir: Base directory for Gold Tier system
        """
        self.name = name
        self.interval_seconds = interval_seconds
        self.base_dir = Path(base_dir)
        self.inbox = self.base_dir / "Inbox"
        self.logs = self.base_dir / "Logs"

        # Ensure directories exist
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = self.setup_logging()

        # Error recovery settings
        self.retry_count = 0
        self.max_retries = 5
        self.base_delay = 1

    def setup_logging(self):
        """Setup logging for this watcher"""
        log_file = self.logs / f"{self.name.lower().replace(' ', '_')}_watcher.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(f'{self.name}Watcher')

    @abstractmethod
    def watch(self):
        """
        Main watch logic - implement in subclass.

        This method should:
        1. Check for new content/events
        2. Call create_task_file() when something is found
        3. Return True on success, False on failure
        """
        pass

    @abstractmethod
    def create_task_file(self, data):
        """
        Create task file in Inbox.

        Args:
            data: Data to write to task file (dict, string, etc.)

        Returns:
            Path to created file
        """
        pass

    def run(self):
        """
        Main run loop with error recovery.

        This method handles:
        - Continuous monitoring (if interval_seconds set)
        - Error recovery with exponential backoff
        - Logging
        """
        self.logger.info(f"Starting {self.name} Watcher with error recovery...")

        if self.interval_seconds:
            self.logger.info(f"Checking every {self.interval_seconds} seconds")
        else:
            self.logger.info("Event-driven monitoring")

        while True:
            try:
                success = self.watch()

                if success:
                    self.retry_count = 0  # Reset on success

                if self.interval_seconds:
                    time.sleep(self.interval_seconds)
                else:
                    # Event-driven watchers handle their own timing
                    break

            except KeyboardInterrupt:
                self.logger.info(f"{self.name} Watcher stopped by user.")
                break

            except Exception as e:
                self.retry_count += 1
                self.logger.error(f"Error in {self.name} Watcher: {e}")

                if self.retry_count <= self.max_retries:
                    # Exponential backoff: 1, 2, 4, 8, 16 seconds
                    delay = self.base_delay * (2 ** (self.retry_count - 1))
                    self.logger.warning(f"Retry {self.retry_count}/{self.max_retries} in {delay} seconds...")
                    time.sleep(delay)
                else:
                    wait_time = self.interval_seconds if self.interval_seconds else 60
                    self.logger.critical(f"Max retries ({self.max_retries}) reached. Waiting {wait_time} seconds before reset...")
                    time.sleep(wait_time)
                    self.retry_count = 0  # Reset retry counter

    def generate_filename(self, prefix, extension="txt"):
        """
        Generate standardized filename.

        Args:
            prefix: Filename prefix (e.g., "GMAIL", "LINKEDIN")
            extension: File extension (default: "txt")

        Returns:
            Filename string
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"

    def write_file(self, filepath, content):
        """
        Write content to file with error handling.

        Args:
            filepath: Path to file
            content: Content to write

        Returns:
            True on success, False on failure
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Created file: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to write file {filepath}: {e}")
            return False

# Example usage in subclass:
"""
from base_watcher import BaseWatcher

class MyCustomWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(name="MyCustom", interval_seconds=300)

    def watch(self):
        # Your monitoring logic here
        data = self.fetch_data()
        if data:
            self.create_task_file(data)
        return True

    def create_task_file(self, data):
        filename = self.generate_filename("MYCUSTOM")
        filepath = self.inbox / filename
        return self.write_file(filepath, str(data))

    def fetch_data(self):
        # Your data fetching logic
        return "Some data"

if __name__ == "__main__":
    watcher = MyCustomWatcher()
    watcher.run()
"""
