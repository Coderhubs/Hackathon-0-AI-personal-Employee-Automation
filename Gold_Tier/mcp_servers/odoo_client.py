#!/usr/bin/env python3
"""
Odoo JSON-RPC Client
Helper class for connecting to Odoo Community Edition via XML-RPC
"""

import xmlrpc.client
from typing import List, Dict, Any, Optional

class OdooClient:
    """
    Client for Odoo JSON-RPC API.

    Provides methods for authentication and CRUD operations.
    """

    def __init__(self, url: str, db: str, username: str, password: str):
        """
        Initialize Odoo client.

        Args:
            url: Odoo server URL (e.g., 'http://localhost:8069')
            db: Database name
            username: Username (usually email)
            password: Password
        """
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None

        # XML-RPC endpoints
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    def authenticate(self) -> bool:
        """
        Authenticate with Odoo server.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.uid = self.common.authenticate(
                self.db,
                self.username,
                self.password,
                {}
            )
            return self.uid is not None
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def execute_kw(self, model: str, method: str, args: List, kwargs: Dict = None) -> Any:
        """
        Execute Odoo model method.

        Args:
            model: Model name (e.g., 'res.partner', 'account.move')
            method: Method name (e.g., 'search', 'read', 'create')
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Method result
        """
        if kwargs is None:
            kwargs = {}

        if not self.uid:
            if not self.authenticate():
                raise Exception("Authentication required")

        return self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            model,
            method,
            args,
            kwargs
        )

    def search(self, model: str, domain: List = None, limit: int = None) -> List[int]:
        """
        Search for records.

        Args:
            model: Model name
            domain: Search domain (e.g., [('name', '=', 'John')])
            limit: Maximum number of results

        Returns:
            List of record IDs
        """
        if domain is None:
            domain = []

        kwargs = {}
        if limit:
            kwargs['limit'] = limit

        return self.execute_kw(model, 'search', [domain], kwargs)

    def read(self, model: str, ids: List[int], fields: List[str] = None) -> List[Dict]:
        """
        Read records by ID.

        Args:
            model: Model name
            ids: List of record IDs
            fields: List of field names to read

        Returns:
            List of record dictionaries
        """
        kwargs = {}
        if fields:
            kwargs['fields'] = fields

        return self.execute_kw(model, 'read', [ids], kwargs)

    def search_read(self, model: str, domain: List = None, fields: List[str] = None,
                    limit: int = None) -> List[Dict]:
        """
        Search and read records in one call.

        Args:
            model: Model name
            domain: Search domain
            fields: List of field names to read
            limit: Maximum number of results

        Returns:
            List of record dictionaries
        """
        if domain is None:
            domain = []

        kwargs = {}
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit

        return self.execute_kw(model, 'search_read', [domain], kwargs)

    def create(self, model: str, values: Dict) -> int:
        """
        Create a new record.

        Args:
            model: Model name
            values: Dictionary of field values

        Returns:
            ID of created record
        """
        return self.execute_kw(model, 'create', [values])

    def write(self, model: str, ids: List[int], values: Dict) -> bool:
        """
        Update existing records.

        Args:
            model: Model name
            ids: List of record IDs to update
            values: Dictionary of field values to update

        Returns:
            True if successful
        """
        return self.execute_kw(model, 'write', [ids, values])

    def unlink(self, model: str, ids: List[int]) -> bool:
        """
        Delete records.

        Args:
            model: Model name
            ids: List of record IDs to delete

        Returns:
            True if successful
        """
        return self.execute_kw(model, 'unlink', [ids])

    def create_invoice(self, partner_id: int, amount: float, description: str) -> int:
        """
        Create a customer invoice.

        Args:
            partner_id: Customer ID
            amount: Invoice amount
            description: Invoice description

        Returns:
            Invoice ID
        """
        invoice_vals = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': description,
                'quantity': 1,
                'price_unit': amount,
            })]
        }

        return self.create('account.move', invoice_vals)

    def create_customer(self, name: str, email: str = None, phone: str = None) -> int:
        """
        Create a customer.

        Args:
            name: Customer name
            email: Customer email
            phone: Customer phone

        Returns:
            Customer ID
        """
        customer_vals = {
            'name': name,
            'customer_rank': 1,
        }

        if email:
            customer_vals['email'] = email
        if phone:
            customer_vals['phone'] = phone

        return self.create('res.partner', customer_vals)

    def get_version(self) -> Dict:
        """
        Get Odoo server version info.

        Returns:
            Version information dictionary
        """
        return self.common.version()

# Example usage
if __name__ == "__main__":
    # Test connection
    client = OdooClient(
        url='http://localhost:8069',
        db='demo',
        username='admin',
        password='admin'
    )

    if client.authenticate():
        print("✓ Connected to Odoo")
        print(f"User ID: {client.uid}")

        # Get version
        version = client.get_version()
        print(f"Odoo version: {version.get('server_version')}")

        # Search customers
        customers = client.search_read(
            'res.partner',
            domain=[('customer_rank', '>', 0)],
            fields=['name', 'email'],
            limit=5
        )
        print(f"\nFound {len(customers)} customers:")
        for customer in customers:
            print(f"  - {customer['name']} ({customer.get('email', 'no email')})")
    else:
        print("✗ Authentication failed")
