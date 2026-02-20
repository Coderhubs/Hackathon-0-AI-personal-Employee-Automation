#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Safety Checker - Traffic Light System
Checks if it's safe to post based on strict safety rules
"""

import sys
import io
from datetime import datetime, timedelta
from pathlib import Path
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# STRICT SAFETY RULES
MAX_POSTS_PER_DAY = 2
MIN_HOURS_BETWEEN_POSTS = 4
MAX_POSTS_PER_WEEK = 10
POSTING_START_HOUR = 9  # 9 AM
POSTING_END_HOUR = 18   # 6 PM
COOLDOWN_HOURS = 48     # After exceeding limits

def parse_timestamp_from_filename(filename):
    """Extract timestamp from POSTED_YYYYMMDD_HHMMSS_* filename"""
    match = re.search(r'POSTED_(\d{8})_(\d{6})', filename)
    if match:
        date_str = match.group(1)  # YYYYMMDD
        time_str = match.group(2)  # HHMMSS
        return datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
    return None

def get_posted_files():
    """Get all posted files with timestamps"""
    done_folder = Path(__file__).parent / "AI_Employee_Vault" / "Done"
    if not done_folder.exists():
        return []

    posted_files = []
    for file in done_folder.glob("POSTED_*.md"):
        timestamp = parse_timestamp_from_filename(file.name)
        if timestamp:
            posted_files.append({
                'filename': file.name,
                'timestamp': timestamp
            })

    return sorted(posted_files, key=lambda x: x['timestamp'], reverse=True)

def check_safety_status():
    """Check if it's safe to post - Returns: GREEN, YELLOW, or RED"""
    now = datetime.now()
    current_hour = now.hour

    # Get all posted files
    posted_files = get_posted_files()

    if not posted_files:
        # No posts yet - check time only
        if POSTING_START_HOUR <= current_hour < POSTING_END_HOUR:
            return "GREEN", "No posts yet. Safe to post.", []
        else:
            return "YELLOW", f"Outside posting hours (9am-6pm). Current: {current_hour}:00", []

    # Get recent posts
    last_post = posted_files[0]
    hours_since_last = (now - last_post['timestamp']).total_seconds() / 3600

    # Count posts in last 24 hours
    yesterday = now - timedelta(hours=24)
    posts_last_24h = [p for p in posted_files if p['timestamp'] > yesterday]

    # Count posts in last 7 days
    last_week = now - timedelta(days=7)
    posts_last_week = [p for p in posted_files if p['timestamp'] > last_week]

    # Count posts today
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    posts_today = [p for p in posted_files if p['timestamp'] > today_start]

    # Count posts yesterday
    yesterday_start = today_start - timedelta(days=1)
    posts_yesterday = [p for p in posted_files if yesterday_start <= p['timestamp'] < today_start]

    # Check for cooldown period (if we exceeded limits recently)
    if len(posts_last_24h) >= 4:
        hours_in_cooldown = 48 - hours_since_last
        if hours_in_cooldown > 0:
            return "RED", f"COOLDOWN: Posted {len(posts_last_24h)} times in 24h. Wait {hours_in_cooldown:.1f} more hours.", posts_today

    # RED CONDITIONS - DO NOT POST
    red_reasons = []

    if len(posts_today) >= MAX_POSTS_PER_DAY:
        red_reasons.append(f"Already posted {len(posts_today)}/{MAX_POSTS_PER_DAY} times today")

    if hours_since_last < MIN_HOURS_BETWEEN_POSTS:
        red_reasons.append(f"Last post was {hours_since_last:.1f} hours ago (need {MIN_HOURS_BETWEEN_POSTS}h gap)")

    if len(posts_last_week) >= MAX_POSTS_PER_WEEK:
        red_reasons.append(f"Already posted {len(posts_last_week)}/{MAX_POSTS_PER_WEEK} times this week")

    # Special rule: If yesterday had 3+ posts, today max 1 post
    if len(posts_yesterday) >= 3 and len(posts_today) >= 1:
        red_reasons.append(f"Yesterday had {len(posts_yesterday)} posts, today limited to 1 (already posted)")

    if red_reasons:
        return "RED", " | ".join(red_reasons), posts_today

    # YELLOW CONDITIONS - Caution
    yellow_reasons = []

    if not (POSTING_START_HOUR <= current_hour < POSTING_END_HOUR):
        yellow_reasons.append(f"Outside optimal hours (9am-6pm). Current: {current_hour}:00")

    if len(posts_today) >= 1:
        yellow_reasons.append(f"Already posted {len(posts_today)} time(s) today")

    if hours_since_last < 6:
        yellow_reasons.append(f"Last post was {hours_since_last:.1f}h ago (recommended: 6h+ gap)")

    if yellow_reasons:
        return "YELLOW", " | ".join(yellow_reasons), posts_today

    # GREEN - Safe to post
    return "GREEN", f"Safe to post. Last post: {hours_since_last:.1f}h ago. Posts today: {len(posts_today)}/2", posts_today

def print_status_report():
    """Print detailed safety status report"""
    status, reason, posts_today = check_safety_status()
    now = datetime.now()

    posted_files = get_posted_files()

    # Calculate next safe time
    if posted_files:
        last_post = posted_files[0]
        next_safe_time = last_post['timestamp'] + timedelta(hours=MIN_HOURS_BETWEEN_POSTS)

        # If we've hit daily limit, next safe time is tomorrow 9am
        if len(posts_today) >= MAX_POSTS_PER_DAY:
            tomorrow = now + timedelta(days=1)
            next_safe_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        next_safe_time = now

    # Status indicator
    if status == "GREEN":
        indicator = "🟢 GREEN - SAFE TO POST"
    elif status == "YELLOW":
        indicator = "🟡 YELLOW - CAUTION"
    else:
        indicator = "🔴 RED - DO NOT POST"

    print("="*70)
    print("LINKEDIN SAFETY STATUS - TRAFFIC LIGHT SYSTEM")
    print("="*70)
    print(f"\n{indicator}")
    print(f"\nReason: {reason}")
    print(f"Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    if posted_files:
        last_post = posted_files[0]
        hours_ago = (now - last_post['timestamp']).total_seconds() / 3600
        print(f"Last Post: {last_post['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} ({hours_ago:.1f}h ago)")

    print(f"\n📊 POSTING STATISTICS")
    print(f"Posts today: {len(posts_today)}/{MAX_POSTS_PER_DAY}")

    # Count weekly posts
    last_week = now - timedelta(days=7)
    posts_last_week = [p for p in posted_files if p['timestamp'] > last_week]
    print(f"Posts this week: {len(posts_last_week)}/{MAX_POSTS_PER_WEEK}")

    print(f"\n⏰ NEXT SAFE POSTING WINDOW")
    if status == "GREEN":
        print(f"✓ Can post NOW")
    else:
        print(f"⏳ Wait until: {next_safe_time.strftime('%Y-%m-%d %H:%M:%S')}")
        hours_to_wait = (next_safe_time - now).total_seconds() / 3600
        if hours_to_wait > 0:
            print(f"   ({hours_to_wait:.1f} hours from now)")

    print("\n" + "="*70)

    return status

def main():
    status = print_status_report()

    # Exit code: 0 = GREEN, 1 = YELLOW, 2 = RED
    exit_code = {"GREEN": 0, "YELLOW": 1, "RED": 2}[status]
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
