#!/usr/bin/env python3
"""
LinkedIn Automation Test Suite
Tests all components of the LinkedIn 24/7 automation system
"""

import sys
from pathlib import Path
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import schedule
        print("[OK] schedule")
    except ImportError:
        print("[FAIL] schedule - Run: pip install schedule")
        return False

    try:
        from playwright.async_api import async_playwright
        print("[OK] playwright")
    except ImportError:
        print("[FAIL] playwright - Run: pip install playwright && playwright install chromium")
        return False

    try:
        from dotenv import load_dotenv
        print("[OK] python-dotenv")
    except ImportError:
        print("[FAIL] python-dotenv - Run: pip install python-dotenv")
        return False

    try:
        from PIL import Image
        print("[OK] Pillow")
    except ImportError:
        print("[FAIL] Pillow - Run: pip install pillow")
        return False

    return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting files...")

    base_dir = Path(__file__).parent
    required_files = [
        "linkedin_content_generator.py",
        "linkedin_scheduler_complete.py",
        "linkedin_24_7_automation.py",
        "setup_linkedin_login.py"
    ]

    all_exist = True
    for file in required_files:
        file_path = base_dir / file
        if file_path.exists():
            print(f"[OK] {file}")
        else:
            print(f"[FAIL] {file} - Missing!")
            all_exist = False

    return all_exist

def test_vault_structure():
    """Test if vault structure is correct"""
    print("\nTesting vault structure...")

    base_dir = Path(__file__).parent
    vault_path = base_dir / "AI_Employee_Vault"

    required_folders = [
        "Needs_Action",
        "Pending_Approval",
        "Approved",
        "Done",
        "Logs",
        "Plans",
        "Skills"
    ]

    all_exist = True
    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists():
            print(f"[OK] {folder}/")
        else:
            print(f"[WARN] {folder}/ - Creating...")
            folder_path.mkdir(parents=True, exist_ok=True)

    return True

def test_configuration():
    """Test if configuration file is valid"""
    print("\nTesting configuration...")

    base_dir = Path(__file__).parent
    config_file = base_dir / "AI_Employee_Vault" / "linkedin_automation_config.json"

    if not config_file.exists():
        print("⚠️  Configuration file not found - Will be created on first run")
        return True

    try:
        import json
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Check required fields
        required_fields = ['enabled', 'weekly_schedule', 'visibility']
        for field in required_fields:
            if field in config:
                print(f"[OK] {field}")
            else:
                print(f"[FAIL] {field} - Missing!")
                return False

        return True
    except Exception as e:
        print(f"[FAIL] Error reading config: {e}")
        return False

def test_environment():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")

    base_dir = Path(__file__).parent
    env_file = base_dir / ".env"

    if not env_file.exists():
        print("[WARN] .env file not found")
        print("   Create .env with:")
        print("   LINKEDIN_EMAIL=your_email@example.com")
        print("   LINKEDIN_PASSWORD=your_password")
        print("   BUSINESS_NAME=Your Business Name")
        return False

    try:
        from dotenv import load_dotenv
        import os

        load_dotenv()

        required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
        all_set = True

        for var in required_vars:
            value = os.getenv(var)
            if value:
                print(f"[OK] {var}")
            else:
                print(f"[FAIL] {var} - Not set!")
                all_set = False

        return all_set
    except Exception as e:
        print(f"[FAIL] Error checking environment: {e}")
        return False

def test_linkedin_session():
    """Test if LinkedIn session exists"""
    print("\nTesting LinkedIn session...")

    base_dir = Path(__file__).parent
    browser_data = base_dir / "browser_data" / "linkedin"

    if browser_data.exists():
        print("[OK] LinkedIn browser session found")
        return True
    else:
        print("[WARN] LinkedIn browser session not found")
        print("   Run: python setup_linkedin_login.py")
        return False

def test_content_generation():
    """Test content generation"""
    print("\nTesting content generation...")

    try:
        from linkedin_content_generator import LinkedInContentGenerator

        base_dir = Path(__file__).parent
        vault_path = base_dir / "AI_Employee_Vault"

        generator = LinkedInContentGenerator(str(vault_path))

        # Test generating a single post
        content = generator.generate_post_content('business_update')

        if content and len(content) > 0:
            print(f"[OK] Content generated ({len(content)} characters)")
            return True
        else:
            print("[FAIL] Content generation failed")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*80)
    print("LinkedIn 24/7 Automation - Test Suite")
    print("="*80)
    print()

    tests = [
        ("Imports", test_imports),
        ("Files", test_files),
        ("Vault Structure", test_vault_structure),
        ("Configuration", test_configuration),
        ("Environment", test_environment),
        ("LinkedIn Session", test_linkedin_session),
        ("Content Generation", test_content_generation)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[FAIL] {name} test crashed: {e}")
            results.append((name, False))
        print()

    # Summary
    print("="*80)
    print("Test Summary")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python setup_linkedin_login.py (if not done)")
        print("2. Run: START_LINKEDIN_24_7.bat")
    else:
        print("\n[WARNING] Some tests failed. Please fix the issues above.")

    print("="*80)

if __name__ == "__main__":
    run_all_tests()
