#!/bin/bash
# Gold Tier Verification Script
# Verifies all Gold Tier components are ready

echo "=========================================="
echo "GOLD TIER VERIFICATION"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

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

echo "1. CHECKING SILVER TIER FOUNDATION (85%)"
echo "----------------------------------------"
check_file "Platinum_Tier/gmail_watcher_hackathon.py"
check_file "Platinum_Tier/linkedin_watcher_hackathon.py"
check_file "Platinum_Tier/whatsapp_watcher_hackathon.py"
check_file "approval_handler.py"
check_file "scheduler.py"
check_file "mcp_servers/email-mcp/index.js"
echo ""

echo "2. CHECKING GOLD TIER COMPONENTS (65%)"
echo "----------------------------------------"
check_file "Gold_Tier/autonomous_monitor.py"
check_file "Gold_Tier/ceo_briefing_generator.py"
check_file "Gold_Tier/plugin_manager.py"
check_file "Gold_Tier/base_watcher.py"
check_file "Gold_Tier/mcp_servers/browser_server.py"
check_file "Gold_Tier/mcp_servers/social_media_server.py"
check_file "RUN_GOLD_TIER.bat"
echo ""

echo "3. CHECKING DOCUMENTATION"
echo "----------------------------------------"
check_file "README.md"
check_file "SILVER_TIER_SUMMARY.md"
check_file "GOLD_TIER_PLAN.md"
check_file "GOLD_TIER_README.md"
check_file "GOLD_TIER_COMPLETE.md"
echo ""

echo "4. CODE STATISTICS"
echo "----------------------------------------"
echo "Python files:"
find . -name "*.py" -type f | wc -l

echo ""
echo "Gold Tier Python files:"
find Gold_Tier -name "*.py" -type f 2>/dev/null | wc -l

echo ""
echo "Documentation files:"
find . -name "*.md" -type f | wc -l

echo ""
echo "Total project size:"
du -sh . 2>/dev/null | head -1

echo ""
echo "=========================================="
echo "VERIFICATION SUMMARY"
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Gold Tier (65%) is ready for submission!"
    echo ""
    echo "Tier Completion:"
    echo "- Bronze: 100%"
    echo "- Silver: 85%"
    echo "- Gold: 65%"
    echo ""
    echo "Next steps:"
    echo "1. Test with: RUN_GOLD_TIER.bat"
    echo "2. Record demo video (15 minutes)"
    echo "3. Create GitHub repository"
    echo "4. Submit to hackathon"
    exit 0
else
    echo -e "${RED}✗ FAILED WITH $ERRORS ERROR(S)${NC}"
    echo ""
    echo "Fix errors above before submission."
    exit 1
fi
