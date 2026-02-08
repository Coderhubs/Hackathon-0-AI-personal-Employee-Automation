#!/usr/bin/env python3
"""
Platinum Tier - System Test Suite
Validates all components before deployment
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import json

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class PlatinumTester:
    """Test suite for Platinum Tier system"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results: List[Tuple[str, bool, str]] = []

    def log_test(self, name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = f"{Colors.GREEN}[PASS]{Colors.RESET}" if passed else f"{Colors.RED}[FAIL]{Colors.RESET}"
        print(f"{status} {name}")
        if message:
            print(f"      {message}")
        self.results.append((name, passed, message))

    def test_directory_structure(self) -> bool:
        """Test that all required directories exist"""
        print(f"\n{Colors.BLUE}=== Testing Directory Structure ==={Colors.RESET}")

        required_dirs = [
            "Inbox", "Needs_Action", "Plans", "Pending_Approval",
            "Approved", "Rejected", "Done", "Logs", "Briefings",
            "Config", "Docker", "Agents", "Voice", "Memory", "Security"
        ]

        all_passed = True
        for dir_name in required_dirs:
            dir_path = self.base_dir / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            self.log_test(f"Directory: {dir_name}", exists)
            if not exists:
                all_passed = False

        return all_passed

    def test_core_files(self) -> bool:
        """Test that all core files exist"""
        print(f"\n{Colors.BLUE}=== Testing Core Files ==={Colors.RESET}")

        required_files = [
            "api_server.py",
            "requirements.txt",
            "README.md",
            "CLOUD_MIGRATION_GUIDE.md",
            ".env.example",
            "deploy.sh",
            "Docker/Dockerfile",
            "Docker/docker-compose.yml",
            "Docker/pm2.config.js",
            "Agents/manager_agent.py",
            "Agents/email_agent.py",
            "Agents/social_media_agent.py",
            "Agents/accounting_agent.py",
            "Voice/vapi_integration.py",
            "Memory/vector_store.py",
            "Security/secrets_manager.py"
        ]

        all_passed = True
        for file_path in required_files:
            full_path = self.base_dir / file_path
            exists = full_path.exists() and full_path.is_file()
            self.log_test(f"File: {file_path}", exists)
            if not exists:
                all_passed = False

        return all_passed

    def test_python_syntax(self) -> bool:
        """Test Python files for syntax errors"""
        print(f"\n{Colors.BLUE}=== Testing Python Syntax ==={Colors.RESET}")

        python_files = [
            "api_server.py",
            "Agents/manager_agent.py",
            "Agents/email_agent.py",
            "Agents/social_media_agent.py",
            "Agents/accounting_agent.py",
            "Voice/vapi_integration.py",
            "Memory/vector_store.py",
            "Security/secrets_manager.py"
        ]

        all_passed = True
        for file_path in python_files:
            full_path = self.base_dir / file_path
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
                self.log_test(f"Syntax: {file_path}", True)
            except SyntaxError as e:
                self.log_test(f"Syntax: {file_path}", False, str(e))
                all_passed = False

        return all_passed

    def test_docker_files(self) -> bool:
        """Test Docker configuration files"""
        print(f"\n{Colors.BLUE}=== Testing Docker Configuration ==={Colors.RESET}")

        # Test Dockerfile
        dockerfile = self.base_dir / "Docker" / "Dockerfile"
        if dockerfile.exists():
            content = dockerfile.read_text()
            has_from = "FROM" in content
            has_cmd = "CMD" in content
            self.log_test("Dockerfile: Valid structure", has_from and has_cmd)
        else:
            self.log_test("Dockerfile: Exists", False)
            return False

        # Test docker-compose.yml
        compose_file = self.base_dir / "Docker" / "docker-compose.yml"
        if compose_file.exists():
            content = compose_file.read_text()
            has_version = "version:" in content
            has_services = "services:" in content
            self.log_test("docker-compose.yml: Valid structure", has_version and has_services)
        else:
            self.log_test("docker-compose.yml: Exists", False)
            return False

        # Test PM2 config
        pm2_config = self.base_dir / "Docker" / "pm2.config.js"
        if pm2_config.exists():
            content = pm2_config.read_text()
            has_apps = "apps:" in content or "apps :" in content
            self.log_test("pm2.config.js: Valid structure", has_apps)
        else:
            self.log_test("pm2.config.js: Exists", False)
            return False

        return True

    def test_requirements(self) -> bool:
        """Test requirements.txt"""
        print(f"\n{Colors.BLUE}=== Testing Requirements ==={Colors.RESET}")

        req_file = self.base_dir / "requirements.txt"
        if not req_file.exists():
            self.log_test("requirements.txt: Exists", False)
            return False

        content = req_file.read_text()

        # Check for essential packages
        essential_packages = [
            "fastapi",
            "uvicorn",
            "redis",
            "psycopg2",
            "cryptography",
            "aiohttp"
        ]

        all_found = True
        for package in essential_packages:
            found = package in content.lower()
            self.log_test(f"Package: {package}", found)
            if not found:
                all_found = False

        return all_found

    def test_env_example(self) -> bool:
        """Test .env.example file"""
        print(f"\n{Colors.BLUE}=== Testing Environment Configuration ==={Colors.RESET}")

        env_file = self.base_dir / ".env.example"
        if not env_file.exists():
            self.log_test(".env.example: Exists", False)
            return False

        content = env_file.read_text()

        # Check for essential variables
        essential_vars = [
            "VAPI_API_KEY",
            "ENCRYPTION_KEY",
            "POSTGRES_PASSWORD",
            "ANTHROPIC_API_KEY",
            "VECTOR_DB_PROVIDER"
        ]

        all_found = True
        for var in essential_vars:
            found = var in content
            self.log_test(f"Variable: {var}", found)
            if not found:
                all_found = False

        return all_found

    async def test_agent_imports(self) -> bool:
        """Test that agent modules can be imported"""
        print(f"\n{Colors.BLUE}=== Testing Agent Imports ==={Colors.RESET}")

        # Add parent directory to path
        sys.path.insert(0, str(self.base_dir))

        agents = [
            ("Agents.manager_agent", "ManagerAgent"),
            ("Agents.email_agent", "EmailAgent"),
            ("Agents.social_media_agent", "SocialMediaAgent"),
            ("Agents.accounting_agent", "AccountingAgent")
        ]

        all_passed = True
        for module_name, class_name in agents:
            try:
                module = __import__(module_name, fromlist=[class_name])
                agent_class = getattr(module, class_name)
                self.log_test(f"Import: {class_name}", True)
            except Exception as e:
                self.log_test(f"Import: {class_name}", False, str(e))
                all_passed = False

        return all_passed

    def test_documentation(self) -> bool:
        """Test documentation completeness"""
        print(f"\n{Colors.BLUE}=== Testing Documentation ==={Colors.RESET}")

        # Test README
        readme = self.base_dir / "README.md"
        if readme.exists():
            content = readme.read_text(encoding='utf-8')
            content_lower = content.lower()
            has_title = "platinum" in content_lower
            has_features = "features" in content_lower
            self.log_test("README.md: Complete", has_title and has_features)
        else:
            self.log_test("README.md: Exists", False)
            return False

        # Test Migration Guide
        guide = self.base_dir / "CLOUD_MIGRATION_GUIDE.md"
        if guide.exists():
            content = guide.read_text(encoding='utf-8')
            has_phases = "Phase" in content
            has_docker = "Docker" in content or "docker" in content
            self.log_test("CLOUD_MIGRATION_GUIDE.md: Complete", has_phases and has_docker)
        else:
            self.log_test("CLOUD_MIGRATION_GUIDE.md: Exists", False)
            return False

        return True

    def generate_report(self):
        """Generate final test report"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}=== FINAL TEST REPORT ==={Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

        total_tests = len(self.results)
        passed_tests = sum(1 for _, passed, _ in self.results if passed)
        failed_tests = total_tests - passed_tests

        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests:  {total_tests}")
        print(f"{Colors.GREEN}Passed:       {passed_tests}{Colors.RESET}")
        print(f"{Colors.RED}Failed:       {failed_tests}{Colors.RESET}")
        print(f"Pass Rate:    {pass_rate:.1f}%\n")

        if failed_tests > 0:
            print(f"{Colors.RED}Failed Tests:{Colors.RESET}")
            for name, passed, message in self.results:
                if not passed:
                    print(f"  - {name}")
                    if message:
                        print(f"    {message}")

        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}\n")

        if pass_rate == 100:
            print(f"{Colors.GREEN}[OK] All tests passed! System is ready for deployment.{Colors.RESET}\n")
            return 0
        elif pass_rate >= 80:
            print(f"{Colors.YELLOW}[WARN] Most tests passed. Review failures before deployment.{Colors.RESET}\n")
            return 1
        else:
            print(f"{Colors.RED}[ERROR] Multiple test failures. System needs fixes before deployment.{Colors.RESET}\n")
            return 2

    async def run_all_tests(self):
        """Run all test suites"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}PLATINUM TIER - SYSTEM TEST SUITE{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")

        # Run all tests
        self.test_directory_structure()
        self.test_core_files()
        self.test_python_syntax()
        self.test_docker_files()
        self.test_requirements()
        self.test_env_example()
        await self.test_agent_imports()
        self.test_documentation()

        # Generate report
        return self.generate_report()

async def main():
    """Main entry point"""
    tester = PlatinumTester()
    exit_code = await tester.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    asyncio.run(main())
