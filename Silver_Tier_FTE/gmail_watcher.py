import os
import time
import random
from datetime import datetime

def get_random_email_subject():
    """Generate a random email subject related to business/tech."""
    subjects = [
        "Project Update: Quarterly Goals",
        "Meeting Request: Team Sync",
        "Invoice: Monthly Subscription",
        "Collaboration Opportunity",
        "Tech Conference Invitation",
        "New Feature Release",
        "Security Alert: Account Activity",
        "Performance Report",
        "Client Feedback Summary",
        "Partnership Proposal",
        "Bug Report: Critical Issue",
        "Training Session Reminder",
        "Budget Approval Request",
        "Vendor Communication",
        "Newsletter: Industry Insights"
    ]
    return random.choice(subjects)

def get_random_email_body(subject):
    """Generate a random email body based on the subject."""
    bodies = {
        "Project Update: Quarterly Goals": "Hi team, I wanted to share our progress on the quarterly goals. We're on track to meet our targets.",
        "Meeting Request: Team Sync": "Can we schedule a team sync for tomorrow? We need to discuss the upcoming deadlines.",
        "Invoice: Monthly Subscription": "Attached is your monthly invoice for our services. Please review and process payment.",
        "Collaboration Opportunity": "I'd like to explore a collaboration opportunity with your team. Are you available for a call?",
        "Tech Conference Invitation": "You're invited to attend our annual tech conference next month. Register here.",
        "New Feature Release": "We're excited to announce our latest feature release. Check out the documentation.",
        "Security Alert: Account Activity": "Unusual activity detected on your account. Please verify this login attempt.",
        "Performance Report": "Monthly performance report attached. Key metrics show improvement in efficiency.",
        "Client Feedback Summary": "Summary of client feedback from last quarter. Several positive reviews received.",
        "Partnership Proposal": "We'd like to propose a partnership that could benefit both organizations.",
        "Bug Report: Critical Issue": "Critical bug detected in production. Immediate attention required.",
        "Training Session Reminder": "Reminder about the training session scheduled for Friday. Please confirm attendance.",
        "Budget Approval Request": "Requesting approval for the Q2 marketing budget. Details attached.",
        "Vendor Communication": "Communication from our vendor regarding supply chain updates.",
        "Newsletter: Industry Insights": "Monthly newsletter with industry insights and trends."
    }
    return bodies.get(subject, f"This email is regarding: {subject}. Please review the attached documents.")

def create_gmail_file():
    """Create a file in Inbox simulating a received email."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subject = get_random_email_subject()
    filename = f"GMAIL_{timestamp}_{subject.replace(' ', '_').replace(':', '').replace('/', '_')}.txt"
    filepath = os.path.join("Inbox", filename)
    
    email_body = get_random_email_body(subject)
    
    with open(filepath, 'w') as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"From: sender@example.com\n")
        f.write(f"To: recipient@silver-tier-fte.com\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 40 + "\n")
        f.write(email_body)
    
    print(f"Created Gmail file: {filepath}")

def main():
    """Main function to run the Gmail watcher."""
    print("Starting Gmail Watcher...")
    print("Creating a new email file every 3 minutes.")
    
    while True:
        try:
            create_gmail_file()
            time.sleep(180)  # Wait for 3 minutes (180 seconds)
        except KeyboardInterrupt:
            print("\nGmail Watcher stopped.")
            break
        except Exception as e:
            print(f"Error in Gmail Watcher: {e}")
            time.sleep(180)  # Wait before retrying

if __name__ == "__main__":
    main()