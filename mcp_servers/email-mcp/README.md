# Email MCP Server

Email MCP server for AI Personal Employee - enables Claude Code to send emails via Gmail.

## Features

- **send_email**: Send emails via Gmail
- **draft_email**: Create email drafts (for HITL approval)

## Setup

1. Install dependencies:
```bash
cd mcp_servers/email-mcp
npm install
```

2. Configure in Claude Code:
Add to your `~/.config/claude-code/mcp.json`:
```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["path/to/mcp_servers/email-mcp/index.js"],
      "env": {
        "GMAIL_EMAIL": "your_email@gmail.com",
        "GMAIL_PASSWORD": "your_app_password"
      }
    }
  }
}
```

3. Test the server:
```bash
node index.js
```

## Usage in Claude Code

### Send Email
```javascript
// Claude can call this tool
await use_mcp_tool("email", "send_email", {
  to: "recipient@example.com",
  subject: "Test Email",
  body: "This is a test email from AI Personal Employee"
});
```

### Draft Email (for HITL approval)
```javascript
// Create draft first
await use_mcp_tool("email", "draft_email", {
  to: "recipient@example.com",
  subject: "Invoice for January",
  body: "Please find attached your invoice..."
});

// After human approval, send it
await use_mcp_tool("email", "send_email", {
  to: "recipient@example.com",
  subject: "Invoice for January",
  body: "Please find attached your invoice..."
});
```

## Security

- Uses Gmail App Passwords (not your main password)
- Credentials stored in environment variables
- Never commits credentials to git

## Troubleshooting

**Error: Invalid login**
- Make sure you're using an App Password, not your regular Gmail password
- Generate one at: https://myaccount.google.com/apppasswords

**Error: Less secure app access**
- Gmail requires App Passwords for third-party apps
- Enable 2FA first, then create App Password
