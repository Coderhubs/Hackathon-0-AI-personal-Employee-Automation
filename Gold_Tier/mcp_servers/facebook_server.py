#!/usr/bin/env python3
"""
Facebook MCP Server
Handles Facebook posting and interaction via HITL approval
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from base_mcp_server import BaseMCPServer

class FacebookMCPServer(BaseMCPServer):
    """
    MCP Server for Facebook integration.

    All operations require HITL approval.
    """

    def __init__(self):
        super().__init__(name="Facebook")

    def register_methods(self):
        """Register Facebook-specific methods"""
        self.methods['post_status'] = self.post_status
        self.methods['post_photo'] = self.post_photo
        self.methods['reply_to_comment'] = self.reply_to_comment
        self.methods['get_status'] = self.get_status

    def post_status(self, params):
        """
        Post status update to Facebook (requires approval).

        Args:
            params: {
                'text': str - Status text
            }
        """
        text = params.get('text', '')

        if not text:
            return {
                'status': 'error',
                'message': 'Text is required'
            }

        # Create approval file
        action_data = {
            'action': 'post_status',
            'text': text,
            'platform': 'Facebook',
            'character_count': len(text)
        }

        approval_file = self.create_approval_file('FACEBOOK_POST', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Facebook status post created and awaiting approval ({len(text)} characters)'
        }

    def post_photo(self, params):
        """
        Post photo to Facebook (requires approval).

        Args:
            params: {
                'image_path': str - Path to image file
                'caption': str - Photo caption
            }
        """
        image_path = params.get('image_path', '')
        caption = params.get('caption', '')

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
            'platform': 'Facebook'
        }

        approval_file = self.create_approval_file('FACEBOOK_PHOTO', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Facebook photo post created and awaiting approval'
        }

    def reply_to_comment(self, params):
        """
        Reply to Facebook comment (requires approval).

        Args:
            params: {
                'comment_id': str - Comment ID
                'text': str - Reply text
            }
        """
        comment_id = params.get('comment_id', '')
        text = params.get('text', '')

        if not comment_id or not text:
            return {
                'status': 'error',
                'message': 'Comment ID and text are required'
            }

        # Create approval file
        action_data = {
            'action': 'reply_to_comment',
            'comment_id': comment_id,
            'text': text,
            'platform': 'Facebook'
        }

        approval_file = self.create_approval_file('FACEBOOK_REPLY', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Facebook comment reply created and awaiting approval'
        }

    def requires_approval(self, method):
        """All Facebook operations require approval"""
        return method != 'get_status'

if __name__ == "__main__":
    server = FacebookMCPServer()
    server.run()
