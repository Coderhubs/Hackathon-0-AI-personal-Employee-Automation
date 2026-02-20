"""
LinkedIn Content Generator - Real Integration
Generates and posts LinkedIn content based on business activities
"""
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
import json

class LinkedInContentGenerator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.done_folder = self.vault_path / "Done"
        self.dashboard = self.vault_path / "Dashboard.md"
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.logs = self.vault_path / "Logs"

        self.pending_approval.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_logging()
        load_dotenv()

        self.business_name = os.getenv('BUSINESS_NAME', 'Your Business')
        self.ceo_name = os.getenv('CEO_NAME', 'CEO')

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / f"linkedin_generator_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedInGenerator')

    def analyze_recent_activity(self) -> dict:
        """Analyze recent business activity from Done folder and Dashboard"""
        activity = {
            'completed_tasks': [],
            'emails_processed': 0,
            'leads_captured': 0,
            'insights': []
        }

        # Check Done folder for recent completions
        if self.done_folder.exists():
            recent_files = sorted(
                self.done_folder.glob("*.md"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:10]

            for file in recent_files:
                try:
                    content = file.read_text(encoding='utf-8')
                    if 'EMAIL_' in file.name:
                        activity['emails_processed'] += 1
                    if 'LEAD_' in file.name or 'pricing' in content.lower():
                        activity['leads_captured'] += 1

                    activity['completed_tasks'].append({
                        'name': file.stem,
                        'date': datetime.fromtimestamp(file.stat().st_mtime)
                    })
                except Exception as e:
                    self.logger.warning(f"Error reading {file.name}: {e}")

        return activity

    def generate_post_content(self, post_type: str = 'business_update') -> str:
        """Generate LinkedIn post content based on type"""

        activity = self.analyze_recent_activity()

        if post_type == 'business_update':
            return self._generate_business_update(activity)
        elif post_type == 'industry_insight':
            return self._generate_industry_insight()
        elif post_type == 'engagement':
            return self._generate_engagement_post()
        elif post_type == 'automation_showcase':
            return self._generate_automation_showcase(activity)
        else:
            return self._generate_business_update(activity)

    def _generate_business_update(self, activity: dict) -> str:
        """Generate business update post"""

        posts = [
            f"""🚀 Week in Review at {self.business_name}

This week, our AI automation system:
✅ Processed {activity['emails_processed']} client inquiries
✅ Captured {activity['leads_captured']} new leads
✅ Saved 10+ hours on routine tasks

The key? Smart automation with human oversight.

AI handles the repetitive work → Humans focus on strategy and relationships.

What's your biggest productivity win this week?

#BusinessAutomation #AI #Productivity #SmallBusiness""",

            f"""💡 Automation Update

Just hit a new milestone: Our AI employee now handles 80% of routine email triage automatically.

The result?
→ Response time: 2 hours → 15 minutes
→ Lead capture: 100% (zero missed inquiries)
→ Time saved: 10+ hours/week

Still keeping human oversight for all client-facing communications.

What processes are you automating in your business?

#AIAutomation #BusinessEfficiency #SmallBusinessTech""",

            f"""🎯 This Week's Achievement

Implemented a new workflow that automatically:
• Monitors Gmail, LinkedIn, WhatsApp
• Categorizes urgent vs routine
• Drafts responses for approval
• Logs everything for audit

Time saved: 2 hours/day
Quality maintained: 100%

The future of work isn't about replacing humans—it's about empowering them.

What's your automation strategy?

#FutureOfWork #AI #BusinessGrowth"""
        ]

        import random
        return random.choice(posts)

    def _generate_industry_insight(self) -> str:
        """Generate industry insight post"""

        insights = [
            """🤔 Hot Take: AI Automation in 2026

The businesses winning aren't using AI to replace people.

They're using AI to:
→ Eliminate busywork
→ Speed up response times
→ Capture every opportunity
→ Free humans for high-value work

The question isn't "Can AI do this?"
It's "Should humans be doing this?"

What tasks have you automated this year?

#AI #BusinessStrategy #Automation #Leadership""",

            """💭 Lesson Learned: The 80/20 of Automation

After 6 months of AI automation:

80% of value comes from automating:
✅ Email triage
✅ Lead capture
✅ Data logging
✅ Routine responses

20% of value comes from:
⚠️ Complex decision-making
⚠️ Relationship building
⚠️ Creative strategy

Focus on automating the 80%. Keep humans in the 20%.

What's your automation priority?

#BusinessAutomation #Productivity #SmartBusiness""",

            """🚨 Unpopular Opinion:

"Fully autonomous AI" is the wrong goal.

The right goal? "Perfectly augmented humans."

AI should:
→ Handle the routine
→ Flag the important
→ Draft the responses
→ Wait for approval

Humans should:
→ Make final decisions
→ Build relationships
→ Set strategy
→ Maintain quality

Agree or disagree?

#AI #HumanInTheLoop #BusinessAutomation"""
        ]

        import random
        return random.choice(insights)

    def _generate_engagement_post(self) -> str:
        """Generate engagement post"""

        questions = [
            """❓ Quick Question for Business Owners:

What's the ONE task you wish you could automate but haven't yet?

For me, it was email triage. Now our AI handles it and saves 10+ hours/week.

Drop your answer below 👇

#BusinessAutomation #Productivity #SmallBusiness""",

            """🗳️ Poll Time:

What's your biggest time sink?

A) Email management
B) Social media posting
C) Lead follow-up
D) Administrative tasks

Comment your answer + how you're solving it!

#BusinessEfficiency #TimeManagement #Automation""",

            """💬 Let's Discuss:

"AI will replace jobs" vs "AI will create jobs"

My take: AI will eliminate tasks, not jobs.

The jobs that survive will be:
→ More strategic
→ More creative
→ More human

What's your perspective?

#FutureOfWork #AI #BusinessTrends"""
        ]

        import random
        return random.choice(questions)

    def _generate_automation_showcase(self, activity: dict) -> str:
        """Generate post showcasing automation capabilities"""

        return f"""🤖 Behind the Scenes: My AI Employee

Here's what my AI automation system did this week:

📧 Email Management:
• Monitored inbox 24/7
• Processed {activity['emails_processed']} messages
• Drafted responses for approval
• Zero missed inquiries

📱 Lead Capture:
• Monitored WhatsApp for keywords
• Captured {activity['leads_captured']} new leads
• Logged to CRM automatically
• Flagged urgent requests

📊 Business Intelligence:
• Generated weekly CEO briefing
• Tracked revenue and metrics
• Identified bottlenecks
• Suggested optimizations

Time saved: 15+ hours/week
Cost: Less than a coffee per day

The future is here. Are you ready?

#AIAutomation #BusinessIntelligence #Productivity #SmallBusinessTech"""

    def create_post_approval_request(self, post_type: str = 'business_update'):
        """Create LinkedIn post and request approval"""

        self.logger.info(f"Generating {post_type} post...")

        # Generate content
        post_content = self.generate_post_content(post_type)

        # Create approval file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        approval_file = self.pending_approval / f"LINKEDIN_POST_{post_type}_{timestamp}.md"

        approval_content = f"""---
type: linkedin_post
action: post_linkedin
post_type: {post_type}
created: {datetime.now().isoformat()}
status: pending_approval
character_count: {len(post_content)}
---

# LinkedIn Post - PENDING APPROVAL

**Type:** {post_type.replace('_', ' ').title()}
**Created:** {datetime.now().isoformat()}
**Character Count:** {len(post_content)}
**Platform:** LinkedIn
**Account:** {os.getenv('LINKEDIN_EMAIL', 'your_account')}

## Post Content

{post_content}

## Posting Instructions

**Best Times to Post:**
- Monday-Friday: 9:00 AM, 12:00 PM, 5:00 PM
- Avoid: Weekends, late nights

**Engagement Tips:**
- Respond to comments within 2 hours
- Ask follow-up questions
- Tag relevant connections
- Share in relevant groups

## Actions
- [ ] Approve and schedule post
- [ ] Edit content and approve
- [ ] Reject and generate new post

## To Approve
1. Review content above
2. Make any edits needed
3. Move this file to /Approved folder
4. Post will be published to LinkedIn

## To Reject
Delete this file or move to /Rejected folder

---
*This post requires human approval before publishing*
*Generated by AI Content Generator v2.0*
"""

        approval_file.write_text(approval_content, encoding='utf-8')
        self.logger.info(f"Created approval request: {approval_file.name}")

        return approval_file

    def generate_weekly_posts(self):
        """Generate a week's worth of LinkedIn posts"""

        self.logger.info("=" * 70)
        self.logger.info("LinkedIn Content Generator - Weekly Batch")
        self.logger.info("=" * 70)

        post_schedule = [
            ('Monday', 'business_update'),
            ('Wednesday', 'industry_insight'),
            ('Friday', 'engagement')
        ]

        for day, post_type in post_schedule:
            self.logger.info(f"Generating {day} post ({post_type})...")
            self.create_post_approval_request(post_type)
            time.sleep(1)

        self.logger.info("")
        self.logger.info("✅ Generated 3 posts for the week")
        self.logger.info(f"📁 Check: {self.pending_approval}")
        self.logger.info("👀 Review and approve posts before publishing")
        self.logger.info("")

def main():
    """Main entry point"""
    vault_path = Path(__file__).parent / "AI_Employee_Vault"

    if not vault_path.exists():
        print(f"ERROR: Vault not found at {vault_path}")
        return

    generator = LinkedInContentGenerator(str(vault_path))

    print("=" * 70)
    print("LinkedIn Content Generator")
    print("=" * 70)
    print()
    print("Options:")
    print("1. Generate single post (business update)")
    print("2. Generate single post (industry insight)")
    print("3. Generate single post (engagement)")
    print("4. Generate weekly batch (3 posts)")
    print()

    choice = input("Enter choice (1-4): ").strip()

    if choice == '1':
        generator.create_post_approval_request('business_update')
    elif choice == '2':
        generator.create_post_approval_request('industry_insight')
    elif choice == '3':
        generator.create_post_approval_request('engagement')
    elif choice == '4':
        generator.generate_weekly_posts()
    else:
        print("Invalid choice")
        return

    print()
    print("✅ Post(s) generated!")
    print(f"📁 Check: {vault_path / 'Pending_Approval'}")
    print("👀 Review and approve before publishing")

if __name__ == "__main__":
    main()
