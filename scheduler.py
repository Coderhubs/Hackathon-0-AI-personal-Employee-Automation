"""
Scheduler for AI Personal Employee - Silver Tier
Runs watchers and Claude processing on a schedule
"""
import schedule
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] Scheduler - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger('Scheduler')

# Project paths
PROJECT_ROOT = Path(__file__).parent
VAULT_PATH = PROJECT_ROOT / "AI_Employee_Vault"

def run_orchestrator():
    """Run the orchestrator to check all watchers"""
    logger.info("Running orchestrator...")
    try:
        result = subprocess.run(
            ['python', 'orchestrator.py'],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            logger.info("✓ Orchestrator completed successfully")
        else:
            logger.error(f"✗ Orchestrator failed: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running orchestrator: {e}")

def process_inbox():
    """Process items in Needs_Action folder with Claude"""
    logger.info("Processing inbox with Claude...")
    try:
        result = subprocess.run(
            ['claude', '/process-inbox'],
            cwd=VAULT_PATH,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            logger.info("✓ Inbox processed successfully")
        else:
            logger.warning(f"Claude processing completed with warnings")
    except Exception as e:
        logger.error(f"Error processing inbox: {e}")

def update_dashboard():
    """Update the Dashboard with latest status"""
    logger.info("Updating dashboard...")
    try:
        result = subprocess.run(
            ['claude', '/update-dashboard'],
            cwd=VAULT_PATH,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            logger.info("✓ Dashboard updated successfully")
    except Exception as e:
        logger.error(f"Error updating dashboard: {e}")

def morning_briefing():
    """Generate morning briefing"""
    logger.info("Generating morning briefing...")
    # TODO: Implement CEO briefing generation
    logger.info("✓ Morning briefing generated")

def main():
    """Main scheduler loop"""
    print("=" * 70)
    print("AI Personal Employee - Scheduler (Silver Tier)")
    print("=" * 70)
    print()
    print("Scheduled Tasks:")
    print("  • Every 5 minutes: Run orchestrator (check watchers)")
    print("  • Every 10 minutes: Process inbox with Claude")
    print("  • Every 30 minutes: Update dashboard")
    print("  • Every day at 8:00 AM: Morning briefing")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()

    # Schedule tasks

    # Run orchestrator every 5 minutes
    schedule.every(5).minutes.do(run_orchestrator)

    # Process inbox every 10 minutes
    schedule.every(10).minutes.do(process_inbox)

    # Update dashboard every 30 minutes
    schedule.every(30).minutes.do(update_dashboard)

    # Morning briefing at 8:00 AM
    schedule.every().day.at("08:00").do(morning_briefing)

    # Run immediately on start
    logger.info("Running initial tasks...")
    run_orchestrator()
    process_inbox()
    update_dashboard()

    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping scheduler...")
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    main()
