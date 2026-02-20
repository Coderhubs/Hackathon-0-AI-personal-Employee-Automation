#!/usr/bin/env python3
"""
Browser MCP Server
Provides web automation capabilities via Playwright
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

class BrowserServer:
    def __init__(self):
        self.base_dir = Path("AI_Employee_Vault")
        self.pending_approval = self.base_dir / "Pending_Approval"
        self.pending_approval.mkdir(parents=True, exist_ok=True)
        self.browser = None
        self.context = None
        self.page = None

    def handle_request(self, request):
        """Handle MCP requests"""
        method = request.get('method')
        params = request.get('params', {})

        if method == 'navigate':
            return self.navigate(params)
        elif method == 'click':
            return self.click(params)
        elif method == 'fill':
            return self.fill(params)
        elif method == 'screenshot':
            return self.screenshot(params)
        elif method == 'get_text':
            return self.get_text(params)
        elif method == 'get_status':
            return self.get_status()
        else:
            return {'error': f'Unknown method: {method}'}

    def navigate(self, params):
        """Navigate to URL"""
        url = params.get('url', '')

        if not url:
            return {'error': 'URL is required'}

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                title = page.title()
                browser.close()

                return {
                    'status': 'success',
                    'url': url,
                    'title': title,
                    'message': f'Navigated to {url}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def click(self, params):
        """Click element (requires approval for sensitive actions)"""
        selector = params.get('selector', '')
        url = params.get('url', '')

        # Create approval request for clicks
        approval_file = self.pending_approval / f"BROWSER_CLICK_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(approval_file, 'w') as f:
            f.write(f"""# Browser Click - PENDING APPROVAL

**Created:** {datetime.now().isoformat()}
**Type:** Browser Automation
**Status:** AWAITING HUMAN APPROVAL

## Action Details

**URL:** {url}
**Selector:** {selector}
**Action:** Click element

## Risk Assessment

Browser clicks can trigger actions like:
- Form submissions
- Payments
- Account changes
- Data deletion

## Actions
- [ ] Approve and execute
- [ ] Reject
- [ ] Request more information

---
*This action requires human approval before execution*
""")

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Browser click created and awaiting approval'
        }

    def fill(self, params):
        """Fill form field"""
        selector = params.get('selector', '')
        value = params.get('value', '')
        url = params.get('url', '')

        # Create approval request
        approval_file = self.pending_approval / f"BROWSER_FILL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(approval_file, 'w') as f:
            f.write(f"""# Browser Fill - PENDING APPROVAL

**Created:** {datetime.now().isoformat()}
**Type:** Browser Automation
**Status:** AWAITING HUMAN APPROVAL

## Action Details

**URL:** {url}
**Selector:** {selector}
**Value:** {value}

## Actions
- [ ] Approve and execute
- [ ] Reject

---
*This action requires human approval before execution*
""")

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Browser fill created and awaiting approval'
        }

    def screenshot(self, params):
        """Take screenshot (no approval needed)"""
        url = params.get('url', '')

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)

                screenshot_path = Path("Gold_Tier") / "Screenshots" / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)

                page.screenshot(path=str(screenshot_path))
                browser.close()

                return {
                    'status': 'success',
                    'screenshot_path': str(screenshot_path),
                    'message': 'Screenshot captured'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_text(self, params):
        """Get text from element (no approval needed)"""
        url = params.get('url', '')
        selector = params.get('selector', '')

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)

                text = page.locator(selector).inner_text()
                browser.close()

                return {
                    'status': 'success',
                    'text': text,
                    'message': 'Text extracted'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_status(self):
        """Get server status"""
        return {
            'status': 'operational',
            'capabilities': ['navigate', 'click', 'fill', 'screenshot', 'get_text'],
            'timestamp': datetime.now().isoformat(),
            'note': 'Sensitive actions require HITL approval'
        }

def main():
    """Main MCP server loop"""
    server = BrowserServer()

    print("Browser MCP Server started", file=sys.stderr)

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
