"""
MCP Client Wrapper - Python interface to Node.js MCP email server
"""
import subprocess
import json
import logging
from pathlib import Path

logger = logging.getLogger('MCPClient')

def send_email_via_mcp(to: str, subject: str, body: str) -> dict:
    """
    Send email via MCP email server

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body (plain text or HTML)

    Returns:
        dict: {'success': bool, 'message': str, 'error': str (if failed)}
    """
    try:
        # Check if MCP server exists
        mcp_server_path = Path("mcp_servers/email-mcp/index.js")
        if not mcp_server_path.exists():
            logger.error(f"MCP email server not found at: {mcp_server_path}")
            return {
                'success': False,
                'error': 'MCP email server not found. Please ensure mcp_servers/email-mcp/index.js exists.'
            }

        # Prepare request
        request = {
            'method': 'tools/call',
            'params': {
                'name': 'send_email',
                'arguments': {
                    'to': to,
                    'subject': subject,
                    'body': body
                }
            }
        }

        logger.info(f"Sending email via MCP to: {to}")
        logger.debug(f"Subject: {subject}")

        # Call MCP server via subprocess
        result = subprocess.run(
            ['node', str(mcp_server_path)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse response
        if result.returncode == 0 and result.stdout:
            try:
                response = json.loads(result.stdout)
                logger.info(f"✓ Email sent successfully to {to}")
                return {
                    'success': True,
                    'message': f'Email sent to {to}',
                    'response': response
                }
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse MCP response: {e}")
                logger.debug(f"Raw output: {result.stdout}")
                return {
                    'success': False,
                    'error': f'Invalid JSON response from MCP server: {result.stdout[:200]}'
                }
        else:
            error_msg = result.stderr or result.stdout or 'Unknown error'
            logger.error(f"MCP server error: {error_msg}")
            return {
                'success': False,
                'error': f'MCP server failed: {error_msg[:200]}'
            }

    except subprocess.TimeoutExpired:
        logger.error("MCP server timeout (30s)")
        return {
            'success': False,
            'error': 'MCP server timeout after 30 seconds'
        }

    except FileNotFoundError:
        logger.error("Node.js not found. Please install Node.js.")
        return {
            'success': False,
            'error': 'Node.js not found. Please install Node.js to use email functionality.'
        }

    except Exception as e:
        logger.error(f"Unexpected error calling MCP server: {e}")
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def check_mcp_server_available() -> bool:
    """
    Check if MCP email server is available

    Returns:
        bool: True if server exists and Node.js is available
    """
    try:
        # Check if server file exists
        mcp_server_path = Path("mcp_servers/email-mcp/index.js")
        if not mcp_server_path.exists():
            return False

        # Check if Node.js is available
        result = subprocess.run(
            ['node', '--version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0

    except:
        return False
