#!/usr/bin/env python3
"""
MCP Server Template
Copy this file to create a new MCP server plugin

Steps to create a new MCP server:
1. Copy this file to mcp_servers/{yourname}_server.py
2. Update the class name and configuration
3. Implement register_methods() and your custom methods
4. Test your server: echo '{"method":"get_status"}' | python mcp_servers/{yourname}_server.py
5. Add to Config/mcp_config.json
6. Restart system
"""

import sys
import os

# Add parent directory to path to import base class
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_servers.base_mcp_server import BaseMCPServer

class TemplateMCPServer(BaseMCPServer):
    """
    Template MCP Server - Replace with your server name

    This server provides [DESCRIBE FUNCTIONALITY]
    and supports the following methods:
    - method1: [DESCRIPTION]
    - method2: [DESCRIPTION]
    """

    def __init__(self):
        # Initialize with your server name
        super().__init__(name="Template")

        # Add any custom initialization here
        self.api_key = os.getenv('TEMPLATE_API_KEY')
        self.api_url = os.getenv('TEMPLATE_API_URL')

    def register_methods(self):
        """
        Register all methods this server supports.

        Each method should:
        1. Accept params dict as argument
        2. Return response dict
        3. Create approval file if HITL required
        """
        # Register your methods here
        self.methods['method1'] = self.method1
        self.methods['method2'] = self.method2
        self.methods['get_status'] = self.get_status

    def method1(self, params):
        """
        Example method that requires approval.

        Args:
            params: Dict with method parameters

        Returns:
            Response dict
        """
        # Extract parameters
        param1 = params.get('param1', '')
        param2 = params.get('param2', '')

        # Validate parameters
        if not param1:
            return {'error': 'param1 is required'}

        # Prepare action data for approval
        action_data = {
            'method': 'method1',
            'param1': param1,
            'param2': param2,
            'description': 'This action will do something important'
        }

        # Create approval file (HITL)
        approval_file = self.create_approval_file('TEMPLATE_METHOD1', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Action created and awaiting approval'
        }

    def method2(self, params):
        """
        Example method that does NOT require approval.

        Args:
            params: Dict with method parameters

        Returns:
            Response dict
        """
        # This method executes immediately without approval
        result = self.do_something_safe(params)

        return {
            'status': 'success',
            'result': result,
            'message': 'Action completed successfully'
        }

    def do_something_safe(self, params):
        """
        Helper method for safe operations.

        Args:
            params: Parameters dict

        Returns:
            Result of operation
        """
        # Your safe operation logic here
        # Example: Read data, query database, etc.
        return {'data': 'example'}

    def requires_approval(self, method):
        """
        Specify which methods require HITL approval.

        Args:
            method: Method name

        Returns:
            True if approval required, False otherwise
        """
        # Methods that require approval
        approval_required = ['method1']

        return method in approval_required

# Example: API Integration Server
"""
class APIIntegrationServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="APIIntegration")
        self.api_key = os.getenv('API_KEY')
        self.base_url = "https://api.example.com"

    def register_methods(self):
        self.methods['fetch_data'] = self.fetch_data
        self.methods['send_data'] = self.send_data
        self.methods['get_status'] = self.get_status

    def fetch_data(self, params):
        import requests
        endpoint = params.get('endpoint', '')
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return {'status': 'success', 'data': response.json()}

    def send_data(self, params):
        # This requires approval
        action_data = {
            'endpoint': params.get('endpoint'),
            'data': params.get('data')
        }
        approval_file = self.create_approval_file('API_SEND', action_data)
        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file)
        }

    def requires_approval(self, method):
        return method == 'send_data'
"""

# Example: Database Server
"""
class DatabaseServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="Database")
        self.connection = None

    def register_methods(self):
        self.methods['query'] = self.query
        self.methods['insert'] = self.insert
        self.methods['update'] = self.update
        self.methods['delete'] = self.delete
        self.methods['get_status'] = self.get_status

    def query(self, params):
        # Read-only, no approval needed
        sql = params.get('sql', '')
        # Execute query
        return {'status': 'success', 'results': []}

    def insert(self, params):
        # Requires approval
        action_data = {
            'table': params.get('table'),
            'data': params.get('data')
        }
        approval_file = self.create_approval_file('DB_INSERT', action_data)
        return {'status': 'pending_approval', 'approval_file': str(approval_file)}

    def requires_approval(self, method):
        return method in ['insert', 'update', 'delete']
"""

if __name__ == "__main__":
    # Test your server
    server = TemplateMCPServer()
    server.run()
