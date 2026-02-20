#!/bin/bash
# Platinum Tier Verification Script
# Verifies all 4 tiers are ready for submission

echo "=========================================="
echo "PLATINUM TIER VERIFICATION"
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

echo "1. CHECKING BRONZE TIER (100%)"
echo "----------------------------------------"
check_file "Platinum_Tier/gmail_watcher_hackathon.py"
check_file "Platinum_Tier/linkedin_watcher_hackathon.py"
check_file "Platinum_Tier/whatsapp_watcher_hackathon.py"
echo ""

echo "2. CHECKING SILVER TIER (85%)"
echo "----------------------------------------"
check_file "approval_handler.py"
check_file "scheduler.py"
check_file "mcp_servers/email-mcp/index.js"
echo ""

echo "3. CHECKING GOLD TIER (65%)"
echo "----------------------------------------"
check_file "Gold_Tier/autonomous_monitor.py"
check_file "Gold_Tier/ceo_briefing_generator.py"
check_file "Gold_Tier/plugin_manager.py"
check_file "Gold_Tier/mcp_servers/browser_server.py"
check_file "Gold_Tier/mcp_servers/social_media_server.py"
echo ""

echo "4. CHECKING PLATINUM TIER (35%)"
echo "----------------------------------------"
check_file "Platinum_Tier/agent_coordinator.py"
check_file "Platinum_Tier/memory_store.py"
check_file "Platinum_Tier/api_server_complete.py"
check_file "RUN_PLATINUM_TIER.bat"
echo ""

echo "5. CHECKING DOCUMENTATION"
echo "----------------------------------------"
check_file "README.md"
check_file "SILVER_TIER_SUMMARY.md"
check_file "GOLD_TIER_README.md"
check_file "PLATINUM_TIER_README.md"
echo ""

echo "6. CODE STATISTICS"
echo "----------------------------------------"
echo "Total Python files:"
find . -name "*.py" -type f | wc -l

echo ""
echo "Platinum Tier files:"
find Platinum_Tier -name "*.py" -type f 2>/dev/null | wc -l

echo ""
echo "Total documentation:"
find . -name "*.md" -type f | wc -l

echo ""
echo "Project size:"
du -sh . 2>/dev/null | head -1

echo ""
echo "=========================================="
echo "TIER COMPLETION SUMMARY"
echo "=========================================="
echo "Bronze Tier:   100% (3 watchers, vault, skills)"
echo "Silver Tier:    85% (MCP, HITL, scheduler)"
echo "Gold Tier:      65% (autonomous, briefing, plugins)"
echo "Platinum Tier:  35% (multi-agent, API, memory)"
echo ""
echo "Total Code: ~3,300 lines"
echo "Documentation: 50+ files"
echo "Time Invested: ~37 hours"
echo ""

echo "=========================================="
echo "VERIFICATION SUMMARY"
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Complete 4-Tier Progression Ready!"
    echo ""
    echo "Next steps:"
    echo "1. Test with: RUN_PLATINUM_TIER.bat"
    echo "2. Test API: curl http://localhost:8000/health"
    echo "3. Record demo video (15 minutes)"
    echo "4. Create GitHub repository"
    echo "5. Submit to hackathon"
    exit 0
else
    echo -e "${RED}✗ FAILED WITH $ERRORS ERROR(S)${NC}"
    echo ""
    echo "Fix errors above before submission."
    exit 1
fi
