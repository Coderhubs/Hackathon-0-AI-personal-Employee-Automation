# Agentic AI Watchers - Complete Guide

## Overview

Gmail and LinkedIn watchers that monitor for Agentic AI content and can also send emails/create posts about Agentic AI technology.

## Features

### 📧 Gmail Watcher
- **Monitor**: Watches inbox for emails about Agentic AI
- **Send**: Can send emails about Agentic AI updates
- **Filter**: Keywords: agentic, ai agent, autonomous ai, llm, claude, gpt, artificial intelligence, machine learning
- **Save**: Stores filtered emails in `Inbox/` folder with `GMAIL_AGENTIC_` prefix

### 📱 LinkedIn Watcher
- **Monitor**: Watches feed for posts about Agentic AI
- **Post**: Can create posts about Agentic AI technology
- **Filter**: Same keywords as Gmail watcher
- **Save**: Stores filtered posts in `Inbox/` folder with `LINKEDIN_AGENTIC_` prefix

## Quick Start

### 1. Setup Credentials
```bash
python Platinum_Tier/setup_credentials.py
```

**Important for Gmail:**
- If you have 2FA enabled, use an App Password
- Generate at: https://myaccount.google.com/apppasswords

### 2. Test the Watchers
```bash
# Test Gmail
python Platinum_Tier/demo_gmail.py

# Test LinkedIn
python Platinum_Tier/demo_linkedin.py
```

### 3. Run the Watchers

**Option A: Both watchers together**
```bash
Platinum_Tier\RUN_WATCHERS.bat
```

**Option B: Individual watchers**
```bash
# Gmail only
python Platinum_Tier/gmail_watcher_playwright.py

# LinkedIn only
python Platinum_Tier/linkedin_watcher_playwright.py
```

## Configuration

### Enable Email Sending (Gmail)
Edit `gmail_watcher_playwright.py` line 197:
```python
asyncio.run(watcher.run(send_demo_email=True))  # Change False to True
```

### Enable Post Creation (LinkedIn)
Edit `linkedin_watcher_playwright.py` line 218:
```python
asyncio.run(watcher.run(create_demo_post=True))  # Change False to True
```

### Change Check Intervals
Edit the `check_interval` parameter:
```python
# Gmail (line 195)
check_interval=180  # seconds (3 minutes)

# LinkedIn (line 215)
check_interval=120  # seconds (2 minutes)
```

### Customize Keywords
Edit the `agentic_keywords` list in `__init__`:
```python
self.agentic_keywords = [
    'agentic',
    'ai agent',
    'autonomous ai',
    'llm',
    'claude',
    'gpt',
    'artificial intelligence',
    'machine learning'
]
```

## How It Works

### Monitoring Mode (Default)
1. Logs into Gmail/LinkedIn using Playwright
2. Checks inbox/feed at regular intervals
3. Filters content for Agentic AI keywords
4. Saves matching content to `Inbox/` folder
5. Tracks seen items to avoid duplicates

### Sending/Posting Mode
1. Logs into Gmail/LinkedIn
2. Sends demo email or creates demo post about Agentic AI
3. Then continues monitoring as normal

## Demo Content

### Gmail Demo Email
```
Subject: Agentic AI Technology Update - [Date]

Key Developments in Agentic AI:
• Autonomous agents with improved reasoning
• Multi-agent systems solving real-world problems
• LLMs with tool use enabling new applications
• Claude, GPT-4 powering intelligent agents

Today's Focus Areas:
- Tool-using AI agents for automation
- Collaborative multi-agent workflows
- Real-time decision making systems
- Agentic AI in enterprise applications
```

### LinkedIn Demo Post
```
🤖 Agentic AI Technology Update - [Date]

The landscape of Agentic AI is evolving rapidly:

✨ Autonomous agents transforming AI interaction
🔧 Tool-using LLMs enabling practical applications
🚀 Multi-agent systems solving complex problems
💡 Claude, GPT-4 powering intelligent workflows

The future of AI is about taking action autonomously.

#AgenticAI #AI #MachineLearning #Automation #LLM
```

## File Structure

```
Platinum_Tier/
├── gmail_watcher_playwright.py      # Gmail watcher with send capability
├── linkedin_watcher_playwright.py   # LinkedIn watcher with post capability
├── demo_gmail.py                    # Gmail test script
├── demo_linkedin.py                 # LinkedIn test script
├── setup_credentials.py             # Credential setup
├── RUN_WATCHERS.bat                 # Run both watchers
└── AGENTIC_AI_WATCHERS_GUIDE.md    # This file

Inbox/
├── GMAIL_AGENTIC_[timestamp]_[subject].txt
└── LINKEDIN_AGENTIC_[timestamp]_[author].txt

Gold_Tier/Logs/
├── gmail_watcher_playwright.log
└── linkedin_watcher_playwright.log
```

## Troubleshooting

### Gmail Issues

**Problem**: Login fails with 2FA
**Solution**: Use an App Password instead of your regular password

**Problem**: "Could not find compose button"
**Solution**: Gmail UI may have changed. Check browser window for manual compose.

**Problem**: Email not sending
**Solution**: Verify selectors are correct. Gmail may have updated their UI.

### LinkedIn Issues

**Problem**: Verification code required
**Solution**: The watcher waits 60 seconds for manual verification. Enter code in browser.

**Problem**: "Could not find Start a post button"
**Solution**: LinkedIn UI may have changed. Try creating a post manually first.

**Problem**: Post not creating
**Solution**: LinkedIn may have rate limits. Wait a few minutes and try again.

### General Issues

**Problem**: No Agentic AI content found
**Solution**: Keywords may be too specific. Add more keywords or broaden search.

**Problem**: Browser crashes
**Solution**: The watcher auto-restarts after 5 retries. Check logs for details.

**Problem**: Duplicate content saved
**Solution**: Delete log files to reset seen items tracking.

## Security Best Practices

1. **Never commit `.env` file** - Contains your credentials
2. **Use App Passwords for Gmail** - Not your main password
3. **Keep credentials secure** - Don't share or expose them
4. **Monitor activity** - Check logs regularly for issues
5. **Use responsibly** - Respect platform rate limits and ToS

## Advanced Usage

### Run in Background (Windows)
```bash
start /B python Platinum_Tier/gmail_watcher_playwright.py
start /B python Platinum_Tier/linkedin_watcher_playwright.py
```

### Schedule with Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\gmail_watcher_playwright.py`

### Custom Email/Post Content
Edit the `demo_subject`, `demo_body`, or `demo_content` variables in the respective scripts to customize what gets sent/posted.

## Logs

Check logs for detailed information:
```bash
# View Gmail logs
type Gold_Tier\Logs\gmail_watcher_playwright.log

# View LinkedIn logs
type Gold_Tier\Logs\linkedin_watcher_playwright.log
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify credentials are correct in `.env`
4. Test with demo scripts first

## Updates

To update keywords or intervals without editing code, you can modify the class initialization parameters when creating the watcher instances.
