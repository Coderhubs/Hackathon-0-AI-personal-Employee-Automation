"""
Integration Coordinator - Complete Automation System
Manages LinkedIn, Gmail, and WhatsApp automation workflows
"""
import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

class IntegrationCoordinator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.approved = self.vault_path / "Approved"
        self.done = self.vault_path / "Done"
        self.plans = self.vault_path / "Plans"
        self.logs = self.vault_path / "Logs"

        # Ensure folders exist
        for folder in [self.needs_action, self.pending_approval, self.approved, self.done, self.plans, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_logging()
        self.load_config()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / f"integration_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('IntegrationCoordinator')

    def load_config(self):
        """Load configuration from .env"""
        load_dotenv()
        self.config = {
            'linkedin_email': os.getenv('LINKEDIN_EMAIL'),
            'gmail_email': os.getenv('GMAIL_EMAIL'),
            'business_name': os.getenv('BUSINESS_NAME', 'Your Business'),
            'ceo_name': os.getenv('CEO_NAME', 'CEO'),
            'auto_reply_enabled': os.getenv('AUTO_REPLY_ENABLED', 'false').lower() == 'true',
            'draft_replies_enabled': os.getenv('DRAFT_REPLIES_ENABLED', 'true').lower() == 'true',
        }

    def process_needs_action(self):
        """Process all files in Needs_Action folder"""
        files = list(self.needs_action.glob("*.md"))

        if not files:
            self.logger.debug("No files in Needs_Action")
            return

        self.logger.info(f"Processing {len(files)} files in Needs_Action")

        for file in files:
            try:
                self.process_single_file(file)
            except Exception as e:
                self.logger.error(f"Error processing {file.name}: {e}")

    def process_single_file(self, file: Path):
        """Process a single action file"""
        self.logger.info(f"Processing: {file.name}")

        # Read file content
        content = file.read_text(encoding='utf-8')

        # Determine file type from frontmatter
        file_type = self.extract_frontmatter_value(content, 'type')

        if file_type == 'email':
            self.process_email_action(file, content)
        elif file_type == 'linkedin':
            self.process_linkedin_action(file, content)
        elif file_type == 'whatsapp':
            self.process_whatsapp_action(file, content)
        else:
            self.process_generic_action(file, content)

    def extract_frontmatter_value(self, content: str, key: str) -> str:
        """Extract value from YAML frontmatter"""
        lines = content.split('\n')
        in_frontmatter = False

        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break
            elif in_frontmatter and ':' in line:
                k, v = line.split(':', 1)
                if k.strip() == key:
                    return v.strip()

        return ''

    def process_email_action(self, file: Path, content: str):
        """Process email action - draft reply"""
        self.logger.info("Processing email action")

        # Extract email details
        sender = self.extract_frontmatter_value(content, 'from')
        subject = self.extract_frontmatter_value(content, 'subject')
        priority = self.extract_frontmatter_value(content, 'priority')

        # Create plan
        plan_file = self.plans / f"PLAN_email_{file.stem}.md"
        plan_content = f"""# Email Response Plan

**Created:** {datetime.now().isoformat()}
**Original Email:** {file.name}
**From:** {sender}
**Subject:** {subject}
**Priority:** {priority}

## Analysis
This email requires a response. Based on Company Handbook rules:
- Check if sender is known contact
- Determine response type (sales, support, admin)
- Draft appropriate response
- Require approval before sending

## Actions Required
- [ ] Analyze email content
- [ ] Draft response following tone guidelines
- [ ] Create approval request
- [ ] Wait for human approval
- [ ] Send email via MCP
- [ ] Log to Dashboard

## Next Steps
Creating draft response and approval request...
"""
        plan_file.write_text(plan_content, encoding='utf-8')
        self.logger.info(f"Created plan: {plan_file.name}")

        # Create approval request
        self.create_email_approval_request(file, sender, subject, content)

    def create_email_approval_request(self, original_file: Path, sender: str, subject: str, content: str):
        """Create email approval request"""
        # Generate draft reply
        draft_reply = self.generate_email_draft(sender, subject, content)

        # Create approval file
        approval_file = self.pending_approval / f"EMAIL_REPLY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        approval_content = f"""---
type: email_reply
action: send_email
to: {sender}
subject: Re: {subject}
created: {datetime.now().isoformat()}
status: pending_approval
original_file: {original_file.name}
---

# Email Reply - PENDING APPROVAL

**To:** {sender}
**Subject:** Re: {subject}
**Created:** {datetime.now().isoformat()}

## Draft Reply

{draft_reply}

## Original Email

{content}

## Actions
- [ ] Approve and send
- [ ] Edit and approve
- [ ] Reject

## Instructions
To approve: Move this file to /Approved folder
To reject: Move this file to /Rejected folder (create if needed)

---
*This email requires human approval before sending*
"""

        approval_file.write_text(approval_content, encoding='utf-8')
        self.logger.info(f"Created approval request: {approval_file.name}")

        # Move original to Done
        done_file = self.done / original_file.name
        original_file.rename(done_file)
        self.logger.info(f"Moved original to Done: {done_file.name}")

    def generate_email_draft(self, sender: str, subject: str, content: str) -> str:
        """Generate draft email reply based on content"""
        # Simple draft generation - in production, use Claude API

        # Check for keywords
        content_lower = content.lower()

        if any(kw in content_lower for kw in ['pricing', 'quote', 'cost', 'price']):
            return f"""Hi {sender.split()[0] if sender else 'there'},

Thank you for your interest in our services!

I'd be happy to discuss pricing with you. Our solutions are tailored to each client's specific needs.

Could we schedule a brief call to understand your requirements better? Here are some times that work for me:
- [Time slot 1]
- [Time slot 2]
- [Time slot 3]

Looking forward to connecting!

Best regards,
{self.config['ceo_name']}
{self.config['business_name']}

---
This email was drafted by AI and reviewed by {self.config['ceo_name']}
"""

        elif any(kw in content_lower for kw in ['meeting', 'call', 'schedule', 'available']):
            return f"""Hi {sender.split()[0] if sender else 'there'},

Thanks for reaching out!

I'd be happy to schedule a meeting. Here are some times that work for me:
- [Time slot 1]
- [Time slot 2]
- [Time slot 3]

Please let me know which works best for you, or suggest an alternative time.

Best regards,
{self.config['ceo_name']}
{self.config['business_name']}

---
This email was drafted by AI and reviewed by {self.config['ceo_name']}
"""

        else:
            return f"""Hi {sender.split()[0] if sender else 'there'},

Thank you for your email.

I've received your message and will get back to you shortly with a detailed response.

Best regards,
{self.config['ceo_name']}
{self.config['business_name']}

---
This email was drafted by AI and reviewed by {self.config['ceo_name']}
"""

    def process_linkedin_action(self, file: Path, content: str):
        """Process LinkedIn action - generate post"""
        self.logger.info("Processing LinkedIn action")

        # Generate LinkedIn post content
        post_content = self.generate_linkedin_post(content)

        # Create approval request
        approval_file = self.pending_approval / f"LINKEDIN_POST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        approval_content = f"""---
type: linkedin_post
action: post_linkedin
created: {datetime.now().isoformat()}
status: pending_approval
---

# LinkedIn Post - PENDING APPROVAL

**Created:** {datetime.now().isoformat()}
**Platform:** LinkedIn
**Account:** {self.config['linkedin_email']}

## Post Content

{post_content}

## Actions
- [ ] Approve and post
- [ ] Edit and approve
- [ ] Reject

## Instructions
To approve: Move this file to /Approved folder
To reject: Delete this file

---
*This post requires human approval before publishing*
"""

        approval_file.write_text(approval_content, encoding='utf-8')
        self.logger.info(f"Created LinkedIn approval request: {approval_file.name}")

        # Move original to Done
        done_file = self.done / file.name
        file.rename(done_file)

    def generate_linkedin_post(self, trigger_content: str) -> str:
        """Generate LinkedIn post content"""
        # Simple post generation - in production, use Claude API

        posts = [
            """🚀 Exciting times in AI automation!

Just implemented a new workflow that saves our team 10+ hours per week on routine tasks.

The key? Smart automation with human oversight. AI handles the repetitive work, humans make the strategic decisions.

What's your biggest time sink that could be automated?

#AI #Automation #Productivity #BusinessEfficiency""",

            """💡 Lesson learned this week:

The best automation isn't about doing everything automatically.

It's about:
✅ Automating the routine
✅ Flagging the important
✅ Empowering humans to focus on high-value work

What's your automation philosophy?

#AIAutomation #BusinessStrategy #Productivity""",

            """🎯 Quick tip for business owners:

Before automating a process, ask:
1. Is this task repetitive?
2. Does it follow clear rules?
3. What's the cost of getting it wrong?

If answers are Yes, Yes, Low → automate it!
If the cost of error is high → keep human in the loop.

What processes have you successfully automated?

#BusinessAutomation #AI #SmartBusiness"""
        ]

        # Return a random post (in production, generate based on context)
        import random
        return random.choice(posts)

    def process_whatsapp_action(self, file: Path, content: str):
        """Process WhatsApp action - draft reply"""
        self.logger.info("Processing WhatsApp action")

        # Similar to email processing
        sender = self.extract_frontmatter_value(content, 'from')

        # Create approval request for reply
        approval_file = self.pending_approval / f"WHATSAPP_REPLY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        draft_reply = f"Thanks for reaching out! I'll get back to you shortly."

        approval_content = f"""---
type: whatsapp_reply
action: send_whatsapp
to: {sender}
created: {datetime.now().isoformat()}
status: pending_approval
---

# WhatsApp Reply - PENDING APPROVAL

**To:** {sender}
**Created:** {datetime.now().isoformat()}

## Draft Reply

{draft_reply}

## Original Message

{content}

## Actions
- [ ] Approve and send
- [ ] Edit and approve
- [ ] Reject

---
*This message requires human approval before sending*
"""

        approval_file.write_text(approval_content, encoding='utf-8')
        self.logger.info(f"Created WhatsApp approval request: {approval_file.name}")

        # Move original to Done
        done_file = self.done / file.name
        file.rename(done_file)

    def process_generic_action(self, file: Path, content: str):
        """Process generic action file"""
        self.logger.info(f"Processing generic action: {file.name}")

        # Just log and move to Done
        done_file = self.done / file.name
        file.rename(done_file)
        self.logger.info(f"Moved to Done: {done_file.name}")

    def run_once(self):
        """Run one processing cycle"""
        self.logger.info("=" * 70)
        self.logger.info("Integration Coordinator - Processing Cycle")
        self.logger.info("=" * 70)

        # Process Needs_Action folder
        self.process_needs_action()

        self.logger.info("Processing cycle complete")
        self.logger.info("")

    def run_continuous(self, interval: int = 60):
        """Run continuously with specified interval"""
        self.logger.info("=" * 70)
        self.logger.info("Integration Coordinator - Continuous Mode")
        self.logger.info("=" * 70)
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Check interval: {interval} seconds")
        self.logger.info("Press Ctrl+C to stop")
        self.logger.info("=" * 70)
        self.logger.info("")

        try:
            while True:
                self.run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("Stopped by user")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent / "AI_Employee_Vault"

    if not vault_path.exists():
        print(f"ERROR: Vault not found at {vault_path}")
        return

    coordinator = IntegrationCoordinator(str(vault_path))

    # Run continuously (check every 60 seconds)
    coordinator.run_continuous(interval=60)

if __name__ == "__main__":
    main()
