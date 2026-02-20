"""
Integration Test Suite - Verify Complete System
Tests all components of the AI automation system
"""
import os
import time
from pathlib import Path
from datetime import datetime
import sys

class IntegrationTester:
    def __init__(self):
        self.vault_path = Path("AI_Employee_Vault")
        self.test_results = []

    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)

    def print_test(self, name, passed, details=""):
        """Print test result"""
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {name}")
        if details:
            print(f"     {details}")
        self.test_results.append((name, passed))

    def test_vault_structure(self):
        """Test vault folder structure"""
        self.print_header("Test 1: Vault Structure")

        required_folders = [
            "Needs_Action",
            "Pending_Approval",
            "Approved",
            "Done",
            "Plans",
            "Logs",
            "Skills"
        ]

        for folder in required_folders:
            folder_path = self.vault_path / folder
            exists = folder_path.exists()
            self.print_test(
                f"Folder: {folder}",
                exists,
                f"Path: {folder_path}"
            )

    def test_configuration(self):
        """Test configuration files"""
        self.print_header("Test 2: Configuration")

        # Check .env file
        env_exists = Path(".env").exists()
        self.print_test(".env file exists", env_exists)

        if env_exists:
            from dotenv import load_dotenv
            load_dotenv()

            gmail = os.getenv('GMAIL_EMAIL')
            linkedin = os.getenv('LINKEDIN_EMAIL')

            self.print_test(
                "Gmail configured",
                gmail is not None,
                f"Email: {gmail if gmail else 'NOT SET'}"
            )

            self.print_test(
                "LinkedIn configured",
                linkedin is not None,
                f"Email: {linkedin if linkedin else 'NOT SET'}"
            )

        # Check Company Handbook
        handbook = self.vault_path / "Company_Handbook.md"
        handbook_exists = handbook.exists()
        self.print_test(
            "Company Handbook exists",
            handbook_exists,
            f"Size: {handbook.stat().st_size if handbook_exists else 0} bytes"
        )

    def test_watcher_scripts(self):
        """Test watcher scripts exist"""
        self.print_header("Test 3: Watcher Scripts")

        watchers = [
            "Platinum_Tier/gmail_watcher_hackathon.py",
            "Platinum_Tier/linkedin_watcher_hackathon.py",
            "Platinum_Tier/whatsapp_watcher_hackathon.py"
        ]

        for watcher in watchers:
            exists = Path(watcher).exists()
            self.print_test(
                f"Watcher: {Path(watcher).name}",
                exists,
                f"Path: {watcher}"
            )

    def test_integration_components(self):
        """Test integration components"""
        self.print_header("Test 4: Integration Components")

        components = [
            "integration_coordinator.py",
            "approval_handler.py",
            "linkedin_content_generator.py",
            "START_COMPLETE_SYSTEM.bat"
        ]

        for component in components:
            exists = Path(component).exists()
            self.print_test(
                f"Component: {component}",
                exists
            )

    def test_dependencies(self):
        """Test Python dependencies"""
        self.print_header("Test 5: Python Dependencies")

        dependencies = [
            ("playwright", "Playwright"),
            ("dotenv", "python-dotenv"),
            ("schedule", "schedule"),
            ("watchdog", "watchdog")
        ]

        for module, package in dependencies:
            try:
                __import__(module)
                self.print_test(f"Package: {package}", True)
            except ImportError:
                self.print_test(
                    f"Package: {package}",
                    False,
                    f"Install: pip install {package}"
                )

    def test_workflow_simulation(self):
        """Test workflow by creating test file"""
        self.print_header("Test 6: Workflow Simulation")

        # Create test file in Needs_Action
        test_file = self.vault_path / "Needs_Action" / "TEST_integration.md"

        test_content = f"""---
type: test
priority: low
created: {datetime.now().isoformat()}
---

# Integration Test

This is a test file to verify the integration workflow.

The system should:
1. Detect this file
2. Process it
3. Create a plan
4. Move to Done

Test timestamp: {datetime.now().isoformat()}
"""

        try:
            test_file.write_text(test_content, encoding='utf-8')
            self.print_test(
                "Created test file",
                True,
                f"File: {test_file.name}"
            )

            print("\n     ⏳ Waiting 5 seconds for processing...")
            time.sleep(5)

            # Check if file was processed
            still_in_needs_action = test_file.exists()
            moved_to_done = (self.vault_path / "Done" / test_file.name).exists()

            self.print_test(
                "File processed",
                moved_to_done or not still_in_needs_action,
                "File should be moved to Done or processed"
            )

            # Cleanup
            if test_file.exists():
                test_file.unlink()

        except Exception as e:
            self.print_test("Workflow simulation", False, f"Error: {e}")

    def test_mcp_servers(self):
        """Test MCP server configuration"""
        self.print_header("Test 7: MCP Servers")

        mcp_servers = [
            "mcp_servers/email-mcp/index.js",
            "Gold_Tier/mcp_servers/social_media_server.py",
            "Gold_Tier/mcp_servers/browser_server.py"
        ]

        for server in mcp_servers:
            exists = Path(server).exists()
            self.print_test(
                f"MCP Server: {Path(server).name}",
                exists,
                f"Path: {server}"
            )

    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")

        total = len(self.test_results)
        passed = sum(1 for _, result in self.test_results if result)
        failed = total - passed

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")

        if failed == 0:
            print("\n*** ALL TESTS PASSED! System is ready to use. ***")
            print("\nNext steps:")
            print("1. Run: START_COMPLETE_SYSTEM.bat")
            print("2. Check: AI_Employee_Vault/Pending_Approval/")
            print("3. Review and approve actions")
        else:
            print("\n*** WARNING: Some tests failed. Please fix issues before proceeding. ***")
            print("\nFailed tests:")
            for name, result in self.test_results:
                if not result:
                    print(f"  - {name}")

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 70)
        print("  AI PERSONAL EMPLOYEE - INTEGRATION TEST SUITE")
        print("=" * 70)
        print(f"\nTest Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Vault Path: {self.vault_path.absolute()}")

        self.test_vault_structure()
        self.test_configuration()
        self.test_watcher_scripts()
        self.test_integration_components()
        self.test_dependencies()
        self.test_mcp_servers()
        self.test_workflow_simulation()

        self.print_summary()

        print("\n" + "=" * 70)
        print()

def main():
    """Main entry point"""
    tester = IntegrationTester()
    tester.run_all_tests()

    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
