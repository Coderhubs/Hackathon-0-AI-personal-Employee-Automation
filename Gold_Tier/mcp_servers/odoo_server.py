#!/usr/bin/env python3
"""
Odoo MCP Server
Integrates with Odoo Community Edition via JSON-RPC for accounting operations
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from base_mcp_server import BaseMCPServer
from odoo_client import OdooClient

class OdooMCPServer(BaseMCPServer):
    """
    MCP Server for Odoo Community Edition integration.

    Provides methods for:
    - Creating invoices
    - Creating customers
    - Creating expenses
    - Querying invoices and customers

    All write operations require HITL approval.
    """

    def __init__(self):
        super().__init__(name="Odoo")

        # Initialize Odoo client
        self.odoo_url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.odoo_db = os.getenv('ODOO_DB', 'demo')
        self.odoo_username = os.getenv('ODOO_USERNAME', 'admin')
        self.odoo_password = os.getenv('ODOO_PASSWORD', 'admin')

        self.client = OdooClient(
            url=self.odoo_url,
            db=self.odoo_db,
            username=self.odoo_username,
            password=self.odoo_password
        )

    def register_methods(self):
        """Register Odoo-specific methods"""
        self.methods['create_invoice'] = self.create_invoice
        self.methods['create_customer'] = self.create_customer
        self.methods['create_expense'] = self.create_expense
        self.methods['get_invoices'] = self.get_invoices
        self.methods['get_customers'] = self.get_customers
        self.methods['get_status'] = self.get_status
        self.methods['test_connection'] = self.test_connection

    def test_connection(self, params):
        """Test connection to Odoo"""
        try:
            if self.client.authenticate():
                return {
                    'status': 'success',
                    'message': 'Connected to Odoo successfully',
                    'url': self.odoo_url,
                    'database': self.odoo_db,
                    'user_id': self.client.uid
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Authentication failed'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}'
            }

    def create_invoice(self, params):
        """
        Create invoice in Odoo (requires approval).

        Args:
            params: {
                'customer_name': str,
                'amount': float,
                'description': str,
                'due_date': str (optional)
            }
        """
        customer_name = params.get('customer_name', 'Unknown Customer')
        amount = params.get('amount', 0.0)
        description = params.get('description', 'Service')
        due_date = params.get('due_date', '')

        # Create approval file
        action_data = {
            'action': 'create_invoice',
            'customer_name': customer_name,
            'amount': f'${amount:.2f}',
            'description': description,
            'due_date': due_date if due_date else 'Not specified',
            'odoo_url': self.odoo_url,
            'database': self.odoo_db
        }

        approval_file = self.create_approval_file('ODOO_INVOICE', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Invoice for {customer_name} (${amount:.2f}) created and awaiting approval'
        }

    def create_customer(self, params):
        """
        Create customer in Odoo (requires approval).

        Args:
            params: {
                'name': str,
                'email': str,
                'phone': str (optional),
                'address': str (optional)
            }
        """
        name = params.get('name', 'Unknown')
        email = params.get('email', '')
        phone = params.get('phone', '')
        address = params.get('address', '')

        # Create approval file
        action_data = {
            'action': 'create_customer',
            'name': name,
            'email': email,
            'phone': phone if phone else 'Not provided',
            'address': address if address else 'Not provided',
            'odoo_url': self.odoo_url,
            'database': self.odoo_db
        }

        approval_file = self.create_approval_file('ODOO_CUSTOMER', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Customer {name} created and awaiting approval'
        }

    def create_expense(self, params):
        """
        Create expense in Odoo (requires approval).

        Args:
            params: {
                'amount': float,
                'category': str,
                'description': str,
                'date': str (optional)
            }
        """
        amount = params.get('amount', 0.0)
        category = params.get('category', 'General')
        description = params.get('description', 'Expense')
        date = params.get('date', '')

        # Create approval file
        action_data = {
            'action': 'create_expense',
            'amount': f'${amount:.2f}',
            'category': category,
            'description': description,
            'date': date if date else 'Today',
            'odoo_url': self.odoo_url,
            'database': self.odoo_db
        }

        approval_file = self.create_approval_file('ODOO_EXPENSE', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': f'Expense ${amount:.2f} ({category}) created and awaiting approval'
        }

    def get_invoices(self, params):
        """
        Get invoices from Odoo (read-only, no approval needed).

        Args:
            params: {
                'status': str (optional) - 'draft', 'posted', 'paid'
                'limit': int (optional) - max number of invoices
            }
        """
        try:
            status = params.get('status', 'all')
            limit = params.get('limit', 10)

            # Authenticate
            if not self.client.authenticate():
                return {
                    'status': 'error',
                    'message': 'Authentication failed'
                }

            # Query invoices
            invoices = self.client.search_read(
                'account.move',
                domain=[('move_type', '=', 'out_invoice')],
                fields=['name', 'partner_id', 'amount_total', 'state', 'invoice_date'],
                limit=limit
            )

            return {
                'status': 'success',
                'count': len(invoices),
                'invoices': invoices
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get invoices: {str(e)}'
            }

    def get_customers(self, params):
        """
        Get customers from Odoo (read-only, no approval needed).

        Args:
            params: {
                'limit': int (optional) - max number of customers
            }
        """
        try:
            limit = params.get('limit', 10)

            # Authenticate
            if not self.client.authenticate():
                return {
                    'status': 'error',
                    'message': 'Authentication failed'
                }

            # Query customers
            customers = self.client.search_read(
                'res.partner',
                domain=[('customer_rank', '>', 0)],
                fields=['name', 'email', 'phone', 'city'],
                limit=limit
            )

            return {
                'status': 'success',
                'count': len(customers),
                'customers': customers
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get customers: {str(e)}'
            }

    def requires_approval(self, method):
        """
        Specify which methods require HITL approval.

        Read operations don't need approval.
        Write operations (create_*) require approval.
        """
        read_methods = ['get_invoices', 'get_customers', 'get_status', 'test_connection']
        return method not in read_methods

if __name__ == "__main__":
    server = OdooMCPServer()
    server.run()
