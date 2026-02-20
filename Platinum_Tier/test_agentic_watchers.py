"""
Quick test script to verify Agentic AI watchers are configured correctly
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_setup():
    """Test that everything is configured correctly"""
    print("=" * 70)
    print("Agentic AI Watchers - Configuration Test")
    print("=" * 70)
    print()

    # Check Python version
    print("[1/6] Checking Python version...")
    if sys.version_info < (3, 7):
        print("  [ERROR] Python 3.7+ required")
        return False
    print(f"  [OK] Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check .env file
    print("\n[2/6] Checking .env file...")
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("  [ERROR] .env file not found")
        print("  Run: python Platinum_Tier/setup_credentials.py")
        return False
    print("  [OK] .env file exists")

    # Load and check credentials
    print("\n[3/6] Checking credentials...")
    load_dotenv(env_path)

    gmail_email = os.getenv('GMAIL_EMAIL')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    if not gmail_email or not gmail_password:
        print("  [ERROR] Gmail credentials missing")
        return False
    print(f"  [OK] Gmail: {gmail_email}")

    if not linkedin_email or not linkedin_password:
        print("  [ERROR] LinkedIn credentials missing")
        return False
    print(f"  [OK] LinkedIn: {linkedin_email}")

    # Check required packages
    print("\n[4/6] Checking required packages...")
    try:
        import playwright
        print("  [OK] playwright installed")
    except ImportError:
        print("  [ERROR] playwright not installed")
        print("  Run: pip install playwright")
        return False

    try:
        import dotenv
        print("  [OK] python-dotenv installed")
    except ImportError:
        print("  [ERROR] python-dotenv not installed")
        print("  Run: pip install python-dotenv")
        return False

    # Check Playwright browsers
    print("\n[5/6] Checking Playwright browsers...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("  [OK] Chromium browser installed")
            except Exception as e:
                print("  [ERROR] Chromium browser not installed")
                print("  Run: playwright install chromium")
                return False
    except Exception as e:
        print(f"  [ERROR] Error checking browsers: {e}")
        return False

    # Check Inbox directory
    print("\n[6/6] Checking Inbox directory...")
    inbox_dir = Path("Inbox")
    if not inbox_dir.exists():
        inbox_dir.mkdir()
        print("  [OK] Created Inbox directory")
    else:
        print("  [OK] Inbox directory exists")

    # Summary
    print("\n" + "=" * 70)
    print("[SUCCESS] All checks passed! Your Agentic AI watchers are ready.")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Test Gmail: python Platinum_Tier/demo_gmail.py")
    print("2. Test LinkedIn: python Platinum_Tier/demo_linkedin.py")
    print("3. Run watchers: Platinum_Tier\\RUN_WATCHERS.bat")
    print("\nTo enable sending/posting:")
    print("- Gmail: Edit gmail_watcher_playwright.py line 197")
    print("- LinkedIn: Edit linkedin_watcher_playwright.py line 218")
    print("\nFiltered content will be saved to: Inbox/")
    print("Keywords: agentic, ai agent, autonomous ai, llm, claude, gpt")
    print()

    return True

if __name__ == "__main__":
    try:
        success = test_setup()
        if not success:
            print("\n[ERROR] Setup incomplete. Please fix the issues above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)
