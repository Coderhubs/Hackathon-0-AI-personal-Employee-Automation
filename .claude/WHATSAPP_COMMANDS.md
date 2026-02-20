# WhatsApp Automation Commands - Send & Receive

## 💬 SENDING MESSAGES

### Test WhatsApp Sending
```cmd
python test_whatsapp_send.py
```

This will:
- Connect to Twilio API
- Send test message to configured number
- Show message SID if successful
- Log to WhatsApp_Vault/Sent/

### Alternative Send Commands

**Direct WhatsApp Send:**
```cmd
python whatsapp_send.py
```

**Send Custom Message:**
```cmd
python -c "from whatsapp_send import WhatsAppSender; import os; from dotenv import load_dotenv; load_dotenv(); sender = WhatsAppSender(); sender.send_message(os.getenv('TEST_PHONE_NUMBER'), 'Your custom message here')"
```

---

## 📥 RECEIVING MESSAGES (Monitoring WhatsApp)

### Start WhatsApp Watcher
```cmd
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

**Features:**
- ✅ Monitors WhatsApp for incoming messages
- ✅ Detects messages with keywords
- ✅ Saves to AI_Employee_Vault/Needs_Action/
- ✅ Auto-reply capability
- ✅ Runs continuously

### Alternative: WhatsApp Auto-Reply
```cmd
python whatsapp_autoreply.py
```

**Features:**
- Automatically replies to incoming messages
- Uses AI to generate contextual responses
- Logs all conversations

### Stop WhatsApp Watcher
Press `Ctrl+C` in the command window

---

## 📊 Check Status

### View Sent Messages
```cmd
dir WhatsApp_Vault\Sent\SENT_*.txt
```

### View Latest Sent Message
```cmd
type WhatsApp_Vault\Sent\SENT_*.txt
```

### View Received Messages
```cmd
dir AI_Employee_Vault\Needs_Action\WHATSAPP_*.md
```

### View Conversations
```cmd
dir WhatsApp_Vault\Conversations\
```

---

## Setup Commands (First Time Only)

### Setup WhatsApp/Twilio Credentials
```cmd
python -c "print('Add these to .env file:'); print('TWILIO_ACCOUNT_SID=your-account-sid'); print('TWILIO_AUTH_TOKEN=your-auth-token'); print('TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886'); print('TEST_PHONE_NUMBER=whatsapp:+your-number')"
```

---

## Check WhatsApp Status

### Verify Credentials
```cmd
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Twilio SID:', os.getenv('TWILIO_ACCOUNT_SID')[:10] + '...' if os.getenv('TWILIO_ACCOUNT_SID') else 'Not Set'); print('Auth Token:', 'Set' if os.getenv('TWILIO_AUTH_TOKEN') else 'Not Set'); print('WhatsApp Number:', os.getenv('TWILIO_WHATSAPP_NUMBER')); print('Test Number:', os.getenv('TEST_PHONE_NUMBER'))"
```

### View Sent Messages
```cmd
dir WhatsApp_Vault\Sent\SENT_*.txt
```

### View Latest Sent Message
```cmd
dir /b /o-d WhatsApp_Vault\Sent\SENT_*.txt | findstr /n "^" | findstr "^1:" > temp.txt && set /p latest=<temp.txt && for /f "tokens=2 delims=:" %%a in ("%latest%") do type "WhatsApp_Vault\Sent\%%a"
```

Or simply:
```cmd
type WhatsApp_Vault\Sent\SENT_*.txt
```

---

## Troubleshooting

### If Network Error (DNS Resolution Failed)

**Check internet connection:**
```cmd
ping api.twilio.com
```

**If ping fails:**
1. Check your internet connection
2. Try again later
3. Check firewall settings

### If Authentication Fails

**Verify Twilio credentials:**
```cmd
type .env | findstr TWILIO
```

Should show:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**Get credentials from:**
- Login to Twilio Console: https://console.twilio.com
- Copy Account SID and Auth Token
- Add to .env file

### If Message Not Received

1. Verify phone number format: `whatsapp:+1234567890`
2. Check if number is registered with Twilio sandbox
3. View Twilio logs in console
4. Check WhatsApp_Vault/Sent/ for confirmation

---

## WhatsApp Watcher Commands

### Start WhatsApp Watcher (Monitor Messages)
```cmd
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

This will:
- Monitor WhatsApp for incoming messages
- Detect messages with keywords
- Save to Needs_Action folder
- Run continuously until stopped

### Stop WhatsApp Watcher
Press `Ctrl+C` in the command window

---

## Example Workflow

```cmd
REM Step 1: Test WhatsApp connection
python test_whatsapp_send.py

REM Step 2: Check if message was sent
dir WhatsApp_Vault\Sent\

REM Step 3: View sent message details
type WhatsApp_Vault\Sent\SENT_*.txt

REM Step 4: Start WhatsApp watcher (optional)
python Platinum_Tier\whatsapp_watcher_hackathon.py
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python test_whatsapp_send.py` | Test WhatsApp sending |
| `python whatsapp_send.py` | Direct WhatsApp send |
| `python Platinum_Tier\whatsapp_watcher_hackathon.py` | Start WhatsApp monitoring |
| `dir WhatsApp_Vault\Sent\` | View sent messages |

---

## Required .env Variables

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-auth-token-here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TEST_PHONE_NUMBER=whatsapp:+1234567890
```

**Note:** Phone numbers must include `whatsapp:` prefix and country code.

---

## Twilio Sandbox Setup

### First Time Setup
1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Send "join <your-sandbox-name>" to +1 415 523 8886 from your WhatsApp
3. Wait for confirmation message
4. Now you can send/receive messages

### Test Sandbox Connection
```cmd
python -c "from whatsapp_send import WhatsAppSender; sender = WhatsAppSender(); print('Sandbox ready!' if sender else 'Setup needed')"
```

---

## Current Known Issues

### Network DNS Error
- **Issue:** Cannot resolve api.twilio.com
- **Status:** Temporary network issue
- **Solution:** Wait for network to stabilize, then retry

---

**Last Updated:** 2026-02-20
