#!/usr/bin/env python3
"""
Twitter/X MCP Server
Handles Twitter posting and interaction via HITL approval
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_mcp_server import BaseMCPServer

class TwitterMCPServer(BaseMCPServer):
    """
    MCP Server for Twitter/X integration.

    All operations require HITL approval.
    """

    def __init__(self):
        super().__init__(name="Twitter")

    def register_methods(self):
        """Register Twitter-specific methods"""
        self.methods['post_tweet'] = self.post_tweet
        self.methods['reply_to_tweet'] = self.reply_to_tweet
        self.methods['send_dm'] = self.send_dm
        self.methods['get_status'] = self.get_status

    def post_tweet(self, params):
        """
        Post tweet to Twitter (requires approval).

        Args:
            params: {
                'text': str - Tweet text (max 280 characters)
            }
        """
        text = params.get('text', '')

        if not text:
            return {
                'status': 'error',
                'message': 'Text is required'
            }

        if len(text) > 280:
            return {
                'status': 'error',
                'message': f'Tweet too long: {len(text)} characters (max 280)'
            }

        # Create approval file
        action_data = {
            'action': 'post_tweet',
            'text': text,
            'platform': 'Twitter',
            'character_count': len(text)
        }

        approval_file = self.create_approval_file('TWITTER_POST', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Tweet created and awaiting approval ({len(text)} characters)'
        }

    def reply_to_tweet(self, params):
        """
        Reply to a tweet (requires approval).

        Args:
            params: {
                'tweet_id': str - Tweet ID or URL
                'text': str - Reply text
            }
        """
        tweet_id = params.get('tweet_id', '')
        text = params.get('text', '')

        if not tweet_id or not text:
            return {
                'status': 'error',
                'message': 'Tweet ID and text are required'
            }

        if len(text) > 280:
            return {
                'status': 'error',
                'message': f'Reply too long: {len(text)} characters (max 280)'
            }

        # Create approval file
        action_data = {
            'action': 'reply_to_tweet',
            'tweet_id': tweet_id,
            'text': text,
            'platform': 'Twitter'
        }

        approval_file = self.create_approval_file('TWITTER_REPLY', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Tweet reply created and awaiting approval'
        }

    def send_dm(self, params):
        """
        Send direct message (requires approval).

        Args:
            params: {
                'user': str - Username to send DM to
                'message': str - DM text
            }
        """
        user = params.get('user', '')
        message = params.get('message', '')

        if not user or not message:
            return {
                'status': 'error',
                'message': 'User and message are required'
            }

        # Create approval file
        action_data = {
            'action': 'send_dm',
            'user': user,
            'message': message,
            'platform': 'Twitter'
        }

        approval_file = self.create_approval_file('TWITTER_DM', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Twitter DM to {user} created and awaiting approval'
        }

    def requires_approval(self, method):
        """All Twitter operations require approval"""
        return method != 'get_status'

if __name__ == "__main__":
    server = TwitterMCPServer()
    server.run()
