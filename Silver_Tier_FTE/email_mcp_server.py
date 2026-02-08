#!/usr/bin/env python3
"""
Email MCP Server for Silver Tier AI Employee
Handles email sending operations with approval workflow
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

class EmailMCPServer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.approved_folder = self.vault_path / "Approved"
        self.done_folder = self.vault_path / "Done"
        self.logs_folder = self.vault_path / "Logs"

        # Ensure folders exist
        self.approved_folder.mkdir(exist_ok=True)
        self.done_folder.mkdir(exist_ok=True)
        self.logs_folder.mkdir(exist_ok=True)

    def send_email(self, draft_file_path):
        """
        Simulate sending an email from an approved draft
        In production, this would use Gmail API or SMTP
        """
        try:
            draft_path = Path(draft_file_path)

            if not draft_path.exists():
                return {
                    "success": False,
                    "error": f"Draft file not found: {draft_file_path}"
                }

            # Read draft content
            with open(draft_path, 'r', encoding='utf-8') as f:
                draft_content = f.read()

            # Extract email details (simplified parsing)
            lines = draft_content.split('\n')
            to_address = None
            subject = None

            for line in lines:
                if line.startswith('To:'):
                    to_address = line.replace('To:', '').strip()
                elif line.startswith('Subject:'):
                    subject = line.replace('Subject:', '').strip()

            # Simulate email sending (in production, use Gmail API)
            timestamp = datetime.now().isoformat()

            # Log the "sent" email
            log_entry = {
                "timestamp": timestamp,
                "action": "email_send",
                "to": to_address,
                "subject": subject,
                "draft_file": str(draft_path.name),
                "status": "simulated_success",
                "note": "Production would use Gmail API"
            }

            # Write to log
            log_file = self.logs_folder / f"email_log_{datetime.now().strftime('%Y%m%d')}.json"

            # Append to log file
            logs = []
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)

            logs.append(log_entry)

            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)

            # Move draft to Done folder
            done_path = self.done_folder / draft_path.name
            draft_path.rename(done_path)

            return {
                "success": True,
                "message": f"Email simulated: {subject}",
                "to": to_address,
                "subject": subject,
                "timestamp": timestamp,
                "log_file": str(log_file)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def process_approved_drafts(self):
        """
        Process all drafts in the Approved folder
        """
        results = []

        # Find all draft files in Approved folder
        draft_files = list(self.approved_folder.glob("DRAFT_*.md"))

        if not draft_files:
            return {
                "success": True,
                "message": "No approved drafts to process",
                "processed": 0
            }

        for draft_file in draft_files:
            result = self.send_email(draft_file)
            results.append({
                "file": draft_file.name,
                "result": result
            })

        return {
            "success": True,
            "message": f"Processed {len(draft_files)} approved drafts",
            "processed": len(draft_files),
            "results": results
        }

    def get_capabilities(self):
        """
        Return MCP server capabilities
        """
        return {
            "name": "email-mcp",
            "version": "1.0.0",
            "capabilities": [
                "send_email",
                "process_approved_drafts",
                "log_email_activity"
            ],
            "description": "Email MCP server for Silver Tier AI Employee"
        }

def main():
    """
    MCP Server main entry point
    Handles JSON-RPC style requests
    """
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python email_mcp_server.py <vault_path>"
        }))
        sys.exit(1)

    vault_path = sys.argv[1]
    server = EmailMCPServer(vault_path)

    # Read command from stdin (MCP protocol)
    try:
        for line in sys.stdin:
            request = json.loads(line)

            method = request.get("method")
            params = request.get("params", {})

            if method == "capabilities":
                response = server.get_capabilities()
            elif method == "send_email":
                draft_file = params.get("draft_file")
                response = server.send_email(draft_file)
            elif method == "process_approved":
                response = server.process_approved_drafts()
            else:
                response = {
                    "error": f"Unknown method: {method}"
                }

            print(json.dumps(response))
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    # If run directly, process approved drafts
    if len(sys.argv) >= 2:
        vault_path = sys.argv[1]
        server = EmailMCPServer(vault_path)
        result = server.process_approved_drafts()
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python email_mcp_server.py <vault_path>")
        print("Example: python email_mcp_server.py ./Silver_Tier_FTE")
