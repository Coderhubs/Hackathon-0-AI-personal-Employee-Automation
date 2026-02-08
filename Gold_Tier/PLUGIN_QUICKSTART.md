# Plugin Development Quick Start

## Create a New Watcher in 5 Minutes

### 1. Copy Template
```bash
cd Gold_Tier
cp watcher_template.py twitter_watcher.py
```

### 2. Edit File
```python
from base_watcher import BaseWatcher
import tweepy
import os

class TwitterWatcher(BaseWatcher):
    def __init__(self):
        super().__init__(name="Twitter", interval_seconds=180)
        self.api = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    def watch(self):
        tweets = self.api.search_recent_tweets(query="your_query", max_results=10)
        for tweet in tweets.data or []:
            self.create_task_file(tweet)
        return True

    def create_task_file(self, tweet):
        filename = self.generate_filename("TWITTER")
        filepath = self.inbox / filename
        content = f"Tweet ID: {tweet.id}\n{tweet.text}"
        return self.write_file(filepath, content)

if __name__ == "__main__":
    watcher = TwitterWatcher()
    watcher.run()
```

### 3. Test
```bash
python twitter_watcher.py
```

### 4. Done!
Restart system - your watcher is now integrated.

---

## Create a New MCP Server in 5 Minutes

### 1. Copy Template
```bash
cd Gold_Tier/mcp_servers
cp mcp_template.py slack_server.py
```

### 2. Edit File
```python
from mcp_servers.base_mcp_server import BaseMCPServer
import requests
import os

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
        return {'status': 'pending_approval', 'approval_file': str(approval_file)}

    def requires_approval(self, method):
        return method == 'send_message'

if __name__ == "__main__":
    server = SlackServer()
    server.run()
```

### 3. Add to Config
Edit `Config/mcp_config.json`:
```json
{
  "mcpServers": {
    "slack": {
      "command": "python",
      "args": ["Gold_Tier/mcp_servers/slack_server.py"],
      "description": "Slack integration",
      "env": {"SLACK_TOKEN": "${SLACK_TOKEN}"}
    }
  }
}
```

### 4. Done!
Set environment variable and restart system.

---

## That's It!

No core code changes needed. Just:
1. Copy template
2. Implement 2-3 methods
3. Restart

See `PLUGIN_ARCHITECTURE_GUIDE.md` for full details.
