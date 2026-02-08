# Plugin Architecture - Complete System Overview

## 🎯 What Was Built

The Gold Tier system now includes a **fully extensible plugin architecture** that allows you to add new watchers and MCP servers without modifying any core code.

---

## 🏗️ Architecture Components

### Core Plugin System

1. **plugin_manager.py** - Plugin discovery and management
   - Auto-discovers watcher plugins
   - Loads configuration dynamically
   - Starts/stops plugins
   - CLI for plugin management

2. **base_watcher.py** - Base class for all watchers
   - Standardized interface
   - Built-in error recovery (exponential backoff)
   - Automatic logging
   - Helper methods for file creation

3. **base_mcp_server.py** - Base class for all MCP servers
   - Standardized interface
   - Built-in HITL approval workflow
   - Method registration system
   - Automatic error handling

### Templates

4. **watcher_template.py** - Template for creating new watchers
   - Copy and customize
   - Includes examples and documentation
   - Ready to use

5. **mcp_template.py** - Template for creating new MCP servers
   - Copy and customize
   - Includes examples and documentation
   - Ready to use

### Configuration

6. **watchers_config.json** - Watcher plugin configuration
   - Enable/disable watchers
   - Set intervals
   - Auto-discovery settings

7. **mcp_config.json** - MCP server configuration
   - Server definitions
   - Environment variables
   - Command configuration

### Example Plugins

8. **slack_watcher.py** - Example watcher plugin
   - Demonstrates API integration
   - Shows error handling
   - Includes demo mode

9. **discord_server.py** - Example MCP server plugin
   - Demonstrates method registration
   - Shows HITL approval workflow
   - Includes demo mode

### Documentation

10. **PLUGIN_ARCHITECTURE_GUIDE.md** - Comprehensive guide
11. **PLUGIN_QUICKSTART.md** - 5-minute quick start

---

## 🚀 How It Works

### Adding a New Watcher (5 Minutes)

```bash
# 1. Copy template
cp watcher_template.py twitter_watcher.py

# 2. Edit file (implement watch() and create_task_file())
# 3. Test
python twitter_watcher.py

# 4. Restart system
start_gold_tier_plugins.bat
```

**That's it!** Your watcher is now integrated. No core code changes needed.

### Adding a New MCP Server (5 Minutes)

```bash
# 1. Copy template
cp mcp_servers/mcp_template.py mcp_servers/telegram_server.py

# 2. Edit file (implement register_methods() and your methods)
# 3. Add to Config/mcp_config.json
# 4. Set environment variables
# 5. Restart system
```

**That's it!** Your MCP server is now integrated. No core code changes needed.

---

## 🎨 Design Principles

### 1. Zero Core Modification
- Add new plugins without touching core code
- Core system remains stable
- Plugins are isolated

### 2. Auto-Discovery
- New watchers automatically detected
- Pattern-based discovery (*_watcher.py)
- Optional manual configuration

### 3. Standardized Interface
- All watchers inherit from BaseWatcher
- All MCP servers inherit from BaseMCPServer
- Consistent behavior across plugins

### 4. Built-in Features
- Error recovery (exponential backoff)
- Automatic logging
- HITL approval workflow
- Configuration management

### 5. Easy Testing
- Each plugin can run standalone
- Demo modes for development
- Clear error messages

---

## 📊 Plugin Lifecycle

### Watcher Plugin Lifecycle

```
1. Create plugin file (*_watcher.py)
   ↓
2. Auto-discovered by plugin_manager.py
   ↓
3. Loaded from watchers_config.json
   ↓
4. Started by start_gold_tier_plugins.bat
   ↓
5. Runs continuously with error recovery
   ↓
6. Creates task files in Inbox/
   ↓
7. Autonomous monitor processes tasks
```

### MCP Server Plugin Lifecycle

```
1. Create server file (mcp_servers/*_server.py)
   ↓
2. Add to mcp_config.json
   ↓
3. Set environment variables
   ↓
4. Server available to autonomous monitor
   ↓
5. Receives method calls via JSON-RPC
   ↓
6. Creates approval files for HITL
   ↓
7. Executes approved actions
```

---

## 🔧 Plugin Manager CLI

```bash
# List all plugins
python plugin_manager.py list

# Start all enabled watchers
python plugin_manager.py start

# Add new watcher
python plugin_manager.py add-watcher \
  --name "Twitter Watcher" \
  --script "twitter_watcher.py" \
  --interval 300
```

---

## 📝 Configuration Files

### watchers_config.json

```json
{
  "watchers": [
    {
      "name": "Gmail Watcher",
      "script": "gmail_watcher.py",
      "enabled": true,
      "description": "Monitors Gmail",
      "interval_seconds": 180
    }
  ],
  "plugin_discovery": {
    "enabled": true,
    "pattern": "*_watcher.py",
    "exclude": ["base_watcher.py", "watcher_template.py"]
  }
}
```

### mcp_config.json

```json
{
  "mcpServers": {
    "discord": {
      "command": "python",
      "args": ["Gold_Tier/mcp_servers/discord_server.py"],
      "description": "Discord integration",
      "env": {
        "DISCORD_WEBHOOK_URL": "${DISCORD_WEBHOOK_URL}"
      }
    }
  }
}
```

---

## 🎯 Example: Adding Slack Integration

### Step 1: Create Watcher (Already Done!)

File: `slack_watcher.py`
- Monitors Slack channels
- Creates task files for new messages
- Includes demo mode

### Step 2: Create MCP Server (5 minutes)

```python
from mcp_servers.base_mcp_server import BaseMCPServer

class SlackServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="Slack")
        self.token = os.getenv('SLACK_TOKEN')

    def register_methods(self):
        self.methods['send_message'] = self.send_message
        self.methods['get_status'] = self.get_status

    def send_message(self, params):
        action_data = {
            'channel': params.get('channel'),
            'message': params.get('message')
        }
        approval_file = self.create_approval_file('SLACK_MESSAGE', action_data)
        return {
            'status': 'pending_approval',
            'approval_file': str(approval_file)
        }

    def requires_approval(self, method):
        return method == 'send_message'
```

### Step 3: Configure

Add to `Config/mcp_config.json`:
```json
{
  "slack": {
    "command": "python",
    "args": ["Gold_Tier/mcp_servers/slack_server.py"],
    "description": "Slack integration",
    "env": {"SLACK_TOKEN": "${SLACK_TOKEN}"}
  }
}
```

### Step 4: Test

```bash
# Test watcher
python slack_watcher.py

# Test MCP server
echo '{"method":"get_status"}' | python mcp_servers/slack_server.py

# Start system
start_gold_tier_plugins.bat
```

**Done!** Slack is now fully integrated.

---

## 🔒 Security Features

### Environment Variables
- All credentials via environment variables
- Never hardcoded in plugins
- Secure credential management

### HITL Approval
- Sensitive actions require approval
- Approval files in Pending_Approval/
- Clear audit trail

### Input Validation
- All parameters validated
- Error handling built-in
- Safe defaults

---

## 📈 Benefits

### For Developers
✅ Add integrations in 5 minutes
✅ No core code changes
✅ Standardized interface
✅ Built-in error recovery
✅ Automatic logging
✅ Easy testing

### For System
✅ Core remains stable
✅ Plugins are isolated
✅ Easy to maintain
✅ Scalable architecture
✅ Clear separation of concerns

### For Users
✅ Easy to extend
✅ No system downtime
✅ Clear documentation
✅ Working examples
✅ Demo modes for testing

---

## 🎓 Learning Path

### Beginner
1. Read PLUGIN_QUICKSTART.md
2. Test slack_watcher.py in demo mode
3. Test discord_server.py in demo mode
4. Understand the workflow

### Intermediate
1. Read PLUGIN_ARCHITECTURE_GUIDE.md
2. Copy watcher_template.py
3. Implement a simple watcher
4. Test and integrate

### Advanced
1. Study base_watcher.py and base_mcp_server.py
2. Create complex integrations
3. Add custom error handling
4. Contribute plugins

---

## 🔄 Integration with Core System

### Autonomous Monitor
- Processes task files from all watchers
- Calls MCP servers as needed
- Handles approval workflow
- No changes needed for new plugins

### Dashboard
- Shows all active watchers
- Displays plugin status
- Tracks queue metrics
- Auto-updates

### Error Recovery
- All plugins inherit error recovery
- Exponential backoff
- Automatic retry
- Comprehensive logging

---

## 📦 What's Included

### Core Files (5)
- plugin_manager.py
- base_watcher.py
- base_mcp_server.py
- watcher_template.py
- mcp_template.py

### Configuration (2)
- watchers_config.json
- mcp_config.json (updated)

### Examples (2)
- slack_watcher.py
- discord_server.py

### Documentation (2)
- PLUGIN_ARCHITECTURE_GUIDE.md
- PLUGIN_QUICKSTART.md

### Scripts (1)
- start_gold_tier_plugins.bat

**Total: 12 new files for complete plugin architecture**

---

## 🚀 Quick Start

### Test Example Plugins

```bash
# Test Slack watcher (demo mode)
python slack_watcher.py

# Test Discord server (demo mode)
echo '{"method":"get_status"}' | python mcp_servers/discord_server.py

# List all plugins
python plugin_manager.py list

# Start system with plugins
start_gold_tier_plugins.bat
```

### Create Your First Plugin

```bash
# Copy template
cp watcher_template.py myservice_watcher.py

# Edit file (implement 2 methods)
# Test
python myservice_watcher.py

# Restart system
start_gold_tier_plugins.bat
```

---

## 🎉 Summary

The Gold Tier system now has a **fully extensible plugin architecture** that allows:

✅ **Add watchers in 5 minutes** - Copy template, implement 2 methods, done
✅ **Add MCP servers in 5 minutes** - Copy template, implement methods, done
✅ **Zero core modifications** - Plugins are completely isolated
✅ **Auto-discovery** - New plugins automatically detected
✅ **Built-in features** - Error recovery, logging, HITL approval
✅ **Working examples** - Slack and Discord plugins included
✅ **Complete documentation** - Guides and quick starts

**The system is now truly extensible and ready for unlimited integrations.**

---

*Gold Tier Autonomous System - Plugin Architecture Complete*
