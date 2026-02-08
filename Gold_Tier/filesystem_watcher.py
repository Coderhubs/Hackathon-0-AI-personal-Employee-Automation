import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from pathlib import Path
import logging

def setup_logging():
    """Setup logging to file"""
    log_dir = Path("Gold_Tier/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'filesystem_watcher.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('FilesystemWatcher')

class InboxHandler(FileSystemEventHandler):
    def __init__(self, inbox_dir, needs_action_dir, done_dir, dashboard_path, logger):
        self.inbox_dir = inbox_dir
        self.needs_action_dir = needs_action_dir
        self.done_dir = done_dir
        self.dashboard_path = dashboard_path
        self.logger = logger

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            filename = os.path.basename(file_path)

            # Wait briefly to ensure file is completely written
            max_attempts = 10
            attempt = 0
            file_copied = False

            while attempt < max_attempts and not file_copied:
                try:
                    # Copy file to Needs_Action
                    destination_path = os.path.join(self.needs_action_dir, filename)
                    shutil.copy2(file_path, destination_path)
                    file_copied = True
                except (OSError, IOError) as e:
                    self.logger.warning(f"Attempt {attempt + 1}: File {filename} not ready, waiting... Error: {e}")
                    time.sleep(0.5)
                    attempt += 1

            if not file_copied:
                self.logger.error(f"Failed to copy {filename} after {max_attempts} attempts")
                return

            # Create metadata .md file
            metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.md"
            metadata_path = os.path.join(self.needs_action_dir, metadata_filename)

            try:
                file_size = os.path.getsize(file_path)
            except OSError:
                # If original file no longer exists, get size from copied file
                file_size = os.path.getsize(destination_path)

            with open(metadata_path, 'w') as md_file:
                md_file.write(f"type: file_drop\n")
                md_file.write(f"filename: {filename}\n")
                md_file.write(f"size: {file_size} bytes\n")

            self.logger.info(f"Copied {filename} to Needs_Action and created metadata file")


class NeedsActionHandler(FileSystemEventHandler):
    def __init__(self, needs_action_dir, done_dir, dashboard_path, logger):
        self.needs_action_dir = needs_action_dir
        self.done_dir = done_dir
        self.dashboard_path = dashboard_path
        self.logger = logger

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('_metadata.md'):
            metadata_path = event.src_path
            self.process_metadata_file(metadata_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('_metadata.md'):
            metadata_path = event.src_path
            # Small delay to ensure file is completely written
            time.sleep(0.1)
            self.process_metadata_file(metadata_path)

    def process_metadata_file(self, metadata_path):
        """Process metadata file by summarizing content to dashboard and moving files to Done"""
        try:
            # Extract original filename from metadata filename
            metadata_filename = os.path.basename(metadata_path)
            original_filename = metadata_filename.replace('_metadata.md', '')

            # Look for the original file in Needs_Action
            original_file_path = os.path.join(self.needs_action_dir, original_filename)

            # Read metadata content
            with open(metadata_path, 'r') as f:
                metadata_content = f.read()

            # Append summary to Dashboard
            with open(self.dashboard_path, 'a') as dashboard:
                dashboard.write(f"\n## File Processed: {original_filename}\n")
                dashboard.write(f"Type: file_drop\n")
                dashboard.write(f"Summary of content:\n{metadata_content}\n")
                dashboard.write(f"Processed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Move both files to Done
            if os.path.exists(original_file_path):
                shutil.move(original_file_path, os.path.join(self.done_dir, original_filename))
            shutil.move(metadata_path, os.path.join(self.done_dir, metadata_filename))

            self.logger.info(f"Processed {original_filename} and moved files to Done")
        except Exception as e:
            self.logger.error(f"Error processing metadata file {metadata_path}: {e}")


def start_watching():
    logger = setup_logging()
    current_dir = os.getcwd()
    inbox_dir = os.path.join(current_dir, "Inbox")
    needs_action_dir = os.path.join(current_dir, "Needs_Action")
    done_dir = os.path.join(current_dir, "Done")
    dashboard_path = os.path.join(current_dir, "Dashboard.md")

    # Handler for Inbox
    inbox_handler = InboxHandler(inbox_dir, needs_action_dir, done_dir, dashboard_path, logger)

    # Handler for Needs_Action
    needs_action_handler = NeedsActionHandler(needs_action_dir, done_dir, dashboard_path, logger)

    retry_count = 0
    max_retries = 5
    base_delay = 1

    while True:
        try:
            observer = Observer()

            # Watch Inbox for new files
            observer.schedule(inbox_handler, inbox_dir, recursive=False)

            # Watch Needs_Action for new metadata files
            observer.schedule(needs_action_handler, needs_action_dir, recursive=False)

            observer.start()
            logger.info(f"Started watching {inbox_dir} and {needs_action_dir}")
            retry_count = 0  # Reset on success

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                logger.info("Stopped watching by user")
                observer.join()
                break

        except Exception as e:
            retry_count += 1
            logger.error(f"Error in filesystem watcher: {e}")

            if retry_count <= max_retries:
                delay = base_delay * (2 ** (retry_count - 1))
                logger.warning(f"Retry {retry_count}/{max_retries} in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.critical(f"Max retries ({max_retries}) reached. Waiting 60 seconds before reset...")
                time.sleep(60)
                retry_count = 0

if __name__ == "__main__":
    start_watching()