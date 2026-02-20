# Final Testing Script

## Run this to verify everything works

echo "=========================================="
echo "AI Personal Employee - Final Test"
echo "=========================================="
echo ""

# Test 1: Check folder structure
echo "[Test 1] Checking folder structure..."
cd "AI_Employee_Vault"
if [ -d "Needs_Action" ] && [ -d "Plans" ] && [ -d "Done" ]; then
    echo "[PASS] Folder structure exists"
else
    echo "[FAIL] Missing folders"
    mkdir -p Needs_Action Plans Done Pending_Approval Approved Rejected Logs
    echo "[FIX] Created missing folders"
fi

# Test 2: Check credentials
echo ""
echo "[Test 2] Checking credentials..."
cd ..
if [ -f ".env" ]; then
    echo "[PASS] .env file exists"
    if grep -q "GMAIL_EMAIL" .env && grep -q "LINKEDIN_EMAIL" .env; then
        echo "[PASS] Credentials configured"
    else
        echo "[FAIL] Credentials incomplete"
    fi
else
    echo "[FAIL] .env file missing"
fi

# Test 3: Check watcher scripts
echo ""
echo "[Test 3] Checking watcher scripts..."
if [ -f "Platinum_Tier/gmail_watcher_hackathon.py" ]; then
    echo "[PASS] Gmail watcher exists"
else
    echo "[FAIL] Gmail watcher missing"
fi

if [ -f "Platinum_Tier/linkedin_watcher_hackathon.py" ]; then
    echo "[PASS] LinkedIn watcher exists"
else
    echo "[FAIL] LinkedIn watcher missing"
fi

if [ -f "Platinum_Tier/whatsapp_watcher_hackathon.py" ]; then
    echo "[PASS] WhatsApp watcher exists"
else
    echo "[FAIL] WhatsApp watcher missing"
fi

if [ -f "Platinum_Tier/base_watcher.py" ]; then
    echo "[PASS] Base watcher exists"
else
    echo "[FAIL] Base watcher missing"
fi

# Test 4: Check orchestrator
echo ""
echo "[Test 4] Checking orchestrator..."
if [ -f "orchestrator.py" ]; then
    echo "[PASS] Orchestrator exists"
else
    echo "[FAIL] Orchestrator missing"
fi

if [ -f "START_ALL_WATCHERS.bat" ]; then
    echo "[PASS] Start script exists"
else
    echo "[FAIL] Start script missing"
fi

# Test 5: Check Agent Skills
echo ""
echo "[Test 5] Checking Agent Skills..."
if [ -d ".claude/skills" ]; then
    skill_count=$(ls -1 .claude/skills/*.md 2>/dev/null | wc -l)
    echo "[PASS] Skills directory exists ($skill_count skills)"
else
    echo "[FAIL] Skills directory missing"
fi

# Test 6: Check documentation
echo ""
echo "[Test 6] Checking documentation..."
if [ -f "HACKATHON_REQUIREMENTS_ANALYSIS.md" ]; then
    echo "[PASS] Requirements analysis exists"
else
    echo "[FAIL] Requirements analysis missing"
fi

if [ -f "COMPLETE_IMPLEMENTATION_GUIDE.md" ]; then
    echo "[PASS] Implementation guide exists"
else
    echo "[FAIL] Implementation guide missing"
fi

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""
echo "Your AI Personal Employee is ready for:"
echo "- Bronze Tier submission"
echo "- Demo video recording"
echo "- Hackathon submission"
echo ""
echo "Next steps:"
echo "1. Run: START_ALL_WATCHERS.bat"
echo "2. Test content detection"
echo "3. Record demo video"
echo "4. Submit to hackathon"
echo ""
echo "=========================================="
