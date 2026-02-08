#!/bin/bash
# SIMPLE CLI COMMANDS TO CREATE FAKE EMAILS/POSTS
# Copy and paste these commands to test your system instantly!

# ============================================
# QUICK TEST COMMANDS
# ============================================

# Navigate to Platinum_Tier directory first:
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"

# ============================================
# CREATE FAKE GMAIL EMAIL
# ============================================

# Basic fake email:
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Test_Email.txt << 'EOF'
Subject: Test Email
From: sender@example.com
To: you@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
This is a test email created from CLI.
EOF

# High priority email:
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_URGENT_Action_Required.txt << 'EOF'
Subject: URGENT: Action Required
From: boss@company.com
To: you@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
URGENT: Please review and respond immediately.
This requires your immediate attention.
EOF

# Invoice email:
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Invoice_Payment_Due.txt << 'EOF'
Subject: Invoice #12345 - Payment Due
From: billing@vendor.com
To: accounts@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
Invoice #12345
Amount: $1,500.00
Due Date: 2026-02-15
Please process payment.
EOF

# Meeting request:
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Meeting_Request.txt << 'EOF'
Subject: Meeting Request: Project Review
From: colleague@company.com
To: you@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
Can we schedule a meeting to review the project?
Available times:
- Tomorrow 2pm
- Friday 10am
EOF

# ============================================
# CREATE FAKE LINKEDIN POST
# ============================================

# Basic post:
echo "AI is transforming the workplace" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# Tech trend:
echo "Breaking: New AI model achieves 95% accuracy" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# Industry news:
echo "Remote work adoption reaches all-time high" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# Job posting:
echo "Hiring: Senior Software Engineer - Apply Now!" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# ============================================
# CREATE MULTIPLE FILES AT ONCE
# ============================================

# Create 5 fake emails:
for i in {1..5}; do
  cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Batch_Test_$i.txt << EOF
Subject: Batch Test Email $i
From: sender$i@example.com
To: you@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
This is batch test email number $i.
EOF
  sleep 1
done

# Create 5 fake LinkedIn posts:
for i in {1..5}; do
  echo "LinkedIn post number $i - Testing system" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt
  sleep 1
done

# ============================================
# WINDOWS POWERSHELL VERSIONS
# ============================================

# If bash doesn't work, use PowerShell:

# Create fake Gmail (PowerShell):
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$content = @"
Subject: Test Email
From: sender@example.com
To: you@company.com
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
----------------------------------------
This is a test email from PowerShell.
"@
$content | Out-File -FilePath "Inbox\GMAIL_${timestamp}_Test.txt" -Encoding UTF8

# Create fake LinkedIn (PowerShell):
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
"Test LinkedIn post from PowerShell" | Out-File -FilePath "Inbox\LINKEDIN_trend_${timestamp}.txt" -Encoding UTF8

# ============================================
# PYTHON VERSION (Most Reliable)
# ============================================

# Create test_creator.py:
cat > test_creator.py << 'PYTHON_EOF'
import os
from datetime import datetime

def create_fake_gmail(subject, body="This is a test email."):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Inbox/GMAIL_{timestamp}_{subject.replace(' ', '_')}.txt"

    content = f"""Subject: {subject}
From: sender@example.com
To: you@company.com
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
----------------------------------------
{body}
"""

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ Created: {filename}")

def create_fake_linkedin(content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Inbox/LINKEDIN_trend_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(content)

    print(f"✓ Created: {filename}")

# Usage examples:
if __name__ == "__main__":
    # Create fake email
    create_fake_gmail("Test Email", "This is a test from Python!")

    # Create fake LinkedIn post
    create_fake_linkedin("AI trends in 2026")

    print("\nFiles created! Check Inbox folder.")
PYTHON_EOF

# Run it:
python test_creator.py

# ============================================
# SIMPLE ONE-LINERS
# ============================================

# Quick Gmail test:
echo -e "Subject: Quick Test\nFrom: test@test.com\nTo: you@company.com\n\nQuick test email" > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Quick.txt

# Quick LinkedIn test:
echo "Quick LinkedIn test post" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# ============================================
# MONITORING COMMANDS
# ============================================

# Watch files being created:
watch -n 2 'ls -lt Inbox | head -10'

# Watch files being processed:
watch -n 2 'echo "Inbox: $(ls Inbox | wc -l) | Needs_Action: $(ls Needs_Action | wc -l) | Done: $(ls Done | wc -l)"'

# Watch Dashboard updates:
tail -f Dashboard.md

# Check latest processed files:
ls -lt Done | head -10

# ============================================
# CLEANUP COMMANDS
# ============================================

# Remove all test files:
rm Inbox/TEST_* 2>/dev/null
rm Inbox/GMAIL_* 2>/dev/null
rm Inbox/LINKEDIN_* 2>/dev/null

# Clean up Done folder:
rm Done/* 2>/dev/null

# ============================================
# USAGE EXAMPLES
# ============================================

# Example 1: Test urgent email processing
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_URGENT_Test.txt << 'EOF'
Subject: URGENT: System Test
From: admin@company.com
To: you@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
Testing urgent email processing.
This should be flagged as high priority.
EOF

# Example 2: Test invoice processing
cat > Inbox/GMAIL_$(date +%Y%m%d_%H%M%S)_Invoice_Test.txt << 'EOF'
Subject: Invoice #TEST123
From: billing@vendor.com
To: accounts@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
Invoice: TEST123
Amount: $999.99
Testing invoice detection and processing.
EOF

# Example 3: Test LinkedIn trend
echo "Breaking: AI achieves human-level performance in coding tasks" > Inbox/LINKEDIN_trend_$(date +%Y%m%d_%H%M%S).txt

# ============================================
# VERIFICATION
# ============================================

# After creating files, verify they're being processed:
echo "Waiting 5 seconds for processing..."
sleep 5

echo "Files in Inbox: $(ls Inbox | wc -l)"
echo "Files in Needs_Action: $(ls Needs_Action | wc -l)"
echo "Files in Done: $(ls Done | wc -l)"

echo ""
echo "Check Dashboard.md for processing log:"
tail -20 Dashboard.md

# ============================================
# NOTES
# ============================================

# - Files are processed within 1 second of creation
# - Filesystem watcher detects them automatically
# - Check Dashboard.md for complete audit trail
# - All files are logged and archived in Done/
# - You can create unlimited test files
# - System handles concurrent file creation
# - No need to restart anything - it's all automatic!

# ============================================
# TROUBLESHOOTING
# ============================================

# If files aren't being processed:
# 1. Check filesystem watcher is running:
ps aux | grep filesystem_watcher

# 2. Check logs:
tail -f Gold_Tier/Logs/filesystem_watcher.log

# 3. Verify directories exist:
ls -la | grep -E "Inbox|Needs_Action|Done"

# 4. Restart filesystem watcher:
python filesystem_watcher.py &
