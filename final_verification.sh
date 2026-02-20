#!/bin/bash
# Final Verification Script - Run before demo/submission

echo "============================================================"
echo "AI Personal Employee - Final Verification"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}[OK]${NC} $1"
        ((PASS++))
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $1 - NOT FOUND"
        ((FAIL++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}[OK]${NC} $1/"
        ((PASS++))
        return 0
    else
        echo -e "${RED}[FAIL]${NC} $1/ - NOT FOUND"
        ((FAIL++))
        return 1
    fi
}

echo "[1/8] Checking Core Watchers..."
check_file "Platinum_Tier/gmail_watcher_hackathon.py"
check_file "Platinum_Tier/linkedin_watcher_hackathon.py"
check_file "Platinum_Tier/whatsapp_watcher_hackathon.py"
check_file "Platinum_Tier/base_watcher.py"
echo ""

echo "[2/8] Checking Orchestrator..."
check_file "orchestrator.py"
echo ""

echo "[3/8] Checking Vault Structure..."
check_dir "AI_Employee_Vault"
check_dir "AI_Employee_Vault/Needs_Action"
check_dir "AI_Employee_Vault/Plans"
check_dir "AI_Employee_Vault/Done"
check_dir "AI_Employee_Vault/Inbox"
check_file "AI_Employee_Vault/Dashboard.md"
check_file "AI_Employee_Vault/Company_Handbook.md"
echo ""

echo "[4/8] Checking Agent Skills..."
check_dir ".claude/skills"
check_file ".claude/skills/gmail-watcher.md"
check_file ".claude/skills/linkedin-watcher.md"
check_file ".claude/skills/process-inbox.md"
check_file ".claude/skills/update-dashboard.md"
check_file ".claude/skills/run-orchestrator.md"
echo ""

echo "[5/8] Checking Batch Files..."
check_file "RUN_DEMO.bat"
check_file "START_ALL_WATCHERS.bat"
echo ""

echo "[6/8] Checking Documentation..."
check_file "README_HACKATHON.md"
check_file "START_HERE.md"
check_file "ACTION_PLAN.md"
check_file "QUICK_SUMMARY.txt"
check_file "WHATSAPP_WATCHER_EXPLAINED.md"
check_file "COMPLETE_TEST_REPORT.md"
echo ""

echo "[7/8] Checking Credentials..."
if [ -f ".env" ]; then
    echo -e "${GREEN}[OK]${NC} .env file exists"
    ((PASS++))

    if grep -q "GMAIL_EMAIL=fateehaaayat@gmail.com" .env; then
        echo -e "${GREEN}[OK]${NC} Gmail credentials configured"
        ((PASS++))
    else
        echo -e "${RED}[FAIL]${NC} Gmail credentials missing"
        ((FAIL++))
    fi

    if grep -q "LINKEDIN_EMAIL=simramumbai@gmail.com" .env; then
        echo -e "${GREEN}[OK]${NC} LinkedIn credentials configured"
        ((PASS++))
    else
        echo -e "${RED}[FAIL]${NC} LinkedIn credentials missing"
        ((FAIL++))
    fi
else
    echo -e "${RED}[FAIL]${NC} .env file not found"
    ((FAIL++))
fi
echo ""

echo "[8/8] Running Pytest..."
if pytest Platinum_Tier/test_whatsapp_watcher.py -q > /dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} All unit tests passed"
    ((PASS++))
else
    echo -e "${RED}[FAIL]${NC} Some tests failed"
    ((FAIL++))
fi
echo ""

# Summary
echo "============================================================"
echo "VERIFICATION SUMMARY"
echo "============================================================"
echo -e "Passed: ${GREEN}${PASS}${NC}"
echo -e "Failed: ${RED}${FAIL}${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "Your AI Personal Employee is ready for:"
    echo "  1. Demo run (RUN_DEMO.bat)"
    echo "  2. Video recording"
    echo "  3. GitHub submission"
    echo "  4. Hackathon submission"
    echo ""
    echo "Next step: Run RUN_DEMO.bat"
    exit 0
else
    echo -e "${RED}✗ SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please fix the issues above before proceeding."
    exit 1
fi
