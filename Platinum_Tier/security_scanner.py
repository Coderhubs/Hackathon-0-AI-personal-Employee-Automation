#!/usr/bin/env python3
"""
Security Scanner - Scans files for secrets before syncing
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityScanner:
    """
    Scans files for secrets and sensitive information.

    Prevents accidental exposure of:
    - API keys
    - Passwords
    - Email addresses
    - Phone numbers
    - Credit card numbers
    """

    def __init__(self):
        # Regex patterns for secret detection
        self.patterns = {
            'api_key': [
                r'api[_-]?key["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})',
                r'apikey["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{20,})',
                r'["\']([A-Z0-9]{20,})["\']',  # Generic long uppercase strings
            ],
            'password': [
                r'password["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
                r'passwd["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
                r'pwd["\']?\s*[:=]\s*["\']([^"\']{8,})["\']',
            ],
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            'phone': [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\+\d{1,3}[-.]?\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            ],
            'credit_card': [
                r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            ],
            'private_key': [
                r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
                r'-----BEGIN OPENSSH PRIVATE KEY-----',
            ],
            'aws_key': [
                r'AKIA[0-9A-Z]{16}',
            ],
            'github_token': [
                r'ghp_[a-zA-Z0-9]{36}',
                r'gho_[a-zA-Z0-9]{36}',
            ],
        }

        # Whitelist patterns (known safe values)
        self.whitelist = [
            'example@example.com',
            'user@example.com',
            'admin@example.com',
            '123-456-7890',
            'YOUR_API_KEY_HERE',
            'your_password_here',
        ]

    def scan_file(self, file_path: Path) -> Tuple[bool, List[Dict]]:
        """
        Scan a file for secrets.

        Args:
            file_path: Path to file to scan

        Returns:
            Tuple of (is_safe, findings)
            - is_safe: True if no secrets found, False otherwise
            - findings: List of detected secrets with details
        """
        findings = []

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return True, [{'error': f'Could not read file: {e}'}]

        # Scan for each pattern type
        for secret_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)

                for match in matches:
                    matched_text = match.group(0)

                    # Skip whitelisted values
                    if any(wl in matched_text for wl in self.whitelist):
                        continue

                    findings.append({
                        'type': secret_type,
                        'match': matched_text[:50] + '...' if len(matched_text) > 50 else matched_text,
                        'line': content[:match.start()].count('\n') + 1,
                        'file': str(file_path)
                    })

        is_safe = len(findings) == 0
        return is_safe, findings

    def scan_directory(self, dir_path: Path, extensions: List[str] = None) -> Dict:
        """
        Scan all files in a directory.

        Args:
            dir_path: Directory to scan
            extensions: List of file extensions to scan (e.g., ['.py', '.md'])

        Returns:
            Dictionary with scan results
        """
        if extensions is None:
            extensions = ['.py', '.md', '.txt', '.json', '.yml', '.yaml', '.env']

        results = {
            'total_files': 0,
            'safe_files': 0,
            'unsafe_files': 0,
            'findings': []
        }

        for file_path in dir_path.rglob('*'):
            if not file_path.is_file():
                continue

            if file_path.suffix not in extensions:
                continue

            results['total_files'] += 1

            is_safe, findings = self.scan_file(file_path)

            if is_safe:
                results['safe_files'] += 1
            else:
                results['unsafe_files'] += 1
                results['findings'].extend(findings)

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate a human-readable report"""
        report = f"""# Security Scan Report

**Total Files Scanned:** {results['total_files']}
**Safe Files:** {results['safe_files']}
**Files with Secrets:** {results['unsafe_files']}

"""

        if results['unsafe_files'] > 0:
            report += "## ⚠️ Secrets Detected\n\n"

            for finding in results['findings']:
                report += f"### {finding['type'].upper()}\n"
                report += f"- **File:** {finding['file']}\n"
                report += f"- **Line:** {finding['line']}\n"
                report += f"- **Match:** `{finding['match']}`\n\n"

            report += "\n**Action Required:** Remove or encrypt these secrets before syncing.\n"
        else:
            report += "## ✓ No Secrets Detected\n\nAll files are safe to sync.\n"

        return report

if __name__ == "__main__":
    # Test security scanner
    scanner = SecurityScanner()

    # Scan current directory
    results = scanner.scan_directory(Path('.'))

    print(scanner.generate_report(results))
