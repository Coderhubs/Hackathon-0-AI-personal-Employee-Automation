#!/usr/bin/env python3
"""
Odoo Watcher
Monitors Odoo for new invoices, expenses, and customers requiring attention
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from base_watcher import BaseWatcher
from mcp_servers.odoo_client import OdooClient
import os

class OdooWatcher(BaseWatcher):
    """
    Watches Odoo for items requiring attention:
    - Unpaid invoices
    - Pending expenses
    - New customers
    """

    def __init__(self):
        super().__init__(name="Odoo", interval_seconds=300)  # Check every 5 minutes

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

        # Track processed items
        self.processed_invoices = set()
        self.processed_customers = set()

    def watch(self):
        """Check Odoo for items requiring attention"""
        try:
            # Authenticate
            if not self.client.authenticate():
                self.logger.error("Failed to authenticate with Odoo")
                return False

            self.logger.info(f"Connected to Odoo at {self.odoo_url}")

            # Check for unpaid invoices
            self.check_unpaid_invoices()

            # Check for new customers
            self.check_new_customers()

            return True

        except Exception as e:
            self.logger.error(f"Error watching Odoo: {e}")
            return False

    def check_unpaid_invoices(self):
        """Check for unpaid invoices"""
        try:
            # Search for posted invoices that are not paid
            invoices = self.client.search_read(
                'account.move',
                domain=[
                    ('move_type', '=', 'out_invoice'),
                    ('state', '=', 'posted'),
                    ('payment_state', 'in', ['not_paid', 'partial'])
                ],
                fields=['name', 'partner_id', 'amount_total', 'invoice_date', 'invoice_date_due'],
                limit=20
            )

            for invoice in invoices:
                invoice_id = invoice['id']

                # Skip if already processed
                if invoice_id in self.processed_invoices:
                    continue

                # Check if overdue
                due_date = invoice.get('invoice_date_due')
                is_overdue = False
                if due_date:
                    from datetime import date
                    due = datetime.strptime(due_date, '%Y-%m-%d').date()
                    is_overdue = due < date.today()

                # Create task file for unpaid/overdue invoices
                if is_overdue:
                    self.create_task_file({
                        'type': 'unpaid_invoice',
                        'invoice_id': invoice_id,
                        'invoice_name': invoice['name'],
                        'customer': invoice['partner_id'][1] if invoice.get('partner_id') else 'Unknown',
                        'amount': invoice['amount_total'],
                        'due_date': due_date,
                        'status': 'OVERDUE'
                    })
                    self.processed_invoices.add(invoice_id)
                    self.logger.info(f"Created task for overdue invoice: {invoice['name']}")

        except Exception as e:
            self.logger.error(f"Error checking unpaid invoices: {e}")

    def check_new_customers(self):
        """Check for recently created customers"""
        try:
            # Search for customers created in last 24 hours
            from datetime import timedelta
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

            customers = self.client.search_read(
                'res.partner',
                domain=[
                    ('customer_rank', '>', 0),
                    ('create_date', '>=', yesterday)
                ],
                fields=['name', 'email', 'phone', 'city', 'create_date'],
                limit=10
            )

            for customer in customers:
                customer_id = customer['id']

                # Skip if already processed
                if customer_id in self.processed_customers:
                    continue

                # Create task file for new customer
                self.create_task_file({
                    'type': 'new_customer',
                    'customer_id': customer_id,
                    'name': customer['name'],
                    'email': customer.get('email', 'Not provided'),
                    'phone': customer.get('phone', 'Not provided'),
                    'city': customer.get('city', 'Not provided'),
                    'created': customer.get('create_date', 'Unknown')
                })
                self.processed_customers.add(customer_id)
                self.logger.info(f"Created task for new customer: {customer['name']}")

        except Exception as e:
            self.logger.error(f"Error checking new customers: {e}")

    def create_task_file(self, data):
        """Create task file in Inbox"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task_type = data.get('type', 'odoo_task')

        filename = f"ODOO_{task_type.upper()}_{timestamp}.txt"
        filepath = self.inbox / filename

        # Build content
        content = f"=== Odoo Task: {task_type.replace('_', ' ').title()} ===\n"
        content += f"Created: {datetime.now().isoformat()}\n"
        content += f"Source: Odoo ({self.odoo_url})\n\n"

        for key, value in data.items():
            if key != 'type':
                content += f"{key.replace('_', ' ').title()}: {value}\n"

        content += f"\n--- End of Odoo Task ---\n"

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.info(f"Created task file: {filename}")
        return filepath

if __name__ == "__main__":
    watcher = OdooWatcher()
    watcher.run()
