"""
Gmail App Password Setup Guide
"""

# STEP 1: Generate an App Password
# ================================
# 1. Go to: https://myaccount.google.com/apppasswords
# 2. Sign in to your Google account
# 3. Select "Mail" as the app
# 4. Select "Windows Computer" as the device
# 5. Click "Generate"
# 6. Copy the 16-character password (looks like: xxxx xxxx xxxx xxxx)

# STEP 2: Update your .env file
# ================================
# Replace your current Gmail password with the App Password:
#
# GMAIL_EMAIL=fateehaaayat@gmail.com
# GMAIL_PASSWORD=xxxx xxxx xxxx xxxx  (the 16-char App Password)

# STEP 3: Test again
# ================================
# Run: python demo_gmail.py

# NOTE: If you don't have 2FA enabled:
# - You need to enable it first to generate App Passwords
# - Or enable "Less secure app access" (not recommended)
# - Go to: https://myaccount.google.com/security

print("Follow the steps above to set up Gmail App Password")
