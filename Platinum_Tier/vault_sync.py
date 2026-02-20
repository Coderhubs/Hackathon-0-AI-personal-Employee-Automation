#!/usr/bin/env python3
"""
Vault Sync - Simulates Git-based vault syncing
Uses shared Docker volume for cloud/local communication
"""

import os
import time
import shutil
from pathlib import Path
from datetime import datetime
import logging
import fcntl

class VaultSync:
    """
    Vault synchronization mechanism.

    Simulates Git sync using shared Docker volume.
    Implements file locking to prevent conflicts.
    """

    def __init__(self, vault_path: str = None):
        if vault_path is None:
            vault_path = os.getenv('VAULT_PATH', '/vault')

        self.vault_path = Path(vault_path)
        self.lock_file = self.vault_path / '.sync.lock'

        # Setup logging
        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / 'vault_sync.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('VaultSync')

    def acquire_lock(self, timeout: int = 10) -> bool:
        """Acquire file lock for sync operation"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Create lock file
                lock_fd = os.open(str(self.lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(lock_fd, f"{os.getpid()}\n{datetime.now().isoformat()}".encode())
                os.close(lock_fd)
                return True
            except FileExistsError:
                # Lock already held, wait
                time.sleep(0.5)

        return False

    def release_lock(self):
        """Release file lock"""
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
        except Exception as e:
            self.logger.error(f"Error releasing lock: {e}")

    def sync_folder(self, source: Path, dest: Path, direction: str = "bidirectional"):
        """
        Sync files between folders.

        Args:
            source: Source folder
            dest: Destination folder
            direction: 'push', 'pull', or 'bidirectional'
        """
        if not source.exists():
            self.logger.warning(f"Source folder does not exist: {source}")
            return

        dest.mkdir(parents=True, exist_ok=True)

        # Get files from source
        source_files = {f.relative_to(source): f for f in source.rglob('*') if f.is_file()}

        # Get files from dest
        dest_files = {f.relative_to(dest): f for f in dest.rglob('*') if f.is_file()}

        # Sync based on direction
        if direction in ['push', 'bidirectional']:
            # Copy from source to dest
            for rel_path, source_file in source_files.items():
                dest_file = dest / rel_path

                # Check if file needs updating
                if not dest_file.exists() or source_file.stat().st_mtime > dest_file.stat().st_mtime:
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, dest_file)
                    self.logger.info(f"Synced: {rel_path}")

        if direction in ['pull', 'bidirectional']:
            # Copy from dest to source
            for rel_path, dest_file in dest_files.items():
                source_file = source / rel_path

                # Check if file needs updating
                if not source_file.exists() or dest_file.stat().st_mtime > source_file.stat().st_mtime:
                    source_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dest_file, source_file)
                    self.logger.info(f"Synced: {rel_path}")

    def sync_vault(self):
        """Sync entire vault"""
        self.logger.info("Starting vault sync...")

        if not self.acquire_lock():
            self.logger.error("Could not acquire lock for sync")
            return

        try:
            # Sync key folders
            folders_to_sync = [
                'Needs_Action',
                'Pending_Approval',
                'Approved',
                'Done',
                'Plans'
            ]

            for folder in folders_to_sync:
                source = self.vault_path / folder
                if source.exists():
                    self.logger.info(f"Syncing folder: {folder}")
                    # In real implementation, would sync with remote
                    # For simulation, just log
                    file_count = len(list(source.rglob('*')))
                    self.logger.info(f"  {file_count} files in {folder}")

            self.logger.info("Vault sync complete")

        finally:
            self.release_lock()

    def run_continuous_sync(self, interval: int = 30):
        """Run continuous sync loop"""
        self.logger.info(f"Starting continuous sync (every {interval} seconds)")

        while True:
            try:
                self.sync_vault()
            except KeyboardInterrupt:
                self.logger.info("Sync stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error during sync: {e}")

            time.sleep(interval)

if __name__ == "__main__":
    sync = VaultSync()
    sync.run_continuous_sync()
