#!/usr/bin/env python3
"""
LinkedIn 24/7 Automation System
Automatically generates and posts LinkedIn content on a weekly schedule
"""

import os
import sys
import time
import schedule
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

# Import existing components
sys.path.append(str(Path(__file__).parent))
from linkedin_content_generator import LinkedInContentGenerator
from linkedin_scheduler_complete import LinkedInScheduler

load_dotenv()

class LinkedIn24x7Automation:
    """
    Complete 24/7 LinkedIn automation system.

    Features:
    - Automatic content generation (weekly)
    - Automatic posting (scheduled times)
    - Human approval workflow (optional)
    - Comprehensive logging
    - Error handling and retries
    """

    def __init__(self, auto_approve: bool = False):
        self.base_dir = Path(__file__).parent
        self.vault_path = self.base_dir / "AI_Employee_Vault"
        self.logs_dir = self.vault_path / "Logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.content_generator = LinkedInContentGenerator(str(self.vault_path))
        self.scheduler = LinkedInScheduler()

        # Configuration
        self.auto_approve = auto_approve
        self.config_file = self.vault_path / "linkedin_automation_config.json"
        self.config = self.load_config()

        # Setup logging
        self.logger = self.setup_logging()

        # State tracking
        self.last_content_generation = None
        self.posts_this_week = 0

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs_dir / f"linkedin_24x7_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedIn24x7')

    def load_config(self) -> dict:
        """Load automation configuration"""
        default_config = {
            "enabled": True,
            "auto_approve": False,
            "weekly_schedule": {
                "Monday": {"time": "09:00", "type": "business_update"},
                "Wednesday": {"time": "12:00", "type": "industry_insight"},
                "Friday": {"time": "17:00", "type": "engagement"}
            },
            "visibility": "public",
            "generate_images": True,
            "max_posts_per_week": 3
        }

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)

        # Save default config
        self.save_config(default_config)
        return default_config

    def save_config(self, config: dict):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def generate_weekly_content(self):
        """Generate content for the week"""
        self.logger.info("="*80)
        self.logger.info("Generating Weekly LinkedIn Content")
        self.logger.info("="*80)

        schedule_config = self.config.get("weekly_schedule", {})

        for day, settings in schedule_config.items():
            post_type = settings.get("type", "business_update")
            self.logger.info(f"Generating {day} post ({post_type})...")

            # Generate content
            approval_file = self.content_generator.create_post_approval_request(post_type)

            # Auto-approve if enabled
            if self.auto_approve or self.config.get("auto_approve", False):
                self.auto_approve_post(approval_file)

            time.sleep(2)

        self.last_content_generation = datetime.now()
        self.logger.info("[OK] Weekly content generation complete")
        self.logger.info("="*80)

    def auto_approve_post(self, approval_file: Path):
        """Automatically approve a post"""
        try:
            approved_dir = self.vault_path / "Approved"
            approved_dir.mkdir(parents=True, exist_ok=True)

            approved_file = approved_dir / approval_file.name
            approval_file.rename(approved_file)

            self.logger.info(f"[OK] Auto-approved: {approval_file.name}")
        except Exception as e:
            self.logger.error(f"Error auto-approving: {e}")

    async def post_scheduled_content(self):
        """Post content at scheduled time"""
        self.logger.info("Checking for scheduled posts...")

        try:
            # Process approved posts
            await self.scheduler.process_approved_posts()
            self.posts_this_week += 1

            self.logger.info(f"[OK] Posted successfully (Total this week: {self.posts_this_week})")

        except Exception as e:
            self.logger.error(f"Error posting content: {e}")

    def reset_weekly_counter(self):
        """Reset weekly post counter"""
        self.logger.info("Resetting weekly counter...")
        self.posts_this_week = 0

    def setup_schedule(self):
        """Setup posting schedule"""
        self.logger.info("Setting up posting schedule...")

        schedule_config = self.config.get("weekly_schedule", {})

        for day, settings in schedule_config.items():
            post_time = settings.get("time", "09:00")

            # Schedule post for specific day
            if day == "Monday":
                schedule.every().monday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Tuesday":
                schedule.every().tuesday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Wednesday":
                schedule.every().wednesday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Thursday":
                schedule.every().thursday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Friday":
                schedule.every().friday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Saturday":
                schedule.every().saturday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )
            elif day == "Sunday":
                schedule.every().sunday.at(post_time).do(
                    lambda: asyncio.run(self.post_scheduled_content())
                )

            self.logger.info(f"[OK] Scheduled {day} post at {post_time}")

        # Generate content every Sunday at 8 PM for next week
        schedule.every().sunday.at("20:00").do(self.generate_weekly_content)
        self.logger.info("[OK] Scheduled weekly content generation (Sunday 8 PM)")

        # Reset counter every Sunday
        schedule.every().sunday.at("23:59").do(self.reset_weekly_counter)
        self.logger.info("[OK] Scheduled weekly counter reset (Sunday 11:59 PM)")

    def get_status(self) -> dict:
        """Get current automation status"""
        return {
            "enabled": self.config.get("enabled", True),
            "auto_approve": self.config.get("auto_approve", False),
            "posts_this_week": self.posts_this_week,
            "max_posts_per_week": self.config.get("max_posts_per_week", 3),
            "last_content_generation": self.last_content_generation.isoformat() if self.last_content_generation else "Never",
            "next_scheduled_post": self.get_next_scheduled_time()
        }

    def get_next_scheduled_time(self) -> str:
        """Get next scheduled post time"""
        try:
            next_job = schedule.next_run()
            return next_job.isoformat() if next_job else "No jobs scheduled"
        except:
            return "Unknown"

    def print_status(self):
        """Print current status"""
        status = self.get_status()

        print("\n" + "="*80)
        print("LinkedIn 24/7 Automation - Status")
        print("="*80)
        print(f"Enabled: {status['enabled']}")
        print(f"Auto-Approve: {status['auto_approve']}")
        print(f"Posts This Week: {status['posts_this_week']}/{status['max_posts_per_week']}")
        print(f"Last Content Generation: {status['last_content_generation']}")
        print(f"Next Scheduled Post: {status['next_scheduled_post']}")
        print("="*80 + "\n")

    def run(self):
        """Run 24/7 automation"""
        self.logger.info("="*80)
        self.logger.info("LinkedIn 24/7 Automation - Starting")
        self.logger.info("="*80)
        self.logger.info(f"Auto-approve: {self.auto_approve}")
        self.logger.info(f"Vault path: {self.vault_path}")

        # Setup schedule
        self.setup_schedule()

        # Generate initial content if needed
        if not self.last_content_generation:
            self.logger.info("Generating initial weekly content...")
            self.generate_weekly_content()

        self.logger.info("Automation running. Press Ctrl+C to stop.")
        self.logger.info("="*80)

        # Main loop
        iteration = 0
        try:
            while True:
                iteration += 1

                # Run scheduled tasks
                schedule.run_pending()

                # Print status every 60 iterations (1 minute)
                if iteration % 60 == 0:
                    self.print_status()

                # Sleep for 1 second
                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("\nAutomation stopped by user")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            raise


def main():
    """Main entry point"""
    print("="*80)
    print("LinkedIn 24/7 Automation System")
    print("="*80)
    print()
    print("This system will:")
    print("[OK] Generate LinkedIn posts automatically every week")
    print("[OK] Post at scheduled times (Mon/Wed/Fri)")
    print("[OK] Run 24/7 in the background")
    print()

    # Check for auto-approve mode
    auto_approve = False
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-approve":
        auto_approve = True
        print("[WARNING] AUTO-APPROVE MODE ENABLED")
        print("   Posts will be published without human review!")
        print()
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm != "yes":
            print("Cancelled.")
            return
    else:
        print("[INFO] Manual approval mode (default)")
        print("   Posts will be saved to Pending_Approval/ for review")
        print("   Move to Approved/ folder to publish")
        print()

    # Start automation
    automation = LinkedIn24x7Automation(auto_approve=auto_approve)
    automation.run()


if __name__ == "__main__":
    main()
