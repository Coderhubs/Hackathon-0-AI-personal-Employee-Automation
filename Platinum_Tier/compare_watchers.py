"""
Quick comparison test: Mock vs Playwright watchers
Shows the difference between fake and real implementations
"""
import os
from pathlib import Path

def compare_implementations():
    print("=" * 70)
    print("GMAIL & LINKEDIN WATCHERS - IMPLEMENTATION COMPARISON")
    print("=" * 70)

    # Check which files exist
    mock_gmail = Path("gmail_watcher.py")
    real_gmail = Path("gmail_watcher_playwright.py")
    mock_linkedin = Path("linkedin_watcher.py")
    real_linkedin = Path("linkedin_watcher_playwright.py")

    print("\n[FILES AVAILABLE]")
    print("-" * 70)

    print("\nGmail Watchers:")
    if mock_gmail.exists():
        print(f"  [OK] {mock_gmail} (Mock - creates fake emails)")
    if real_gmail.exists():
        print(f"  [OK] {real_gmail} (Real - fetches actual Gmail)")

    print("\nLinkedIn Watchers:")
    if mock_linkedin.exists():
        print(f"  [OK] {mock_linkedin} (Mock - creates fake posts)")
    if real_linkedin.exists():
        print(f"  [OK] {real_linkedin} (Real - fetches actual LinkedIn)")

    print("\n" + "=" * 70)
    print("FEATURE COMPARISON")
    print("=" * 70)

    comparison = [
        ("Feature", "Mock Implementation", "Playwright Implementation"),
        ("-" * 20, "-" * 20, "-" * 25),
        ("Data Source", "Random fake data", "Real Gmail/LinkedIn"),
        ("Authentication", "None required", "Your credentials"),
        ("Browser", "No browser", "Chrome/Chromium"),
        ("Setup Time", "Instant", "5-10 minutes"),
        ("Disk Space", "< 1 MB", "~500 MB"),
        ("Reliability", "100%", "~90%"),
        ("Internet", "Not required", "Required"),
        ("Rate Limits", "None", "May hit limits"),
        ("ToS Compliance", "N/A", "May violate ToS"),
        ("Testing", "Perfect for testing", "Production use"),
    ]

    print()
    for row in comparison:
        print(f"{row[0]:<20} | {row[1]:<20} | {row[2]:<25}")

    print("\n" + "=" * 70)
    print("CURRENT STATUS")
    print("=" * 70)

    # Check disk space
    import shutil
    total, used, free = shutil.disk_usage("C:\\")
    free_mb = free / (1024**2)
    free_gb = free / (1024**3)

    print(f"\n[DISK SPACE] {free_mb:.0f} MB ({free_gb:.2f} GB) free on C:")

    if free_gb < 0.5:
        print("   [ERROR] CRITICAL: Not enough space for Playwright")
        print("   [WARN]  Need at least 2-3 GB free")
        print("\n   RECOMMENDATION: Use MOCK watchers for now")
        print("   They work perfectly for testing and development!")
    elif free_gb < 2:
        print("   [WARN]  WARNING: Low disk space")
        print("   Playwright needs ~500 MB for browsers")
    else:
        print("   [OK] Sufficient space for Playwright")

    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)

    if free_gb < 0.5:
        print("\n[ACTION] IMMEDIATE ACTION:")
        print("   1. Use MOCK watchers (they're already working!)")
        print("   2. Free up disk space when convenient")
        print("   3. Switch to Playwright later for real data")
        print("\n   To test mock watchers:")
        print("   python gmail_watcher.py")
        print("   python linkedin_watcher.py")
    else:
        print("\n[ACTION] NEXT STEPS:")
        print("   1. Install Playwright: pip install playwright python-dotenv")
        print("   2. Install browsers: playwright install chromium")
        print("   3. Configure .env with your credentials")
        print("   4. Run: python test_playwright_setup.py")
        print("   5. Start watchers:")
        print("      python gmail_watcher_playwright.py")
        print("      python linkedin_watcher_playwright.py")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    compare_implementations()
