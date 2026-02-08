#!/usr/bin/env python3
"""
Email MCP Server
Handles Gmail integration with HITL approval for sending
"""

import json
import sys
from datetime import datetime
from pathlib import Path

class EmailServer:
    def __init__(self):
        self.base_dir = Path("Gold_Tier")
        self.pending_approval = self.base_dir / "Pending_Approval"
        self.pending_approval.mkdir(parents=True, exist_ok=True)

    def handle_request(self, request):
        """Handle MCP requests"""
        method = request.get('method')
        params = request.get('params', {})

        if method == 'send_email':
            return self.send_email(params)
        elif method == 'read_emails':
            return self.read_emails(params)
        elif method == 'get_status':
            return self.get_status()
        else:
            return {'error': f'Unknown method: {method}'}

    def send_email(self, params):
        """Send email (requires HITL approval)"""
        to = params.get('to', '')
        subject = params.get('subject', '')
        body = params.get('body', '')
        cc = params.get('cc', '')
        bcc = params.get('bcc', '')

        # Create approval request
        approval_file = self.pending_approval / f"EMAIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(approval_file, 'w') as f:
            f.write(f"""# Email - PENDING APPROVAL

**Created:** {datetime.now().isoformat()}
**Type:** Outgoing Email
**Status:** AWAITING HUMAN APPROVAL

## Email Details

**To:** {to}
**Subject:** {subject}
**CC:** {cc if cc else 'None'}
**BCC:** {bcc if bcc else 'None'}

## Body

{body}

## Actions
- [ ] Approve and send
- [ ] Reject
- [ ] Request revisions

---
*This email requires human approval before sending*
""")

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Email created and awaiting approval'
        }

    def read_emails(self, params):
        """Read emails from Gmail (no approval needed)"""
        max_results = params.get('max_results', 10)
        query = params.get('query', '')

        # This would integrate with Gmail API
        # For now, return placeholder
        return {
            'status': 'success',
            'message': 'Email reading would integrate with Gmail API',
            'emails': [],
            'note': 'Requires GMAIL_API_KEY environment variable'
        }

    def get_status(self):
        """Get server status"""
        return {
            'status': 'operational',
            'capabilities': ['send_email', 'read_emails'],
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main MCP server loop"""
    server = EmailServer()

    print("Email MCP Server started", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            error_response = {'error': str(e)}
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
