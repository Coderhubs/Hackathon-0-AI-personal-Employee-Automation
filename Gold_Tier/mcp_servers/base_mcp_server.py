#!/usr/bin/env python3
"""
Base MCP Server Class
Template for creating new MCP servers with standardized interface
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod

class BaseMCPServer(ABC):
    """
    Abstract base class for all MCP servers.

    To create a new MCP server:
    1. Inherit from BaseMCPServer
    2. Implement handle_method() for each method you support
    3. Register methods in __init__
    4. Save as {name}_server.py in mcp_servers/
    5. Add to Config/mcp_config.json
    """

    def __init__(self, name, base_dir="Gold_Tier"):
        """
        Initialize base MCP server.

        Args:
            name: Server name (e.g., "Email", "Social Media")
            base_dir: Base directory for Gold Tier system
        """
        self.name = name
        self.base_dir = Path(base_dir)
        self.pending_approval = self.base_dir / "Pending_Approval"
        self.logs = self.base_dir / "Logs"

        # Ensure directories exist
        self.pending_approval.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Method registry
        self.methods = {}
        self.register_methods()

    @abstractmethod
    def register_methods(self):
        """
        Register supported methods.

        Example:
            self.methods['send_email'] = self.send_email
            self.methods['get_status'] = self.get_status
        """
        pass

    def handle_request(self, request):
        """
        Handle MCP request.

        Args:
            request: Request dict with 'method' and 'params'

        Returns:
            Response dict
        """
        method = request.get('method')
        params = request.get('params', {})

        if method in self.methods:
            try:
                return self.methods[method](params)
            except Exception as e:
                return {'error': f'Error executing {method}: {str(e)}'}
        else:
            return {'error': f'Unknown method: {method}', 'available_methods': list(self.methods.keys())}

    def create_approval_file(self, action_type, content_dict):
        """
        Create approval file for HITL.

        Args:
            action_type: Type of action (e.g., "EMAIL", "FACEBOOK_POST")
            content_dict: Dictionary with action details

        Returns:
            Path to approval file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{action_type}_{timestamp}.md"
        filepath = self.pending_approval / filename

        # Build approval file content
        content = f"# {action_type.replace('_', ' ').title()} - PENDING APPROVAL\n\n"
        content += f"**Created:** {datetime.now().isoformat()}\n"
        content += f"**Server:** {self.name}\n"
        content += f"**Status:** AWAITING HUMAN APPROVAL\n\n"

        # Add details
        content += "## Details\n\n"
        for key, value in content_dict.items():
            content += f"**{key.replace('_', ' ').title()}:** {value}\n"

        # Add approval actions
        content += "\n## Actions\n"
        content += "- [ ] Approve and execute\n"
        content += "- [ ] Reject\n"
        content += "- [ ] Request revisions\n\n"
        content += "---\n"
        content += "*This action requires human approval before execution*\n"

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def requires_approval(self, method):
        """
        Check if method requires HITL approval.

        Override in subclass to specify which methods need approval.

        Args:
            method: Method name

        Returns:
            True if approval required, False otherwise
        """
        # By default, assume all methods require approval
        # Override in subclass for specific logic
        return True

    def get_status(self, params=None):
        """
        Get server status (standard method all servers should have).

        Returns:
            Status dict
        """
        return {
            'status': 'operational',
            'server': self.name,
            'methods': list(self.methods.keys()),
            'timestamp': datetime.now().isoformat()
        }

    def run(self):
        """
        Main MCP server loop.

        Reads JSON requests from stdin, processes them, writes JSON responses to stdout.
        """
        print(f"{self.name} MCP Server started", file=sys.stderr)

        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except Exception as e:
                error_response = {'error': str(e)}
                print(json.dumps(error_response))
                sys.stdout.flush()

# Example usage in subclass:
"""
from base_mcp_server import BaseMCPServer

class MyCustomMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="MyCustom")

    def register_methods(self):
        self.methods['do_something'] = self.do_something
        self.methods['get_status'] = self.get_status

    def do_something(self, params):
        # Your logic here
        action_data = {
            'action': 'do_something',
            'param1': params.get('param1'),
            'param2': params.get('param2')
        }

        # Create approval file
        approval_file = self.create_approval_file('CUSTOM_ACTION', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Action created and awaiting approval'
        }

    def requires_approval(self, method):
        # Only 'do_something' requires approval
        return method == 'do_something'

if __name__ == "__main__":
    server = MyCustomMCPServer()
    server.run()
"""
