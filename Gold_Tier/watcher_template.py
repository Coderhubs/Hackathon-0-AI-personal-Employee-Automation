#!/usr/bin/env python3
"""
Watcher Template
Copy this file to create a new watcher plugin

Steps to create a new watcher:
1. Copy this file to {yourname}_watcher.py
2. Update the class name and configuration
3. Implement watch() and create_task_file() methods
4. Test your watcher: python {yourname}_watcher.py
5. Add to Config/watchers_config.json (optional - auto-discovery enabled)
6. Restart system: start_gold_tier.bat
"""

from base_watcher import BaseWatcher
from datetime import datetime

class TemplateWatcher(BaseWatcher):
    """
    Template Watcher - Replace with your watcher name

    This watcher monitors [DESCRIBE WHAT YOU'RE MONITORING]
    and creates task files when [DESCRIBE TRIGGER CONDITION].
    """

    def __init__(self):
        # Configure your watcher
        super().__init__(
            name="Template",              # Display name
            interval_seconds=300,         # Check every 5 minutes (or None for event-driven)
            base_dir="Gold_Tier"         # Base directory
        )

        # Add any custom initialization here
        self.api_key = None  # Example: API credentials
        self.last_check = None

    def watch(self):
        """
        Main monitoring logic.

        This method is called every interval_seconds.
        Return True on success, False on failure.
        """
        try:
            # STEP 1: Check for new content/events
            # Example: Call an API, check a database, monitor a file, etc.
            data = self.fetch_data()

            # STEP 2: If something found, create task file
            if data:
                self.create_task_file(data)

            # STEP 3: Return success
            return True

        except Exception as e:
            self.logger.error(f"Error in watch(): {e}")
            return False

    def fetch_data(self):
        """
        Fetch data from your source.

        Replace this with your actual data fetching logic:
        - API calls
        - Database queries
        - File system checks
        - Web scraping
        - etc.
        """
        # Example: Return some data
        # In real implementation, this would call an API, check a database, etc.

        # For now, return None (no data)
        return None

        # Example of returning data:
        # return {
        #     "title": "New Event",
        #     "content": "Something happened",
        #     "timestamp": datetime.now().isoformat()
        # }

    def create_task_file(self, data):
        """
        Create task file in Inbox.

        Args:
            data: Data to write to task file

        Returns:
            Path to created file
        """
        # Generate filename with your prefix
        filename = self.generate_filename("TEMPLATE")  # Change "TEMPLATE" to your prefix
        filepath = self.inbox / filename

        # Format content
        if isinstance(data, dict):
            content = self.format_dict_content(data)
        else:
            content = str(data)

        # Write file
        self.write_file(filepath, content)

        return filepath

    def format_dict_content(self, data):
        """
        Format dictionary data as readable content.

        Args:
            data: Dictionary to format

        Returns:
            Formatted string
        """
        lines = []
        for key, value in data.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)

# Example: Event-driven watcher (no interval)
"""
class EventDrivenWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(
            name="EventDriven",
            interval_seconds=None,  # Event-driven, not interval-based
            base_dir="Gold_Tier"
        )

    def watch(self):
        # Use watchdog or similar for event-driven monitoring
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        # Your event-driven logic here
        pass
"""

# Example: API-based watcher
"""
class APIWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(
            name="API",
            interval_seconds=600,  # Check every 10 minutes
            base_dir="Gold_Tier"
        )
        self.api_url = "https://api.example.com/data"
        self.api_key = os.getenv("API_KEY")

    def fetch_data(self):
        import requests
        response = requests.get(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        if response.status_code == 200:
            return response.json()
        return None
"""

# Example: Database watcher
"""
class DatabaseWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(
            name="Database",
            interval_seconds=300,  # Check every 5 minutes
            base_dir="Gold_Tier"
        )
        self.db_connection = None

    def fetch_data(self):
        # Connect to database and query for new records
        # Return results
        pass
"""

if __name__ == "__main__":
    # Test your watcher
    watcher = TemplateWatcher()
    watcher.run()
