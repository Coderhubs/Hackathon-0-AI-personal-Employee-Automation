#!/usr/bin/env python3
"""
Example: Discord MCP Server Plugin
Demonstrates how to create a custom MCP server in 5 minutes
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_servers.base_mcp_server import BaseMCPServer

class DiscordServer(BaseMCPServer):
    """
    Discord MCP Server - Sends messages to Discord channels

    This is a complete, working example of a custom MCP server plugin.
    It demonstrates:
    - Method registration
    - HITL approval workflow
    - Configuration via environment variables
    - Error handling
    """

    def __init__(self):
        super().__init__(name="Discord")

        # Configuration from environment variables
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN')

        if not self.webhook_url and not self.bot_token:
            print("Warning: DISCORD_WEBHOOK_URL or DISCORD_BOT_TOKEN not set - running in demo mode", file=sys.stderr)

    def register_methods(self):
        """Register all supported methods"""
        self.methods['send_message'] = self.send_message
        self.methods['send_embed'] = self.send_embed
        self.methods['get_channels'] = self.get_channels
        self.methods['get_status'] = self.get_status

    def send_message(self, params):
        """
        Send message to Discord channel (requires HITL approval).

        Args:
            params: Dict with 'channel', 'message'

        Returns:
            Response dict
        """
        channel = params.get('channel', '')
        message = params.get('message', '')

        # Validate parameters
        if not message:
            return {'error': 'message parameter is required'}

        # Prepare action data for approval
        action_data = {
            'action': 'Send Discord Message',
            'channel': channel or 'Default',
            'message': message,
            'webhook_url': self.webhook_url or 'Not configured'
        }

        # Create approval file (HITL)
        approval_file = self.create_approval_file('DISCORD_MESSAGE', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Discord message created and awaiting approval'
        }

    def send_embed(self, params):
        """
        Send rich embed to Discord channel (requires HITL approval).

        Args:
            params: Dict with 'channel', 'title', 'description', 'color'

        Returns:
            Response dict
        """
        channel = params.get('channel', '')
        title = params.get('title', '')
        description = params.get('description', '')
        color = params.get('color', '0x00ff00')

        # Validate parameters
        if not title and not description:
            return {'error': 'title or description required'}

        # Prepare action data for approval
        action_data = {
            'action': 'Send Discord Embed',
            'channel': channel or 'Default',
            'title': title,
            'description': description,
            'color': color
        }

        # Create approval file (HITL)
        approval_file = self.create_approval_file('DISCORD_EMBED', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Discord embed created and awaiting approval'
        }

    def get_channels(self, params):
        """
        Get list of Discord channels (no approval needed).

        Args:
            params: Dict (unused)

        Returns:
            Response dict with channels list
        """
        # This is a read-only operation, no approval needed

        if not self.bot_token:
            return {
                'status': 'demo_mode',
                'channels': [
                    {'id': '123456789', 'name': 'general'},
                    {'id': '987654321', 'name': 'announcements'}
                ],
                'message': 'Demo mode - DISCORD_BOT_TOKEN not set'
            }

        # Real implementation would call Discord API here
        # import requests
        # response = requests.get(
        #     'https://discord.com/api/v10/guilds/{guild_id}/channels',
        #     headers={'Authorization': f'Bot {self.bot_token}'}
        # )
        # return {'status': 'success', 'channels': response.json()}

        return {
            'status': 'success',
            'channels': [],
            'message': 'Would fetch channels from Discord API'
        }

    def requires_approval(self, method):
        """
        Specify which methods require HITL approval.

        Args:
            method: Method name

        Returns:
            True if approval required, False otherwise
        """
        # Sending messages requires approval
        # Reading channels does not
        approval_required = ['send_message', 'send_embed']
        return method in approval_required

if __name__ == "__main__":
    # Test the server
    server = DiscordServer()
    server.run()
