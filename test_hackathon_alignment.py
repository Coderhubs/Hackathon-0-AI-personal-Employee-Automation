"""
Hackathon Alignment Test Script
Tests current project against Bronze Tier requirements
"""
import os
from pathlib import Path
import json
from datetime import datetime

class HackathonAlignmentTest:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tier': 'Bronze',
            'tests': [],
            'score': 0,
            'max_score': 0
        }

    def test_obsidian_vault(self):
        """Test if Obsidian vault exists with required files"""
        test = {
            'name': 'Obsidian Vault Structure',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        # Check for vault directory
        vault_paths = [
            self.project_root / "AI_Employee_Vault",
            self.project_root / "Vault",
            self.project_root / "Obsidian"
        ]

        vault_found = False
        for vault_path in vault_paths:
            if vault_path.exists():
                vault_found = True
                test['details'].append(f"✓ Vault found: {vault_path}")

                # Check for Dashboard.md
                if (vault_path / "Dashboard.md").exists():
                    test['details'].append("[OK] Dashboard.md exists")
                else:
                    test['details'].append("[MISSING] Dashboard.md missing")

                # Check for Company_Handbook.md
                if (vault_path / "Company_Handbook.md").exists():
                    test['details'].append("[OK] Company_Handbook.md exists")
                else:
                    test['details'].append("[MISSING] Company_Handbook.md missing")

                break

        if not vault_found:
            test['details'].append("✗ No Obsidian vault found")

        test['status'] = 'PASS' if vault_found else 'FAIL'
        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        self.results['max_score'] += 1

    def test_folder_structure(self):
        """Test if required folder structure exists"""
        test = {
            'name': 'Folder Structure',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        required_folders = ['Inbox', 'Needs_Action', 'Done', 'Plans', 'Pending_Approval']
        found_folders = []

        for folder in required_folders:
            folder_path = self.project_root / folder
            if folder_path.exists():
                found_folders.append(folder)
                test['details'].append(f"✓ /{folder} exists")
            else:
                test['details'].append(f"✗ /{folder} missing")

        test['status'] = 'PASS' if len(found_folders) >= 3 else 'PARTIAL' if len(found_folders) > 0 else 'FAIL'
        test['details'].append(f"Found {len(found_folders)}/{len(required_folders)} required folders")

        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        elif test['status'] == 'PARTIAL':
            self.results['score'] += 0.5
        self.results['max_score'] += 1

    def test_watchers(self):
        """Test if watcher scripts exist and are functional"""
        test = {
            'name': 'Watcher Scripts',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        watcher_files = [
            'gmail_watcher_playwright.py',
            'linkedin_watcher_playwright.py',
            'gmail_watcher_session.py',
            'linkedin_watcher_session.py',
            'filesystem_watcher.py',
            'whatsapp_watcher.py'
        ]

        found_watchers = []
        platinum_tier = self.project_root / "Platinum_Tier"

        for watcher in watcher_files:
            watcher_path = platinum_tier / watcher
            if watcher_path.exists():
                found_watchers.append(watcher)
                test['details'].append(f"✓ {watcher} exists")

        test['status'] = 'PASS' if len(found_watchers) >= 1 else 'FAIL'
        test['details'].append(f"Found {len(found_watchers)} watcher scripts")

        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        self.results['max_score'] += 1

    def test_credentials(self):
        """Test if credentials are properly configured"""
        test = {
            'name': 'Credentials Configuration',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        env_file = self.project_root / ".env"
        if env_file.exists():
            test['details'].append("✓ .env file exists")

            # Check if it has required keys
            with open(env_file, 'r') as f:
                content = f.read()
                if 'GMAIL_EMAIL' in content:
                    test['details'].append("✓ GMAIL_EMAIL configured")
                if 'GMAIL_PASSWORD' in content:
                    test['details'].append("✓ GMAIL_PASSWORD configured")
                if 'LINKEDIN_EMAIL' in content:
                    test['details'].append("✓ LINKEDIN_EMAIL configured")
                if 'LINKEDIN_PASSWORD' in content:
                    test['details'].append("✓ LINKEDIN_PASSWORD configured")

            test['status'] = 'PASS'
        else:
            test['details'].append("✗ .env file missing")
            test['status'] = 'FAIL'

        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        self.results['max_score'] += 1

    def test_agent_skills(self):
        """Test if Agent Skills are implemented"""
        test = {
            'name': 'Agent Skills',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        skills_dir = self.project_root / ".claude" / "skills"
        if skills_dir.exists():
            skills = list(skills_dir.glob("*.md"))
            test['details'].append(f"✓ Skills directory exists")
            test['details'].append(f"Found {len(skills)} skill(s)")

            for skill in skills:
                test['details'].append(f"  - {skill.name}")

            test['status'] = 'PASS' if len(skills) > 0 else 'FAIL'
        else:
            test['details'].append("✗ No .claude/skills directory found")
            test['status'] = 'FAIL'

        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        self.results['max_score'] += 1

    def test_mcp_servers(self):
        """Test if MCP servers are configured"""
        test = {
            'name': 'MCP Servers',
            'required': False,  # Not required for Bronze
            'status': 'FAIL',
            'details': []
        }

        mcp_config_paths = [
            Path.home() / ".config" / "claude-code" / "mcp.json",
            self.project_root / "mcp.json"
        ]

        for mcp_path in mcp_config_paths:
            if mcp_path.exists():
                test['details'].append(f"✓ MCP config found: {mcp_path}")
                test['status'] = 'PASS'
                break

        if test['status'] == 'FAIL':
            test['details'].append("✗ No MCP configuration found (Silver Tier requirement)")

        self.results['tests'].append(test)
        # Don't add to score for Bronze tier

    def test_documentation(self):
        """Test if documentation exists"""
        test = {
            'name': 'Documentation',
            'required': True,
            'status': 'FAIL',
            'details': []
        }

        doc_files = [
            'README.md',
            'SETUP.md',
            'QUICK_START.md',
            'AGENTIC_AI_WATCHERS_GUIDE.md'
        ]

        found_docs = []
        for doc in doc_files:
            doc_path = self.project_root / doc
            if not doc_path.exists():
                doc_path = self.project_root / "Platinum_Tier" / doc

            if doc_path.exists():
                found_docs.append(doc)
                test['details'].append(f"✓ {doc} exists")

        test['status'] = 'PASS' if len(found_docs) >= 1 else 'FAIL'
        test['details'].append(f"Found {len(found_docs)} documentation file(s)")

        self.results['tests'].append(test)
        if test['status'] == 'PASS':
            self.results['score'] += 1
        self.results['max_score'] += 1

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("=" * 70)
        print("HACKATHON ALIGNMENT TEST - BRONZE TIER")
        print("=" * 70)
        print()

        self.test_obsidian_vault()
        self.test_folder_structure()
        self.test_watchers()
        self.test_credentials()
        self.test_agent_skills()
        self.test_mcp_servers()
        self.test_documentation()

        # Generate report
        print("\n" + "=" * 70)
        print("TEST RESULTS")
        print("=" * 70)

        for test in self.results['tests']:
            status_symbol = "[PASS]" if test['status'] == 'PASS' else "[PARTIAL]" if test['status'] == 'PARTIAL' else "[FAIL]"
            required = "[REQUIRED]" if test['required'] else "[OPTIONAL]"
            print(f"\n{status_symbol} {test['name']} {required}")
            for detail in test['details']:
                print(f"  {detail}")

        # Calculate percentage
        percentage = (self.results['score'] / self.results['max_score'] * 100) if self.results['max_score'] > 0 else 0

        print("\n" + "=" * 70)
        print(f"BRONZE TIER COMPLETION: {percentage:.1f}%")
        print(f"Score: {self.results['score']}/{self.results['max_score']}")
        print("=" * 70)

        # Recommendations
        print("\nRECOMMENDATIONS:")
        if percentage < 50:
            print("- Create Obsidian vault with Dashboard.md and Company_Handbook.md")
            print("- Set up proper folder structure (/Needs_Action, /Done, /Plans)")
            print("- Convert watcher functionality to Agent Skills")
            print("- Integrate Claude Code with your vault")
        elif percentage < 80:
            print("- Complete missing Bronze Tier requirements")
            print("- Test Claude Code integration with vault")
            print("- Create at least one Agent Skill")
        else:
            print("- You're close to Bronze Tier completion!")
            print("- Focus on remaining gaps")
            print("- Consider moving to Silver Tier requirements")

        # Save results
        results_file = self.project_root / "hackathon_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nResults saved to: {results_file}")

        return self.results

if __name__ == "__main__":
    import sys

    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    tester = HackathonAlignmentTest(project_root)
    results = tester.run_all_tests()

    # Exit code based on completion percentage
    percentage = (results['score'] / results['max_score'] * 100) if results['max_score'] > 0 else 0
    sys.exit(0 if percentage >= 80 else 1)
