#!/usr/bin/env python3
"""
LinkedIn Automation Status Checker
Quick script to check the status of LinkedIn automation
"""

import json
from pathlib import Path
from datetime import datetime

def check_status():
    """Check LinkedIn automation status"""
    base_dir = Path(__file__).parent
    vault_path = base_dir / "AI_Employee_Vault"

    print("="*80)
    print("LinkedIn 24/7 Automation - Status Check")
    print("="*80)
    print()

    # Check configuration
    config_file = vault_path / "linkedin_automation_config.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)

        print("[Configuration]")
        print(f"   Enabled: {config.get('enabled', False)}")
        print(f"   Auto-Approve: {config.get('auto_approve', False)}")
        print(f"   Max Posts/Week: {config.get('max_posts_per_week', 3)}")
        print(f"   Visibility: {config.get('visibility', 'public')}")
        print(f"   Generate Images: {config.get('generate_images', True)}")
        print()

        print("[Weekly Schedule]")
        schedule = config.get('weekly_schedule', {})
        for day, settings in schedule.items():
            print(f"   {day}: {settings.get('time')} - {settings.get('type')}")
        print()
    else:
        print("[WARNING] Configuration file not found!")
        print(f"   Expected: {config_file}")
        print()

    # Check folders
    pending = vault_path / "Pending_Approval"
    approved = vault_path / "Approved"
    done = vault_path / "Done"

    print("[Folder Status]")

    if pending.exists():
        pending_files = list(pending.glob("LINKEDIN_*.md"))
        print(f"   Pending Approval: {len(pending_files)} post(s)")
        for f in pending_files[:3]:  # Show first 3
            print(f"      - {f.name}")
    else:
        print("   Pending Approval: Folder not found")

    if approved.exists():
        approved_files = list(approved.glob("LINKEDIN_*.md"))
        print(f"   Approved: {len(approved_files)} post(s)")
        for f in approved_files[:3]:
            print(f"      - {f.name}")
    else:
        print("   Approved: Folder not found")

    if done.exists():
        done_files = list(done.glob("LINKEDIN_*.md"))
        print(f"   Done: {len(done_files)} post(s)")
        # Show most recent 3
        recent = sorted(done_files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
        for f in recent:
            mod_time = datetime.fromtimestamp(f.stat().st_mtime)
            print(f"      - {f.name} ({mod_time.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("   Done: Folder not found")

    print()

    # Check logs
    logs_dir = vault_path / "Logs"
    if logs_dir.exists():
        log_files = list(logs_dir.glob("linkedin_*.log"))
        if log_files:
            latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
            print(f"[Latest Log] {latest_log.name}")

            # Show last 10 lines
            try:
                with open(latest_log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    last_lines = lines[-10:] if len(lines) > 10 else lines

                print("\n   Recent Log Entries:")
                for line in last_lines:
                    print(f"   {line.rstrip()}")
            except Exception as e:
                print(f"   Error reading log: {e}")
        else:
            print("[No log files found]")
    else:
        print("[Logs folder not found]")

    print()
    print("="*80)

    # Check if LinkedIn session exists
    browser_data = base_dir / "browser_data" / "linkedin"
    if browser_data.exists():
        print("[OK] LinkedIn browser session found")
    else:
        print("[WARNING] LinkedIn browser session not found")
        print("   Run: python setup_linkedin_login.py")

    print()

    # Check environment variables
    env_file = base_dir / ".env"
    if env_file.exists():
        print("[OK] .env file found")

        # Check for required variables
        with open(env_file, 'r') as f:
            env_content = f.read()

        required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD', 'BUSINESS_NAME']
        missing = []
        for var in required_vars:
            if var not in env_content:
                missing.append(var)

        if missing:
            print(f"[WARNING] Missing environment variables: {', '.join(missing)}")
        else:
            print("[OK] All required environment variables present")
    else:
        print("[WARNING] .env file not found")
        print("   Create .env with: LINKEDIN_EMAIL, LINKEDIN_PASSWORD, BUSINESS_NAME")

    print()
    print("="*80)

    # Quick actions
    print("\n[Quick Actions]")
    print("   1. Generate content now: python linkedin_content_generator.py")
    print("   2. Post approved content: python linkedin_scheduler_complete.py post-now")
    print("   3. Start 24/7 automation: START_LINKEDIN_24_7.bat")
    print("   4. Configure schedule: Edit AI_Employee_Vault/linkedin_automation_config.json")
    print()

if __name__ == "__main__":
    check_status()
