"""
Master Orchestrator - Runs all watchers and Claude Code automation
Hackathon Compliant Implementation
"""
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime
import logging
import signal
import sys

class Orchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.processes = {}
        self.running = True
        self.logger = self.setup_logging()

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def setup_logging(self):
        """Setup logging"""
        log_dir = Path("Gold_Tier/Logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('Orchestrator')

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Shutdown signal received")
        self.running = False
        self.stop_all_watchers()
        sys.exit(0)

    def start_watcher(self, name: str, script_path: str):
        """Start a watcher process"""
        try:
            self.logger.info(f"Starting {name}...")
            process = subprocess.Popen(
                ['python', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes[name] = process
            self.logger.info(f"{name} started with PID {process.pid}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start {name}: {e}")
            return False

    def check_process_health(self, name: str):
        """Check if a process is still running"""
        if name not in self.processes:
            return False

        process = self.processes[name]
        return process.poll() is None

    def restart_process(self, name: str, script_path: str):
        """Restart a failed process"""
        self.logger.warning(f"{name} has stopped, restarting...")
        if name in self.processes:
            try:
                self.processes[name].terminate()
                self.processes[name].wait(timeout=5)
            except:
                pass
            del self.processes[name]

        return self.start_watcher(name, script_path)

    def stop_all_watchers(self):
        """Stop all watcher processes"""
        self.logger.info("Stopping all watchers...")
        for name, process in self.processes.items():
            try:
                self.logger.info(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.logger.warning(f"{name} did not stop gracefully, killing...")
                process.kill()
            except Exception as e:
                self.logger.error(f"Error stopping {name}: {e}")

        self.processes.clear()
        self.logger.info("All watchers stopped")

    def run(self):
        """Main orchestrator loop"""
        self.logger.info("=" * 70)
        self.logger.info("AI Employee Orchestrator - Hackathon Edition")
        self.logger.info("=" * 70)
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Starting all watchers...")
        self.logger.info("=" * 70)

        # Define watchers
        watchers = {
            'Gmail Watcher': 'Platinum_Tier/gmail_watcher_hackathon.py',
            'LinkedIn Watcher': 'Platinum_Tier/linkedin_watcher_hackathon.py',
            'WhatsApp Watcher': 'Platinum_Tier/whatsapp_watcher_hackathon.py'
        }

        # Start all watchers
        for name, script in watchers.items():
            if Path(script).exists():
                self.start_watcher(name, script)
            else:
                self.logger.warning(f"Script not found: {script}")

        self.logger.info("")
        self.logger.info("All watchers started!")
        self.logger.info("Monitoring health and processing items...")
        self.logger.info("Press Ctrl+C to stop")
        self.logger.info("")

        # Main monitoring loop
        health_check_interval = 60  # Check every minute
        last_health_check = time.time()

        while self.running:
            try:
                # Health check
                if time.time() - last_health_check >= health_check_interval:
                    self.logger.info("Performing health check...")

                    for name, script in watchers.items():
                        if not self.check_process_health(name):
                            self.logger.warning(f"{name} is not running!")
                            self.restart_process(name, script)

                    last_health_check = time.time()
                    self.logger.info("Health check complete - all systems OK")

                # Sleep for a bit
                time.sleep(10)

            except KeyboardInterrupt:
                self.logger.info("Orchestrator stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in orchestrator loop: {e}")
                time.sleep(5)

        # Cleanup
        self.stop_all_watchers()
        self.logger.info("Orchestrator shutdown complete")

def main():
    """Main entry point"""
    # Vault path
    vault_path = Path(__file__).parent / "AI_Employee_Vault"

    if not vault_path.exists():
        print(f"ERROR: Vault not found at {vault_path}")
        print("Please create the vault first")
        return

    orchestrator = Orchestrator(str(vault_path))
    orchestrator.run()

if __name__ == "__main__":
    main()
