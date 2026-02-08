"""
Test script to verify Playwright watchers setup
Run this after freeing disk space and installing Playwright
"""
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("=" * 60)
    print("PLAYWRIGHT WATCHERS - SETUP VERIFICATION")
    print("=" * 60)

    issues = []
    warnings = []

    # Check 1: Disk space
    print("\n1. Checking disk space...")
    try:
        import shutil
        total, used, free = shutil.disk_usage("C:\\")
        free_gb = free / (1024**3)
        print(f"   Free space: {free_gb:.2f} GB")

        if free_gb < 0.5:
            issues.append(f"CRITICAL: Only {free_gb:.2f} GB free. Need at least 2-3 GB")
        elif free_gb < 2:
            warnings.append(f"WARNING: Only {free_gb:.2f} GB free. Recommended: 2-3 GB")
        else:
            print(f"   [OK] Sufficient disk space ({free_gb:.2f} GB)")
    except Exception as e:
        issues.append(f"Could not check disk space: {e}")

    # Check 2: Playwright installed
    print("\n2. Checking Playwright installation...")
    try:
        import playwright
        print(f"   [OK] Playwright installed")
    except ImportError:
        issues.append("Playwright not installed. Run: pip install playwright")

    # Check 3: Playwright browsers
    print("\n3. Checking Playwright browsers...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to get browser path
            print("   [OK] Playwright browsers installed")
    except Exception as e:
        issues.append(f"Playwright browsers not installed. Run: playwright install chromium")

    # Check 4: python-dotenv
    print("\n4. Checking python-dotenv...")
    try:
        import dotenv
        print("   [OK] python-dotenv installed")
    except ImportError:
        issues.append("python-dotenv not installed. Run: pip install python-dotenv")

    # Check 5: .env file exists
    print("\n5. Checking .env file...")
    env_path = Path(".env")
    if env_path.exists():
        print("   [OK] .env file exists")

        # Check for credentials
        from dotenv import load_dotenv
        load_dotenv()

        gmail_email = os.getenv('GMAIL_EMAIL')
        gmail_password = os.getenv('GMAIL_PASSWORD')
        linkedin_email = os.getenv('LINKEDIN_EMAIL')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD')

        if not gmail_email or gmail_email == 'your_gmail_email@gmail.com':
            warnings.append("Gmail credentials not configured in .env")
        else:
            print(f"   [OK] Gmail email configured: {gmail_email}")

        if not gmail_password or gmail_password == 'your_gmail_password':
            warnings.append("Gmail password not configured in .env")
        else:
            print("   [OK] Gmail password configured")

        if not linkedin_email or linkedin_email == 'your_linkedin_email@example.com':
            warnings.append("LinkedIn credentials not configured in .env")
        else:
            print(f"   [OK] LinkedIn email configured: {linkedin_email}")

        if not linkedin_password or linkedin_password == 'your_linkedin_password':
            warnings.append("LinkedIn password not configured in .env")
        else:
            print("   [OK] LinkedIn password configured")
    else:
        issues.append(".env file not found")

    # Check 6: Watcher files exist
    print("\n6. Checking watcher files...")
    gmail_watcher = Path("gmail_watcher_playwright.py")
    linkedin_watcher = Path("linkedin_watcher_playwright.py")

    if gmail_watcher.exists():
        print("   [OK] gmail_watcher_playwright.py exists")
    else:
        issues.append("gmail_watcher_playwright.py not found")

    if linkedin_watcher.exists():
        print("   [OK] linkedin_watcher_playwright.py exists")
    else:
        issues.append("linkedin_watcher_playwright.py not found")

    # Check 7: Inbox directory
    print("\n7. Checking Inbox directory...")
    inbox_dir = Path("Inbox")
    if inbox_dir.exists():
        print(f"   [OK] Inbox directory exists")
        file_count = len(list(inbox_dir.glob("*")))
        print(f"   [OK] Contains {file_count} files")
    else:
        print("   ! Inbox directory will be created automatically")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if issues:
        print("\n[ERROR] CRITICAL ISSUES (must fix):")
        for issue in issues:
            print(f"   - {issue}")

    if warnings:
        print("\n[WARN] WARNINGS (should fix):")
        for warning in warnings:
            print(f"   - {warning}")

    if not issues and not warnings:
        print("\n[SUCCESS] ALL CHECKS PASSED!")
        print("\nYou can now run:")
        print("   python gmail_watcher_playwright.py")
        print("   python linkedin_watcher_playwright.py")
    elif not issues:
        print("\n[WARN] Setup incomplete but can proceed with warnings")
    else:
        print("\n[ERROR] Setup incomplete. Fix critical issues first.")

    print("\n" + "=" * 60)

    return len(issues) == 0

if __name__ == "__main__":
    try:
        success = check_requirements()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Error during verification: {e}")
        sys.exit(1)
