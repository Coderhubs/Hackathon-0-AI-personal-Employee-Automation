# Gold Tier System - Environment Variables Setup

## Required Environment Variables

### Email MCP Server
```bash
GMAIL_API_KEY=your_gmail_api_key_here
```

### Social Media MCP Server
```bash
FACEBOOK_TOKEN=your_facebook_access_token
INSTAGRAM_TOKEN=your_instagram_access_token
TWITTER_API_KEY=your_twitter_api_key
```

### Odoo MCP Server
```bash
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database_name
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
```

---

## Windows Setup

### Option 1: System Environment Variables (Recommended)

1. Open System Properties (Win + Pause/Break)
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Add each variable name and value
6. Click OK to save

### Option 2: .env File

Create `.env` file in Gold_Tier directory:

```env
# Email Configuration
GMAIL_API_KEY=your_gmail_api_key_here

# Social Media Configuration
FACEBOOK_TOKEN=your_facebook_access_token
INSTAGRAM_TOKEN=your_instagram_access_token
TWITTER_API_KEY=your_twitter_api_key

# Odoo ERP Configuration
ODOO_URL=https://your-odoo-instance.com
ODOO_DB=your_database_name
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

### Option 3: Batch File

Create `set_env.bat`:

```batch
@echo off
REM Set Gold Tier environment variables

set GMAIL_API_KEY=your_gmail_api_key_here
set FACEBOOK_TOKEN=your_facebook_access_token
set INSTAGRAM_TOKEN=your_instagram_access_token
set TWITTER_API_KEY=your_twitter_api_key
set ODOO_URL=https://your-odoo-instance.com
set ODOO_DB=your_database_name
set ODOO_USERNAME=your_username
set ODOO_PASSWORD=your_password

echo Environment variables set for current session
```

Run before starting system:
```bash
set_env.bat
start_gold_tier.bat
```

---

## Security Notes

- **NEVER** commit `.env` file to version control
- Add `.env` to `.gitignore`
- Use secure credential storage for production
- Rotate API keys regularly
- Use read-only tokens where possible

---

## Verification

Test environment variables are set:

```bash
echo %GMAIL_API_KEY%
echo %FACEBOOK_TOKEN%
echo %ODOO_URL%
```

---

*Gold Tier Autonomous System - Environment Configuration*
