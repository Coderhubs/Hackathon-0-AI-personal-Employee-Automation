#!/usr/bin/env python3
"""
Instagram MCP Server
Handles Instagram posting and interaction via HITL approval
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_mcp_server import BaseMCPServer

class InstagramMCPServer(BaseMCPServer):
    """
    MCP Server for Instagram integration.

    All operations require HITL approval.
    """

    def __init__(self):
        super().__init__(name="Instagram")

    def register_methods(self):
        """Register Instagram-specific methods"""
        self.methods['post_photo'] = self.post_photo
        self.methods['reply_to_dm'] = self.reply_to_dm
        self.methods['get_status'] = self.get_status

    def post_photo(self, params):
        """
        Post photo to Instagram (requires approval).

        Args:
            params: {
                'image_path': str - Path to image file
                'caption': str - Photo caption
                'hashtags': list - List of hashtags (optional)
            }
        """
        image_path = params.get('image_path', '')
        caption = params.get('caption', '')
        hashtags = params.get('hashtags', [])

        if not image_path:
            return {
                'status': 'error',
                'message': 'Image path is required'
            }

        # Create approval file
        action_data = {
            'action': 'post_photo',
            'image_path': image_path,
            'caption': caption,
            'hashtags': ', '.join(hashtags) if hashtags else 'None',
            'platform': 'Instagram'
        }

        approval_file = self.create_approval_file('INSTAGRAM_POST', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Instagram photo post created and awaiting approval'
        }

    def reply_to_dm(self, params):
        """
        Reply to Instagram DM (requires approval).

        Args:
            params: {
                'user': str - Username to reply to
                'message': str - Reply message
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
            'action': 'reply_to_dm',
            'user': user,
            'message': message,
            'platform': 'Instagram'
        }

        approval_file = self.create_approval_file('INSTAGRAM_REPLY', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Instagram DM reply to {user} created and awaiting approval'
        }

    def requires_approval(self, method):
        """All Instagram operations require approval"""
        return method != 'get_status'

if __name__ == "__main__":
    server = InstagramMCPServer()
    server.run()
