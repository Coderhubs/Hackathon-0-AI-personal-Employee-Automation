#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Post Scheduler with AI Image Generation
Schedules posts at optimal times with generated images
"""

import sys
import io
import json
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Optimal posting times (IST - Indian Standard Time)
POSTING_SCHEDULE = [
    "09:00",  # Morning - professionals checking LinkedIn
    "12:30",  # Lunch break
    "17:00",  # Evening - end of workday
    "20:00",  # Night - casual browsing
]

# LinkedIn cookie (will be loaded from config)
LINKEDIN_COOKIE = None

def load_config():
    """Load configuration including LinkedIn cookie"""
    global LINKEDIN_COOKIE
    config_file = Path(__file__).parent / "linkedin_automation_config.json"

    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            LINKEDIN_COOKIE = config.get('linkedin_cookie')
            print(f"✅ Loaded config from {config_file}")
    else:
        print("⚠️  No config file found. Creating one...")
        if len(sys.argv) > 1:
            LINKEDIN_COOKIE = sys.argv[1]
            config = {'linkedin_cookie': LINKEDIN_COOKIE}
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Saved cookie to {config_file}")
        else:
            print("❌ Please provide LinkedIn cookie as argument")
            sys.exit(1)

def get_next_post():
    """Get the next scheduled post from Approved folder"""
    approved_folder = Path(__file__).parent / "AI_Employee_Vault" / "Approved"
    posts = sorted(approved_folder.glob("*.md"))
    return posts[0] if posts else None

def post_to_linkedin():
    """Post the next scheduled item to LinkedIn"""
    print("\n" + "="*60)
    print(f"⏰ SCHEDULED POST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    next_post = get_next_post()
    if not next_post:
        print("📭 No posts in queue. Skipping this slot.")
        return

    print(f"📄 Posting: {next_post.name}")

    # Run the posting script
    try:
        result = subprocess.run(
            ['python', 'linkedin_cookie_post.py', LINKEDIN_COOKIE],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        if result.returncode == 0:
            print("✅ Post published successfully!")
            print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
        else:
            print("❌ Posting failed!")
            print(result.stderr[-200:] if len(result.stderr) > 200 else result.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")

def schedule_posts():
    """Schedule posts at optimal times"""
    print("="*60)
    print("LINKEDIN POST SCHEDULER")
    print("="*60)
    print("\n📅 Scheduling posts at optimal times:")

    for post_time in POSTING_SCHEDULE:
        schedule.every().day.at(post_time).do(post_to_linkedin)
        print(f"   • {post_time} IST")

    print("\n✅ Scheduler is running...")
    print("Press Ctrl+C to stop\n")

    # Show next scheduled post
    next_run = schedule.next_run()
    if next_run:
        print(f"⏰ Next post: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def main():
    load_config()

    if not LINKEDIN_COOKIE:
        print("❌ No LinkedIn cookie found!")
        return

    print(f"🔑 Cookie loaded: {LINKEDIN_COOKIE[:20]}...")

    # Check if there are posts to schedule
    approved_folder = Path(__file__).parent / "AI_Employee_Vault" / "Approved"
    post_count = len(list(approved_folder.glob("*.md")))
    print(f"📊 Posts in queue: {post_count}")

    if post_count == 0:
        print("\n⚠️  No posts in Approved folder!")
        print("Generate some posts first, then run this scheduler.")
        return

    # Start scheduling
    schedule_posts()

if __name__ == "__main__":
    main()
