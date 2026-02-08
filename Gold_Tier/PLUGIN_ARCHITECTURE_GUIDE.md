# Plugin Architecture Guide

## Overview

The Gold Tier system uses a plugin architecture that allows you to add new watchers and MCP servers without modifying the core system. This guide explains how to create and integrate plugins.

---

## Architecture Components

### 1. Plugin Manager (`plugin_manager.py`)
- Discovers and manages watcher plugins
- Loads configuration from `Config/watchers_config.json`
- Starts/stops watchers dynamically
- Supports auto-discovery of new watchers

### 2. Base Classes
- **BaseWatcher** (`base_watcher.py`) - Template for watcher plugins
- **BaseMCPServer** (`mcp_servers/base_mcp_server.py`) - Template for MCP servers

### 3. Configuration Files
- **watchers_config.json** - Watcher plugin configuration
- **mcp_config.json** - MCP server configuration

---

## Creating a New Watcher Plugin

### Step 1: Copy Template

```bash
cd Gold_Tier
cp watcher_template.py mynewservice_watcher.py
```

### Step 2: Implement Your Watcher

```python
from base_watcher import BaseWatcher

class MyNewServiceWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(
            name="MyNewService",
            interval_seconds=300,  # Check every 5 minutes
            base_dir="Gold_Tier"
        )
        # Your initialization
        self.api_key = os.getenv('MYNEWSERVICE_API_KEY')

    def watch(self):
        """Check for new content"""
        data = self.fetch_from_api()
        if data:
            self.create_task_file(data)
        return True

    def fetch_from_api(self):
        """Your API logic here"""
        # Call your API, return data or None
        pass

    def create_task_file(self, data):
        """Create task file in Inbox"""
        filename = self.generate_filename("MYNEWSERVICE")
        filepath = self.inbox / filename
        content = json.dumps(data, indent=2)
        return self.write_file(filepath, content)

if __name__ == "__main__":
    watcher = MyNewServiceWatcher()
    watcher.run()
```

### Step 3: Test Your Watcher

```bash
python mynewservice_watcher.py
```

### Step 4: Add to Configuration (Optional)

If auto-discovery is enabled, your watcher will be automatically detected. Otherwise, add to `Config/watchers_config.json`:

```json
{
  "watchers": [
    {
      "name": "MyNewService Watcher",
      "script": "mynewservice_watcher.py",
      "enabled": true,
      "description": "Monitors MyNewService API",
      "interval_seconds": 300
    }
  ]
}
```

### Step 5: Restart System

```bash
start_gold_tier_plugins.bat
```

Your watcher is now integrated!

---

## Creating a New MCP Server Plugin

### Step 1: Copy Template

```bash
cd Gold_Tier/mcp_servers
cp mcp_template.py mynewservice_server.py
```

### Step 2: Implement Your Server

```python
from mcp_servers.base_mcp_server import BaseMCPServer
import os

class MyNewServiceServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="MyNewService")
        self.api_key = os.getenv('MYNEWSERVICE_API_KEY')

    def register_methods(self):
        """Register supported methods"""
        self.methods['send_message'] = self.send_message
        self.methods['get_messages'] = self.get_messages
        self.methods['get_status'] = self.get_status

    def send_message(self, params):
        """Send message (requires approval)"""
        message = params.get('message', '')
        recipient = params.get('recipient', '')

        action_data = {
            'action': 'send_message',
            'recipient': recipient,
            'message': message
        }

        approval_file = self.create_approval_file('MYNEWSERVICE_MESSAGE', action_data)

        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file),
            'message': 'Message created and awaiting approval'
        }

    def get_messages(self, params):
        """Get messages (no approval needed)"""
        # Your API logic here
        return {
            'status': 'success',
            'messages': []
        }

    def requires_approval(self, method):
        """Specify which methods need approval"""
        return method == 'send_message'

if __name__ == "__main__":
    server = MyNewServiceServer()
    server.run()
```

### Step 3: Test Your Server

```bash
echo '{"method":"get_status"}' | python mcp_servers/mynewservice_server.py
```

### Step 4: Add to MCP Configuration

Edit `Config/mcp_config.json`:

```json
{
  "mcpServers": {
    "mynewservice": {
      "command": "python",
      "args": ["Gold_Tier/mcp_servers/mynewservice_server.py"],
      "description": "MyNewService integration",
      "env": {
        "MYNEWSERVICE_API_KEY": "${MYNEWSERVICE_API_KEY}"
      }
    }
  }
}
```

### Step 5: Set Environment Variables

```bash
set MYNEWSERVICE_API_KEY=your_api_key_here
```

Your MCP server is now integrated!

---

## Plugin Features

### Automatic Error Recovery

All watchers inherit error recovery with exponential backoff:
- Retry failed operations: 1s, 2s, 4s, 8s, 16s
- Max 5 retries before extended wait
- All errors logged automatically

### Automatic Logging

All plugins automatically log to `Gold_Tier/Logs/`:
- `{name}_watcher.log` for watchers
- Console output for MCP servers

### Human-in-the-Loop (HITL)

MCP servers can easily create approval files:

```python
approval_file = self.create_approval_file('ACTION_TYPE', {
    'field1': 'value1',
    'field2': 'value2'
})
```

This creates a markdown file in `Pending_Approval/` with checkboxes for approval.

---

## Plugin Discovery

### Auto-Discovery (Enabled by Default)

The system automatically discovers new watchers matching the pattern `*_watcher.py`.

To disable auto-discovery, edit `Config/watchers_config.json`:

```json
{
  "plugin_discovery": {
    "enabled": false
  }
}
```

### Manual Discovery

List all plugins:

```bash
python plugin_manager.py list
```

Add a watcher manually:

```bash
python plugin_manager.py add-watcher --name "My Watcher" --script "my_watcher.py" --interval 300
```

---

## Best Practices

### Watcher Plugins

1. **Use meaningful prefixes** for task files (e.g., "SLACK_", "DISCORD_")
2. **Set appropriate intervals** - don't poll too frequently
3. **Handle API rate limits** in your fetch logic
4. **Return True/False** from watch() to indicate success/failure
5. **Use self.logger** for all logging

### MCP Server Plugins

1. **Require approval for sensitive actions** (sending, deleting, posting)
2. **Don't require approval for read operations** (fetching, querying)
3. **Validate parameters** before creating approval files
4. **Return consistent response format** (status, message, data)
5. **Handle errors gracefully** and return error dicts

### Security

1. **Use environment variables** for API keys and credentials
2. **Never hardcode secrets** in plugin code
3. **Validate all input** from params
4. **Log security-relevant events**
5. **Use HTTPS** for all API calls

---

## Example Plugins

### Slack Watcher

```python
from base_watcher import BaseWatcher
import requests
import os

class SlackWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(name="Slack", interval_seconds=60)
        self.token = os.getenv('SLACK_TOKEN')
        self.channel = os.getenv('SLACK_CHANNEL', 'general')

    def watch(self):
        messages = self.fetch_messages()
        for msg in messages:
            self.create_task_file(msg)
        return True

    def fetch_messages(self):
        response = requests.get(
            'https://slack.com/api/conversations.history',
            headers={'Authorization': f'Bearer {self.token}'},
            params={'channel': self.channel, 'limit': 10}
        )
        return response.json().get('messages', [])

    def create_task_file(self, message):
        filename = self.generate_filename("SLACK")
        filepath = self.inbox / filename
        content = f"User: {message.get('user')}\n{message.get('text')}"
        return self.write_file(filepath, content)
```

### Discord MCP Server

```python
from mcp_servers.base_mcp_server import BaseMCPServer
import os

class DiscordServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="Discord")
        self.token = os.getenv('DISCORD_TOKEN')

    def register_methods(self):
        self.methods['send_message'] = self.send_message
        self.methods['get_status'] = self.get_status

    def send_message(self, params):
        action_data = {
            'channel': params.get('channel'),
            'message': params.get('message')
        }
        approval_file = self.create_approval_file('DISCORD_MESSAGE', action_data)
        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file)
        }

    def requires_approval(self, method):
        return method == 'send_message'
```

---

## Troubleshooting

### Watcher Not Starting

1. Check `Config/watchers_config.json` - is it enabled?
2. Check file naming - does it match `*_watcher.py`?
3. Check logs in `Gold_Tier/Logs/`
4. Test manually: `python your_watcher.py`

### MCP Server Not Responding

1. Check `Config/mcp_config.json` - is it configured?
2. Check environment variables are set
3. Test manually: `echo '{"method":"get_status"}' | python mcp_servers/your_server.py`
4. Check for import errors

### Plugin Not Auto-Discovered

1. Check filename matches pattern `*_watcher.py`
2. Check not in exclude list
3. Check auto-discovery is enabled
4. Run: `python plugin_manager.py list`

---

## Plugin Manager CLI

```bash
# List all plugins
python plugin_manager.py list

# Start all enabled watchers
python plugin_manager.py start

# Add new watcher
python plugin_manager.py add-watcher --name "My Watcher" --script "my_watcher.py" --interval 300
```

---

## Summary

The plugin architecture allows you to:

✅ Add new watchers without modifying core code
✅ Add new MCP servers without modifying core code
✅ Auto-discover new plugins on startup
✅ Inherit error recovery and logging automatically
✅ Use HITL approval workflow easily
✅ Configure plugins via JSON files

**To add a new integration:**
1. Copy template
2. Implement 2-3 methods
3. Test
4. Restart system
5. Done!

---

*Gold Tier Autonomous System - Plugin Architecture*
