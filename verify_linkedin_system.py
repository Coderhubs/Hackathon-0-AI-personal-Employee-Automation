"""
Verify LinkedIn Automation System Installation
"""
import sys

print("="*70)
print("LinkedIn Automation System - Installation Check")
print("="*70)
print()

# Check Python version
print(f"Python Version: {sys.version.split()[0]}")

# Check dependencies
dependencies = {
    'playwright': 'Playwright (browser automation)',
    'schedule': 'Schedule (task scheduling)',
    'PIL': 'Pillow (image generation)',
    'dotenv': 'python-dotenv (environment variables)',
    'pathlib': 'pathlib (file operations)',
    'asyncio': 'asyncio (async operations)'
}

missing = []
installed = []

for module, description in dependencies.items():
    try:
        __import__(module)
        installed.append(f"[OK] {description}")
    except ImportError:
        missing.append(f"[MISSING] {description}")

print("\nInstalled Dependencies:")
for item in installed:
    print(f"  {item}")

if missing:
    print("\nMissing Dependencies:")
    for item in missing:
        print(f"  {item}")
    print("\nInstall missing dependencies:")
    print("  pip install playwright schedule Pillow python-dotenv")
else:
    print("\n[SUCCESS] All dependencies installed!")

print()
print("="*70)
print("System Status: READY" if not missing else "System Status: INCOMPLETE")
print("="*70)
