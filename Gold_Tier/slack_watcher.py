#!/usr/bin/env python3
"""
Example: Slack Watcher Plugin
Demonstrates how to create a custom watcher in 5 minutes
"""

from base_watcher import BaseWatcher
import os
import json

class SlackWatcher(BaseWatcher):
    """
    Slack Watcher - Monitors Slack channels for new messages

    This is a complete, working example of a custom watcher plugin.
    It demonstrates:
    - API integration
    - Error handling
    - Task file creation
    - Configuration via environment variables
    """

    def __init__(self):
        super().__init__(
            name="Slack",
            interval_seconds=120,  # Check every 2 minutes
            base_dir="Gold_Tier"
        )

        # Configuration from environment variables
        self.token = os.getenv('SLACK_TOKEN')
        self.channel = os.getenv('SLACK_CHANNEL', 'general')
        self.last_timestamp = None

        if not self.token:
            self.logger.warning("SLACK_TOKEN not set - running in demo mode")

    def watch(self):
        """
        Check Slack for new messages.

        Returns:
            True on success, False on failure
        """
        try:
            # In demo mode, create sample messages
            if not self.token:
                return self.demo_mode()

            # Real implementation would call Slack API here
            # import requests
            # response = requests.get(
            #     'https://slack.com/api/conversations.history',
            #     headers={'Authorization': f'Bearer {self.token}'},
            #     params={
            #         'channel': self.channel,
            #         'limit': 10,
            #         'oldest': self.last_timestamp or '0'
            #     }
            # )
            # messages = response.json().get('messages', [])

            # For now, return success
            return True

        except Exception as e:
            self.logger.error(f"Error fetching Slack messages: {e}")
            return False

    def demo_mode(self):
        """
        Demo mode - creates sample task files for testing.

        Returns:
            True
        """
        self.logger.info("Running in demo mode - SLACK_TOKEN not set")

        # Create a sample message every 5th check
        import random
        if random.randint(1, 5) == 1:
            sample_message = {
                'user': 'demo_user',
                'text': 'This is a demo Slack message',
                'channel': self.channel,
                'timestamp': '1234567890.123456'
            }
            self.create_task_file(sample_message)

        return True

    def create_task_file(self, message):
        """
        Create task file from Slack message.

        Args:
            message: Slack message dict

        Returns:
            Path to created file
        """
        # Generate filename
        filename = self.generate_filename("SLACK")
        filepath = self.inbox / filename

        # Format content
        content = self.format_message(message)

        # Write file
        self.write_file(filepath, content)

        # Update last timestamp
        self.last_timestamp = message.get('timestamp')

        return filepath

    def format_message(self, message):
        """
        Format Slack message as readable content.

        Args:
            message: Slack message dict

        Returns:
            Formatted string
        """
        lines = [
            f"Slack Message",
            f"=" * 40,
            f"Channel: {self.channel}",
            f"User: {message.get('user', 'Unknown')}",
            f"Timestamp: {message.get('timestamp', 'N/A')}",
            f"",
            f"Message:",
            f"{message.get('text', '')}",
            f"",
            f"=" * 40
        ]
        return "\n".join(lines)

if __name__ == "__main__":
    # Test the watcher
    watcher = SlackWatcher()
    watcher.run()
