"""
System Orchestrator - Master Process for AI Personal Employee
Coordinates all components: Watchers, Integration, Approval Handler
"""
import subprocess
import time
import logging
import sys
from pathlib import Path
from datetime import datetime
import signal
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('SystemOrchestrator')


class SystemOrchestrator:
    """Orchestrates all AI Personal Employee components"""

    def __init__(self):
        self.processes = {}
        self.running = False
        self.base_dir = Path(__file__).parent

    def start_process(self, name: str, command: list, cwd: str = None) -> subprocess.Popen:
        """Start a subprocess and track it"""
        try:
            logger.info(f"Starting {name}...")

            # Use current directory if not specified
            if cwd is None:
                cwd = str(self.base_dir)

            # Start process
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            self.processes[name] = {
                'process': process,
                'command': command,
                'cwd': cwd,
                'started': datetime.now(),
                'restarts': 0
            }

            logger.info(f"✓ {name} started (PID: {process.pid})")
            return process

        except Exception as e:
            logger.error(f"✗ Failed to start {name}: {e}")
            return None

    def check_process(self, name: str) -> bool:
        """Check if a process is still running"""
        if name not in self.processes:
            return False

        process = self.processes[name]['process']
        return process.poll() is None

    def restart_process(self, name: str):
        """Restart a failed process"""
        if name not in self.processes:
            logger.error(f"Cannot restart {name}: not found")
            return

        info = self.processes[name]
        info['restarts'] += 1

        logger.warning(f"Restarting {name} (attempt {info['restarts']})...")

        # Kill old process if still running
        try:
            info['process'].kill()
        except:
            pass

        # Start new process
        self.start_process(name, info['command'], info['cwd'])

    def monitor_processes(self):
        """Monitor all processes and restart if needed"""
        while self.running:
            for name in list(self.processes.keys()):
                if not self.check_process(name):
                    logger.warning(f"⚠ {name} stopped unexpectedly")

                    # Check restart limit
                    if self.processes[name]['restarts'] < 5:
                        self.restart_process(name)
                    else:
                        logger.error(f"✗ {name} failed too many times, giving up")

            time.sleep(10)  # Check every 10 seconds

    def start_all(self):
        """Start all AI Personal Employee components"""
        logger.info("=" * 70)
        logger.info("AI PERSONAL EMPLOYEE - SYSTEM ORCHESTRATOR")
        logger.info("=" * 70)
        logger.info("")

        self.running = True

        # Component 1: Gmail Watcher
        self.start_process(
            "Gmail Watcher",
            [sys.executable, "gmail_watcher_playwright.py"],
            cwd=str(self.base_dir / "Platinum_Tier")
        )
        time.sleep(2)

        # Component 2: LinkedIn Watcher
        self.start_process(
            "LinkedIn Watcher",
            [sys.executable, "linkedin_watcher_playwright.py"],
            cwd=str(self.base_dir / "Platinum_Tier")
        )
        time.sleep(2)

        # Component 3: WhatsApp Watcher
        self.start_process(
            "WhatsApp Watcher",
            [sys.executable, "whatsapp_watcher_hackathon.py"],
            cwd=str(self.base_dir / "Platinum_Tier")
        )
        time.sleep(2)

        # Component 4: Integration Coordinator
        if (self.base_dir / "integration_coordinator.py").exists():
            self.start_process(
                "Integration Coordinator",
                [sys.executable, "integration_coordinator.py"],
                cwd=str(self.base_dir)
            )
            time.sleep(2)

        # Component 5: Approval Handler
        self.start_process(
            "Approval Handler",
            [sys.executable, "approval_handler.py"],
            cwd=str(self.base_dir)
        )
        time.sleep(2)

        # Component 6: LinkedIn Content Generator (weekly)
        # This runs once to generate initial posts
        if (self.base_dir / "Platinum_Tier" / "linkedin_content_generator.py").exists():
            logger.info("Generating initial LinkedIn posts...")
            try:
                subprocess.run(
                    [sys.executable, "linkedin_content_generator.py"],
                    cwd=str(self.base_dir / "Platinum_Tier"),
                    timeout=30
                )
                logger.info("✓ Initial LinkedIn posts generated")
            except Exception as e:
                logger.error(f"✗ Failed to generate LinkedIn posts: {e}")

        logger.info("")
        logger.info("=" * 70)
        logger.info("SYSTEM STATUS")
        logger.info("=" * 70)
        logger.info("")
        logger.info(f"Active Components: {len(self.processes)}")
        for name, info in self.processes.items():
            status = "RUNNING" if self.check_process(name) else "STOPPED"
            logger.info(f"  • {name}: {status} (PID: {info['process'].pid})")

        logger.info("")
        logger.info("System is now running. Press Ctrl+C to stop all components.")
        logger.info("")

        # Start monitoring
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            logger.info("\nShutdown signal received...")
            self.stop_all()

    def stop_all(self):
        """Stop all components gracefully"""
        logger.info("Stopping all components...")
        self.running = False

        for name, info in self.processes.items():
            try:
                logger.info(f"Stopping {name}...")
                info['process'].terminate()
                info['process'].wait(timeout=5)
                logger.info(f"✓ {name} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}...")
                info['process'].kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")

        logger.info("All components stopped")

    def status(self):
        """Show status of all components"""
        print("\n" + "=" * 70)
        print("SYSTEM STATUS")
        print("=" * 70)
        print()

        if not self.processes:
            print("No components running")
            return

        for name, info in self.processes.items():
            running = self.check_process(name)
            status = "✓ RUNNING" if running else "✗ STOPPED"
            uptime = datetime.now() - info['started']

            print(f"{name}:")
            print(f"  Status: {status}")
            print(f"  PID: {info['process'].pid}")
            print(f"  Uptime: {uptime}")
            print(f"  Restarts: {info['restarts']}")
            print()


def main():
    """Main entry point"""
    orchestrator = SystemOrchestrator()

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        logger.info("\nShutdown signal received...")
        orchestrator.stop_all()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Start all components
    orchestrator.start_all()


if __name__ == "__main__":
    main()
