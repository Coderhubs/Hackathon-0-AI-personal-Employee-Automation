#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Safe Post - Wrapper with Traffic Light Safety Check
ALWAYS checks safety before posting
"""

import sys
import io
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def check_safety():
    """Run safety checker and return status"""
    try:
        result = subprocess.run(
            ['python', 'linkedin_safety_check.py'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        # Exit code: 0=GREEN, 1=YELLOW, 2=RED
        return result.returncode, result.stdout
    except Exception as e:
        print(f"Error checking safety: {e}")
        return 2, ""  # Default to RED if check fails

def post_to_linkedin():
    """Post to LinkedIn using cookie from .linkedin_session"""
    try:
        result = subprocess.run(
            ['python', 'linkedin_cookie_post.py'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"Error posting: {e}")
        return False

def main():
    print("="*70)
    print("LINKEDIN SAFE POST - WITH TRAFFIC LIGHT SAFETY CHECK")
    print("="*70)

    # Step 1: Check safety status
    print("\nStep 1: Checking safety status...\n")
    status_code, status_output = check_safety()
    print(status_output)

    # Step 2: Decide based on traffic light
    if status_code == 2:  # RED
        print("\n" + "="*70)
        print("🔴 POSTING BLOCKED - RED STATUS")
        print("="*70)
        print("\nREASONS:")
        print("- Account is in cooldown period")
        print("- OR exceeded daily/weekly limits")
        print("- OR posted too recently")
        print("\nACTION REQUIRED:")
        print("- Wait for the next safe posting window shown above")
        print("- Do NOT attempt to post until status is GREEN")
        print("="*70)
        return 1

    elif status_code == 1:  # YELLOW
        print("\n" + "="*70)
        print("🟡 CAUTION - YELLOW STATUS")
        print("="*70)
        print("\nWARNINGS:")
        print("- Outside optimal posting hours")
        print("- OR already posted today")
        print("- OR short gap since last post")
        print("\nYou CAN post, but it's not optimal.")

        response = input("\nDo you want to proceed anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("\nPosting cancelled. Wait for GREEN status for optimal safety.")
            return 1

        print("\nProceeding with caution...")

    else:  # GREEN
        print("\n" + "="*70)
        print("🟢 SAFE TO POST - GREEN STATUS")
        print("="*70)
        print("\nAll safety checks passed. Proceeding with post...")

    # Step 3: Post to LinkedIn
    print("\nStep 2: Posting to LinkedIn...\n")
    success = post_to_linkedin()

    if success:
        print("\n" + "="*70)
        print("✅ POST SUCCESSFUL")
        print("="*70)
        print("\nNext steps:")
        print("- Wait at least 4 hours before next post")
        print("- Check safety status before posting again")
        print("- Run: python linkedin_safe_post.py")
        print("="*70)
        return 0
    else:
        print("\n" + "="*70)
        print("❌ POST FAILED")
        print("="*70)
        print("\nPossible reasons:")
        print("- Cookie expired (refresh .linkedin_session file)")
        print("- Network error")
        print("- LinkedIn API issue")
        print("\nTry again or check logs for details.")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
