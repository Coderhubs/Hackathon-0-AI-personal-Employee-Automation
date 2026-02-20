"""
Quick Test Script - AI Personal Employee
Run this to test all three platforms quickly
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_whatsapp():
    """Test WhatsApp sending"""
    print("\n" + "="*60)
    print("TESTING WHATSAPP")
    print("="*60)

    try:
        from whatsapp_send import WhatsAppSender

        sender = WhatsAppSender()
        phone = os.getenv('TEST_PHONE_NUMBER', '+923173851441')

        result = sender.send_message(
            phone,
            "🧪 Quick Test: WhatsApp automation is working!"
        )

        if result['success']:
            print("✓ WhatsApp: PASSED")
            print(f"  Message SID: {result['sid']}")
            return True
        else:
            print("✗ WhatsApp: FAILED")
            print(f"  Error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"✗ WhatsApp: ERROR - {e}")
        return False

def test_gmail():
    """Test Gmail sending"""
    print("\n" + "="*60)
    print("TESTING GMAIL")
    print("="*60)

    try:
        sys.path.insert(0, 'Platinum_Tier')
        from gmail_sender_smtp import GmailSender

        email = os.getenv('GMAIL_ADDRESS')
        password = os.getenv('GMAIL_APP_PASSWORD')

        if not email or not password:
            print("✗ Gmail: FAILED - Credentials not found in .env")
            return False

        sender = GmailSender(email, password)

        # Send test email to yourself
        result = sender.send_email(
            to_email=email,
            subject='🧪 Quick Test: Gmail Automation',
            body='This is a test email from your AI Personal Employee. Gmail automation is working!'
        )

        if result:
            print("✓ Gmail: PASSED")
            print(f"  Test email sent to: {email}")
            return True
        else:
            print("✗ Gmail: FAILED")
            return False

    except Exception as e:
        print(f"✗ Gmail: ERROR - {e}")
        return False

def test_linkedin():
    """Test LinkedIn session"""
    print("\n" + "="*60)
    print("TESTING LINKEDIN")
    print("="*60)

    try:
        browser_data = Path("browser_data/linkedin")

        if not browser_data.exists():
            print("✗ LinkedIn: Session not found")
            print("  Run: python setup_linkedin_login.py")
            return False

        print("✓ LinkedIn: Session exists")
        print(f"  Session path: {browser_data}")
        print("  To test posting, run:")
        print('  python linkedin_post_simple.py "Test post"')
        return True

    except Exception as e:
        print(f"✗ LinkedIn: ERROR - {e}")
        return False

def check_vault_structure():
    """Check if vault directories exist"""
    print("\n" + "="*60)
    print("CHECKING VAULT STRUCTURE")
    print("="*60)

    required_dirs = [
        "AI_Employee_Vault/Needs_Action",
        "AI_Employee_Vault/Pending_Approval",
        "AI_Employee_Vault/Approved",
        "AI_Employee_Vault/Done",
        "AI_Employee_Vault/Logs",
        "AI_Employee_Vault/Plans",
        "WhatsApp_Vault/Sent",
        "WhatsApp_Vault/Conversations"
    ]

    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} - MISSING")
            all_exist = False

    return all_exist

def main():
    print("\n" + "="*60)
    print("AI PERSONAL EMPLOYEE - QUICK TEST")
    print("="*60)
    print()

    # Check vault structure
    vault_ok = check_vault_structure()

    # Test each platform
    whatsapp_ok = test_whatsapp()
    gmail_ok = test_gmail()
    linkedin_ok = test_linkedin()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Vault Structure: {'✓ PASS' if vault_ok else '✗ FAIL'}")
    print(f"WhatsApp:        {'✓ PASS' if whatsapp_ok else '✗ FAIL'}")
    print(f"Gmail:           {'✓ PASS' if gmail_ok else '✗ FAIL'}")
    print(f"LinkedIn:        {'✓ PASS' if linkedin_ok else '✗ FAIL'}")
    print("="*60)

    if all([vault_ok, whatsapp_ok, gmail_ok, linkedin_ok]):
        print("\n🎉 ALL TESTS PASSED! System is ready.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        print("\nFor detailed testing guide, see: MANUAL_TESTING_GUIDE.md")

    print()

if __name__ == "__main__":
    main()
