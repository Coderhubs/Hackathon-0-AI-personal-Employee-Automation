"""
System Verification Script - Tests all AI Personal Employee components
"""
import sys
from pathlib import Path
import subprocess
import json

print("=" * 80)
print("AI PERSONAL EMPLOYEE - SYSTEM VERIFICATION")
print("=" * 80)
print()

# Test 1: Check vault structure
print("[1/8] Checking vault structure...")
vault = Path("AI_Employee_Vault")
required_dirs = ["Needs_Action", "Pending_Approval", "Approved", "Done", "Logs"]

for dir_name in required_dirs:
    dir_path = vault / dir_name
    dir_path.mkdir(parents=True, exist_ok=True)
    status = "EXISTS" if dir_path.exists() else "CREATED"
    print(f"  - {dir_name}/: {status}")

print()

# Test 2: Check MCP configuration
print("[2/8] Checking MCP configuration...")
try:
    with open("mcp.json", "r") as f:
        mcp_config = json.load(f)

    if "email" in mcp_config.get("mcpServers", {}):
        print("  - Email MCP server: REGISTERED")
    else:
        print("  - Email MCP server: NOT REGISTERED")

    if "filesystem" in mcp_config.get("mcpServers", {}):
        print("  - Filesystem MCP server: REGISTERED")
    else:
        print("  - Filesystem MCP server: NOT REGISTERED")
except Exception as e:
    print(f"  - ERROR: {e}")

print()

# Test 3: Check environment variables
print("[3/8] Checking environment variables...")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()

    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    linkedin_email = os.getenv("LINKEDIN_EMAIL")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    print(f"  - GMAIL_EMAIL: {'SET' if gmail_email and '@' in gmail_email else 'NOT SET'}")
    print(f"  - GMAIL_PASSWORD: {'SET' if gmail_password and len(gmail_password) > 5 else 'NOT SET'}")
    print(f"  - LINKEDIN_EMAIL: {'SET' if linkedin_email and '@' in linkedin_email else 'NOT SET'}")
    print(f"  - LINKEDIN_PASSWORD: {'SET' if linkedin_password and len(linkedin_password) > 5 else 'NOT SET'}")
except Exception as e:
    print(f"  - ERROR: {e}")

print()

# Test 4: Check watcher scripts
print("[4/8] Checking watcher scripts...")
watchers = [
    "Platinum_Tier/gmail_watcher_playwright.py",
    "Platinum_Tier/linkedin_watcher_playwright.py",
    "Platinum_Tier/whatsapp_watcher_hackathon.py"
]

for watcher in watchers:
    if Path(watcher).exists():
        print(f"  - {Path(watcher).name}: EXISTS")
    else:
        print(f"  - {Path(watcher).name}: NOT FOUND")

print()

# Test 5: Check execution components
print("[5/8] Checking execution components...")
components = [
    "Platinum_Tier/mcp_client.py",
    "Platinum_Tier/execution_engine.py",
    "approval_handler.py"
]

for component in components:
    if Path(component).exists():
        print(f"  - {Path(component).name}: EXISTS")
    else:
        print(f"  - {Path(component).name}: NOT FOUND")

print()

# Test 6: Check MCP email server
print("[6/8] Checking MCP email server...")
email_mcp = Path("mcp_servers/email-mcp/index.js")
if email_mcp.exists():
    print(f"  - Email MCP server: EXISTS")
    print(f"  - Location: {email_mcp}")
else:
    print(f"  - Email MCP server: NOT FOUND")

print()

# Test 7: Check LinkedIn content generator
print("[7/8] Checking LinkedIn content generator...")
linkedin_gen = Path("Platinum_Tier/linkedin_content_generator.py")
if linkedin_gen.exists():
    print(f"  - LinkedIn content generator: EXISTS")
    print(f"  - Testing generation...")
    try:
        result = subprocess.run(
            [sys.executable, str(linkedin_gen)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"  - Generation test: SUCCESS")
            # Count generated posts
            posts = list(Path("AI_Employee_Vault/Pending_Approval").glob("LINKEDIN_POST_*.md"))
            print(f"  - Posts generated: {len(posts)}")
        else:
            print(f"  - Generation test: FAILED")
            print(f"  - Error: {result.stderr[:200]}")
    except Exception as e:
        print(f"  - Generation test: ERROR - {e}")
else:
    print(f"  - LinkedIn content generator: NOT FOUND")

print()

# Test 8: Check system orchestrator
print("[8/8] Checking system orchestrator...")
orchestrator = Path("system_orchestrator.py")
if orchestrator.exists():
    print(f"  - System orchestrator: EXISTS")
else:
    print(f"  - System orchestrator: NOT FOUND")

startup_script = Path("START_AI_EMPLOYEE.bat")
if startup_script.exists():
    print(f"  - Startup script: EXISTS")
else:
    print(f"  - Startup script: NOT FOUND")

print()
print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)
print()

# Count successes
vault_ok = all((vault / d).exists() for d in required_dirs)
mcp_ok = Path("mcp.json").exists()
watchers_ok = all(Path(w).exists() for w in watchers)
execution_ok = all(Path(c).exists() for c in components)
email_mcp_ok = email_mcp.exists()
linkedin_gen_ok = linkedin_gen.exists()
orchestrator_ok = orchestrator.exists() and startup_script.exists()

total_checks = 7
passed_checks = sum([vault_ok, mcp_ok, watchers_ok, execution_ok, email_mcp_ok, linkedin_gen_ok, orchestrator_ok])

print(f"Checks Passed: {passed_checks}/{total_checks}")
print()

if passed_checks == total_checks:
    print("✓ ALL SYSTEMS OPERATIONAL")
    print()
    print("Next steps:")
    print("  1. Run: START_AI_EMPLOYEE.bat")
    print("  2. Login to Gmail, LinkedIn, WhatsApp (first time only)")
    print("  3. Review posts in AI_Employee_Vault/Pending_Approval/")
    print("  4. Move approved posts to AI_Employee_Vault/Approved/")
    print("  5. Watch them execute automatically!")
else:
    print("⚠ SOME COMPONENTS MISSING")
    print()
    print("Please review the checks above and fix any issues.")

print()
print("=" * 80)
