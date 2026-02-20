"""
Base Watcher Template - Following Hackathon Architecture
All watchers inherit from this base class
"""
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

class BaseWatcher(ABC):
    """Base class for all watcher scripts"""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path.parent / 'Inbox'
        self.check_interval = check_interval
        self.logger = self.setup_logging()

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)

    def setup_logging(self):
        """Setup logging to file and console"""
        log_dir = Path("Gold_Tier/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'{self.__class__.__name__}.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def save_to_inbox(self, item, filename: str, content: str):
        """Save raw content to Inbox folder for reference"""
        filepath = self.inbox / filename
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Saved to Inbox: {filename}")
        return filepath

    def run(self):
        """Main run loop"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()

                if items:
                    self.logger.info(f'Found {len(items)} new item(s)')
                    for item in items:
                        self.create_action_file(item)
                else:
                    self.logger.info('No new items')

            except KeyboardInterrupt:
                self.logger.info(f'{self.__class__.__name__} stopped by user')
                break
            except Exception as e:
                self.logger.error(f'Error: {e}', exc_info=True)

            time.sleep(self.check_interval)
