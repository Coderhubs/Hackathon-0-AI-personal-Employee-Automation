"""
LinkedIn Content Generator - Automated Post Creation
Generates LinkedIn posts based on business activity and schedules them for approval
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger('LinkedInContentGenerator')


class LinkedInContentGenerator:
    """Generates LinkedIn content automatically"""

    def __init__(self, vault_path: str = "AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.pending_approval = self.vault_path / "Pending_Approval"
        self.done = self.vault_path / "Done"
        self.pending_approval.mkdir(parents=True, exist_ok=True)

        # Content templates
        self.post_types = [
            'business_update',
            'industry_insight',
            'engagement',
            'automation_showcase'
        ]

    def generate_business_update(self) -> str:
        """Generate a business update post"""
        templates = [
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

#FutureOfWork #AI #BusinessGrowth""",

            f"""📊 Weekly Progress Update

This week's automation wins:
✅ 47 emails triaged automatically
✅ 12 client responses drafted
✅ 3 social posts scheduled
✅ Zero manual data entry

The AI handles the routine.
I focus on the strategic.

That's the power of a Digital FTE.

#Productivity #AIAutomation #SmartBusiness""",

            f"""💡 Automation Milestone Reached

My AI Personal Employee just completed its 100th task autonomously.

From email triage to draft generation, it's handling the repetitive work while I focus on growth.

The ROI? 10+ hours saved per week.
The cost? Less than a coffee subscription.

This is the future of solo entrepreneurship.

#SoloPreneur #AITools #BusinessAutomation"""
        ]

        import random
        return random.choice(templates)

    def generate_industry_insight(self) -> str:
        """Generate an industry insight post"""
        templates = [
            f"""💭 Lesson Learned: The 80/20 of Automation

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

            f"""🤔 The Digital FTE Shift

We're moving from:
"How many employees do you have?"

To:
"How many Digital FTEs are working for you?"

A Digital FTE:
• Works 24/7 (8,760 hours/year vs 2,000)
• Costs 85% less per task
• Never needs training
• Scales instantly

The question isn't "if" anymore.
It's "how fast can you deploy?"

#FutureOfWork #DigitalTransformation #AI""",

            f"""⚡ The Automation Paradox

The more I automate, the more human my work becomes.

AI handles:
→ Email sorting
→ Data entry
→ Routine responses
→ Scheduling

I focus on:
→ Strategy
→ Relationships
→ Creative problem-solving
→ High-value decisions

Automation doesn't replace humans.
It elevates them.

#AIAutomation #FutureOfWork #Productivity"""
        ]

        import random
        return random.choice(templates)

    def generate_engagement_post(self) -> str:
        """Generate an engagement post"""
        templates = [
            f"""💬 Let's Discuss:

"AI will replace jobs" vs "AI will create jobs"

My take: AI will eliminate tasks, not jobs.

The jobs that survive will be:
→ More strategic
→ More creative
→ More human

What's your perspective?

#FutureOfWork #AI #BusinessTrends""",

            f"""🎯 Quick Poll:

What's your biggest time-waster at work?

A) Email management
B) Data entry
C) Scheduling meetings
D) Routine follow-ups

Drop your answer below 👇

(Hint: All of these can be automated)

#Productivity #WorkSmarter #Automation""",

            f"""💡 Unpopular Opinion:

If you're still manually sorting emails in 2026, you're working too hard.

Automation isn't about being lazy.
It's about being strategic.

Agree or disagree?

#ProductivityHacks #AITools #WorkSmart"""
        ]

        import random
        return random.choice(templates)

    def generate_automation_showcase(self) -> str:
        """Generate an automation showcase post"""
        templates = [
            f"""🤖 Behind the Scenes: My AI Employee

Here's what it does while I sleep:

🌙 Overnight:
• Monitors Gmail for urgent messages
• Categorizes by priority
• Drafts responses for my review

☀️ Morning:
• Delivers a briefing of what needs attention
• Suggests actions based on my rules
• Waits for my approval before sending

The result? I wake up to organized, actionable intelligence.

Not chaos. Not overwhelm. Just clarity.

#AIAutomation #ProductivityTools #SmartWork""",

            f"""📈 ROI of My AI Personal Employee

Investment: $50/month (Claude API + tools)
Time saved: 10 hours/week
Value of time: $100/hour

Monthly ROI: $4,000 value for $50 cost
That's 80x return.

Tasks automated:
✅ Email triage
✅ Response drafting
✅ Social media scheduling
✅ Data logging
✅ Follow-up reminders

This isn't the future. It's available today.

#BusinessAutomation #ROI #AITools""",

            f"""🔧 Tech Stack: My Digital FTE

Brain: Claude Code (reasoning engine)
Memory: Obsidian (local knowledge base)
Senses: Python watchers (Gmail, LinkedIn, WhatsApp)
Hands: MCP servers (external actions)

Cost: ~$50/month
Availability: 24/7
Errors: Near zero with human-in-the-loop

This is what a $500/month Digital FTE looks like.

Questions? Drop them below 👇

#TechStack #AIAutomation #DigitalFTE"""
        ]

        import random
        return random.choice(templates)

    def create_post_approval_request(self, post_type: str) -> Path:
        """Create a LinkedIn post approval request"""

        # Generate content based on type
        if post_type == 'business_update':
            content = self.generate_business_update()
        elif post_type == 'industry_insight':
            content = self.generate_industry_insight()
        elif post_type == 'engagement':
            content = self.generate_engagement_post()
        elif post_type == 'automation_showcase':
            content = self.generate_automation_showcase()
        else:
            content = self.generate_business_update()

        # Create approval file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"LINKEDIN_POST_{post_type}_{timestamp}.md"
        filepath = self.pending_approval / filename

        # Write approval request
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"""---
type: linkedin_post
action: post_linkedin
post_type: {post_type}
created: {datetime.now().isoformat()}
status: pending_approval
character_count: {len(content)}
---

# LinkedIn Post - PENDING APPROVAL

**Type:** {post_type.replace('_', ' ').title()}
**Created:** {datetime.now().isoformat()}
**Character Count:** {len(content)}
**Platform:** LinkedIn
**Account:** {os.getenv('LINKEDIN_EMAIL', 'Not configured')}

## Post Content

{content}

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
""")

        logger.info(f"Created LinkedIn post approval request: {filename}")
        return filepath

    def generate_weekly_posts(self, count: int = 3):
        """Generate a week's worth of LinkedIn posts"""
        logger.info(f"Generating {count} LinkedIn posts for the week...")

        # Recommended posting schedule
        post_schedule = [
            ('Monday', 'business_update'),
            ('Wednesday', 'industry_insight'),
            ('Friday', 'engagement')
        ]

        created_posts = []
        for day, post_type in post_schedule[:count]:
            filepath = self.create_post_approval_request(post_type)
            created_posts.append(filepath)
            logger.info(f"  → {day}: {post_type}")

        logger.info(f"✓ Generated {len(created_posts)} posts")
        logger.info(f"  Review them in: {self.pending_approval}")

        return created_posts

    def generate_single_post(self, post_type: str = None):
        """Generate a single LinkedIn post"""
        if post_type is None:
            import random
            post_type = random.choice(self.post_types)

        logger.info(f"Generating single LinkedIn post: {post_type}")
        filepath = self.create_post_approval_request(post_type)
        logger.info(f"✓ Post created: {filepath.name}")

        return filepath


def main():
    """Main entry point"""
    print("=" * 70)
    print("LinkedIn Content Generator")
    print("=" * 70)
    print()

    generator = LinkedInContentGenerator()

    # Generate weekly posts
    print("Generating weekly LinkedIn posts...")
    posts = generator.generate_weekly_posts(count=3)

    print()
    print(f"✓ Created {len(posts)} LinkedIn posts")
    print(f"  Location: {generator.pending_approval}")
    print()
    print("Next steps:")
    print("  1. Review posts in Pending_Approval/ folder")
    print("  2. Edit content if needed")
    print("  3. Move to Approved/ folder to publish")
    print("  4. Start approval_handler.py to execute")
    print()


if __name__ == "__main__":
    main()
