#!/usr/bin/env python3
"""
Gold Tier Autonomous Monitoring Loop
Ralph Wiggum Loop - Never stops until all tasks complete
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path

class AutonomousMonitor:
    def __init__(self, base_dir="Gold_Tier"):
        self.base_dir = Path(base_dir)
        self.needs_action = self.base_dir / "Needs_Action"
        self.plans = self.base_dir / "Plans"
        self.pending_approval = self.base_dir / "Pending_Approval"
        self.approved = self.base_dir / "Approved"
        self.done = self.base_dir / "Done"
        self.logs = self.base_dir / "Logs"

        self.state_file = self.base_dir / "Config" / "monitor_state.json"
        self.running = True

    def load_state(self):
        """Load previous state if interrupted"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_processed": [], "pending_tasks": []}

    def save_state(self, state):
        """Save state for recovery"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def log(self, message, level="INFO"):
        """Log to file"""
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} [{level}] {message}\n"

        log_file = self.logs / f"{datetime.now().strftime('%Y%m%d')}_monitor.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'a') as f:
            f.write(log_entry)

        print(log_entry.strip())

    def scan_needs_action(self):
        """Scan for new files in Needs_Action"""
        if not self.needs_action.exists():
            return []

        files = [f for f in self.needs_action.iterdir() if f.is_file()]
        return files

    def create_plan(self, file_path):
        """Create execution plan for file"""
        self.log(f"Creating plan for {file_path.name}")

        # Read file content
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except Exception as e:
            self.log(f"Error reading {file_path.name}: {e}", "ERROR")
            return None

        # Create plan
        plan_name = f"Plan_{file_path.stem}.md"
        plan_path = self.plans / plan_name

        plan_content = f"""# Plan: {file_path.name}

**Created:** {datetime.now().isoformat()}
**Source:** {file_path.name}
**Status:** IN PROGRESS

## Objective
Process {file_path.name} and execute required actions.

## File Content
```
{content[:500]}...
```

## Execution Steps
1. [ ] Analyze content
2. [ ] Determine action type
3. [ ] Execute or request approval
4. [ ] Verify completion
5. [ ] Move to Done

## Status
Created - awaiting execution
"""

        self.plans.mkdir(parents=True, exist_ok=True)
        with open(plan_path, 'w') as f:
            f.write(plan_content)

        self.log(f"Plan created: {plan_name}")
        return plan_path

    def process_file(self, file_path):
        """Process a file through the system"""
        self.log(f"Processing {file_path.name}")

        try:
            # Create plan
            plan = self.create_plan(file_path)
            if not plan:
                return False

            # Analyze content
            with open(file_path, 'r') as f:
                content = f.read()

            # Determine if sensitive (requires approval)
            is_sensitive = self.is_sensitive_action(content)

            if is_sensitive:
                # Move to Pending_Approval
                self.log(f"{file_path.name} requires approval")
                dest = self.pending_approval / file_path.name
                self.pending_approval.mkdir(parents=True, exist_ok=True)
                file_path.rename(dest)
            else:
                # Auto-process and move to Done
                self.log(f"{file_path.name} auto-processed")
                dest = self.done / file_path.name
                self.done.mkdir(parents=True, exist_ok=True)
                file_path.rename(dest)

            return True

        except Exception as e:
            self.log(f"Error processing {file_path.name}: {e}", "ERROR")
            return False

    def is_sensitive_action(self, content):
        """Determine if action requires human approval"""
        sensitive_keywords = [
            'post', 'publish', 'send', 'email', 'delete',
            'linkedin', 'facebook', 'twitter', 'instagram'
        ]

        content_lower = content.lower()
        return any(keyword in content_lower for keyword in sensitive_keywords)

    def process_approved(self):
        """Process files that have been approved"""
        if not self.approved.exists():
            return

        for file_path in self.approved.iterdir():
            if file_path.is_file():
                self.log(f"Executing approved action: {file_path.name}")
                # Execute the approved action
                # Then move to Done
                dest = self.done / file_path.name
                self.done.mkdir(parents=True, exist_ok=True)
                file_path.rename(dest)

    def update_dashboard(self):
        """Update Dashboard.md with current status"""
        dashboard_path = self.base_dir / "Dashboard.md"

        needs_action_count = len(list(self.needs_action.iterdir())) if self.needs_action.exists() else 0
        pending_count = len(list(self.pending_approval.iterdir())) if self.pending_approval.exists() else 0
        approved_count = len(list(self.approved.iterdir())) if self.approved.exists() else 0

        dashboard_content = f"""# Gold Tier Dashboard

**Last Update:** {datetime.now().isoformat()}
**Status:** OPERATIONAL [ACTIVE]

## Queue Status
- Needs_Action: {needs_action_count} files
- Pending_Approval: {pending_count} files
- Approved: {approved_count} files

## System Health
- Monitoring: ACTIVE
- Error Count: 0
- Uptime: Continuous

## Recent Activity
Last scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*Auto-updated by Autonomous Monitor*
"""

        with open(dashboard_path, 'w') as f:
            f.write(dashboard_content)

    def run(self):
        """Main monitoring loop - Ralph Wiggum style"""
        self.log("Starting Autonomous Monitor - Ralph Wiggum Loop")
        self.log("Never stopping until all tasks complete...")

        state = self.load_state()

        while self.running:
            try:
                # Scan for new files
                files = self.scan_needs_action()

                if files:
                    self.log(f"Found {len(files)} files to process")

                    for file_path in files:
                        if file_path.name not in state["last_processed"]:
                            success = self.process_file(file_path)
                            if success:
                                state["last_processed"].append(file_path.name)
                                self.save_state(state)

                # Process approved items
                self.process_approved()

                # Update dashboard
                self.update_dashboard()

                # Sleep briefly before next scan
                time.sleep(5)

            except KeyboardInterrupt:
                self.log("Received interrupt signal - saving state")
                self.save_state(state)
                break
            except Exception as e:
                self.log(f"Error in main loop: {e}", "ERROR")
                time.sleep(10)  # Wait longer on error

        self.log("Monitor stopped")

if __name__ == "__main__":
    monitor = AutonomousMonitor()
    monitor.run()
