#!/bin/bash
# Silver Tier Verification Script
# Checks all components are ready for submission

echo "=========================================="
echo "SILVER TIER VERIFICATION"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        ((ERRORS++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (MISSING)"
        ((ERRORS++))
        return 1
    fi
}

echo "1. CHECKING BRONZE TIER WATCHERS (100%)"
echo "----------------------------------------"
check_file "Platinum_Tier/gmail_watcher_hackathon.py"
check_file "Platinum_Tier/linkedin_watcher_hackathon.py"
check_file "Platinum_Tier/whatsapp_watcher_hackathon.py"
check_file "orchestrator.py"
echo ""

echo "2. CHECKING SILVER TIER COMPONENTS (85%)"
echo "----------------------------------------"
check_file "approval_handler.py"
check_file "scheduler.py"
check_file "mcp_servers/email-mcp/index.js"
check_file "mcp_servers/email-mcp/package.json"
check_file "mcp_servers/email-mcp/README.md"
check_file "mcp.json"
check_file "RUN_SILVER_TIER.bat"
echo ""

echo "3. CHECKING OBSIDIAN VAULT"
echo "----------------------------------------"
check_dir "AI_Employee_Vault"
check_dir "AI_Employee_Vault/Inbox"
check_dir "AI_Employee_Vault/Needs_Action"
check_dir "AI_Employee_Vault/Pending_Approval"
check_dir "AI_Employee_Vault/Approved"
check_dir "AI_Employee_Vault/Done"
check_dir "AI_Employee_Vault/Plans"
check_dir "AI_Employee_Vault/Logs"
check_dir "AI_Employee_Vault/Skills"
check_file "AI_Employee_Vault/Company_Handbook.md"
echo ""

echo "4. CHECKING DOCUMENTATION"
echo "----------------------------------------"
check_file "README.md"
check_file "SILVER_TIER_SUMMARY.md"
check_file "SILVER_TIER_TESTING_GUIDE.md"
check_file "SUBMISSION_CHECKLIST.md"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"
echo ""

echo "5. CHECKING SECURITY"
echo "----------------------------------------"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env exists (credentials configured)"
else
    echo -e "${YELLOW}⚠${NC} .env not found (needs configuration)"
    ((WARNINGS++))
fi

if grep -q "your_" .env.example 2>/dev/null; then
    echo -e "${GREEN}✓${NC} .env.example has placeholders (safe)"
else
    echo -e "${RED}✗${NC} .env.example may contain real credentials"
    ((ERRORS++))
fi

if grep -q "^.env$" .gitignore 2>/dev/null; then
    echo -e "${GREEN}✓${NC} .env is in .gitignore"
else
    echo -e "${RED}✗${NC} .env NOT in .gitignore (SECURITY RISK)"
    ((ERRORS++))
fi
echo ""

echo "6. CHECKING PYTHON DEPENDENCIES"
echo "----------------------------------------"
python -c "import playwright" 2>/dev/null && echo -e "${GREEN}✓${NC} playwright" || { echo -e "${RED}✗${NC} playwright"; ((ERRORS++)); }
python -c "import schedule" 2>/dev/null && echo -e "${GREEN}✓${NC} schedule" || { echo -e "${RED}✗${NC} schedule"; ((ERRORS++)); }
python -c "import watchdog" 2>/dev/null && echo -e "${GREEN}✓${NC} watchdog" || { echo -e "${RED}✗${NC} watchdog"; ((ERRORS++)); }
python -c "import dotenv" 2>/dev/null && echo -e "${GREEN}✓${NC} python-dotenv" || { echo -e "${RED}✗${NC} python-dotenv"; ((ERRORS++)); }
echo ""

echo "7. CHECKING NODE.JS DEPENDENCIES"
echo "----------------------------------------"
if [ -d "mcp_servers/email-mcp/node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules installed"
else
    echo -e "${RED}✗${NC} node_modules not installed"
    ((ERRORS++))
fi

if [ -f "mcp_servers/email-mcp/node_modules/@modelcontextprotocol/sdk/package.json" ]; then
    echo -e "${GREEN}✓${NC} @modelcontextprotocol/sdk"
else
    echo -e "${RED}✗${NC} @modelcontextprotocol/sdk"
    ((ERRORS++))
fi

if [ -f "mcp_servers/email-mcp/node_modules/nodemailer/package.json" ]; then
    echo -e "${GREEN}✓${NC} nodemailer"
else
    echo -e "${RED}✗${NC} nodemailer"
    ((ERRORS++))
fi
echo ""

echo "8. CODE STATISTICS"
echo "----------------------------------------"
echo "Python files:"
wc -l approval_handler.py scheduler.py orchestrator.py 2>/dev/null | tail -1
echo ""
echo "Watcher files:"
wc -l Platinum_Tier/gmail_watcher_hackathon.py Platinum_Tier/linkedin_watcher_hackathon.py Platinum_Tier/whatsapp_watcher_hackathon.py 2>/dev/null | tail -1
echo ""
echo "MCP server:"
wc -l mcp_servers/email-mcp/index.js 2>/dev/null
echo ""

echo "=========================================="
echo "VERIFICATION SUMMARY"
echo "=========================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Silver Tier (85%) is ready for submission!"
    echo ""
    echo "Next steps:"
    echo "1. Test with: RUN_SILVER_TIER.bat"
    echo "2. Record demo video (5-10 minutes)"
    echo "3. Create GitHub repository"
    echo "4. Submit to hackathon"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ PASSED WITH $WARNINGS WARNING(S)${NC}"
    echo ""
    echo "Silver Tier is mostly ready, but check warnings above."
    exit 0
else
    echo -e "${RED}✗ FAILED WITH $ERRORS ERROR(S) AND $WARNINGS WARNING(S)${NC}"
    echo ""
    echo "Fix errors above before submission."
    exit 1
fi
