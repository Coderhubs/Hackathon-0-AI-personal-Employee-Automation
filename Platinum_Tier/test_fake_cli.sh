#!/bin/bash
# Quick CLI Test Script for Gmail/LinkedIn Watchers
# Creates fake emails and posts instantly for testing

echo "=== FAKE GMAIL/LINKEDIN CLI TESTER ==="
echo ""
echo "This script creates fake emails and LinkedIn posts instantly"
echo "to test your AI Employee system without waiting."
echo ""

# Function to create fake Gmail
create_fake_gmail() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SUBJECT=$1
    FILENAME="Inbox/GMAIL_${TIMESTAMP}_${SUBJECT}.txt"

    cat > "$FILENAME" << EOF
Subject: $SUBJECT
From: sender@example.com
To: recipient@company.com
Date: $(date '+%Y-%m-%d %H:%M:%S')
----------------------------------------
This is a fake email created for testing.

You can customize this content to test different scenarios:
- High priority emails
- Invoices
- Meeting requests
- Security alerts
- etc.
EOF

    echo "✓ Created: $FILENAME"
}

# Function to create fake LinkedIn post
create_fake_linkedin() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    CONTENT=$1
    FILENAME="Inbox/LINKEDIN_trend_${TIMESTAMP}.txt"

    echo "$CONTENT" > "$FILENAME"

    echo "✓ Created: $FILENAME"
}

# Main menu
while true; do
    echo ""
    echo "Choose an option:"
    echo "1. Create fake Gmail email"
    echo "2. Create fake LinkedIn post"
    echo "3. Create both (Gmail + LinkedIn)"
    echo "4. Create 5 fake emails"
    echo "5. Create 5 fake posts"
    echo "6. Exit"
    echo ""
    read -p "Enter choice (1-6): " choice

    case $choice in
        1)
            read -p "Enter email subject (or press Enter for default): " subject
            subject=${subject:-"Test_Email"}
            subject=$(echo $subject | tr ' ' '_')
            create_fake_gmail "$subject"
            ;;
        2)
            read -p "Enter LinkedIn post content (or press Enter for default): " content
            content=${content:-"This is a test LinkedIn post"}
            create_fake_linkedin "$content"
            ;;
        3)
            create_fake_gmail "Quick_Test"
            create_fake_linkedin "Quick test post"
            ;;
        4)
            echo "Creating 5 fake emails..."
            for i in {1..5}; do
                create_fake_gmail "Test_Email_$i"
                sleep 0.5
            done
            ;;
        5)
            echo "Creating 5 fake posts..."
            for i in {1..5}; do
                create_fake_linkedin "Test post number $i"
                sleep 0.5
            done
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1-6."
            ;;
    esac

    echo ""
    echo "Files will be processed by filesystem watcher automatically!"
    echo "Check Dashboard.md to see them being processed."
done
