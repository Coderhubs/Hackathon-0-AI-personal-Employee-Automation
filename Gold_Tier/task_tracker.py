#!/usr/bin/env python3
"""
Task Tracker for Ralph Wiggum Loop
Tracks task states and dependencies
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

class TaskTracker:
    """
    Tracks task states and dependencies for autonomous monitoring.

    Features:
    - Track task states (pending, in_progress, completed)
    - Detect when all tasks are complete
    - Generate completion reports
    """

    def __init__(self, base_dir="AI_Employee_Vault"):
        self.base_dir = Path(base_dir)
        self.state_file = Path("Gold_Tier") / "Config" / "task_tracker_state.json"
        self.tasks: Dict[str, Dict] = {}
        self.load_state()

    def load_state(self):
        """Load task tracker state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print(f"Error loading task tracker state: {e}")
                self.tasks = {}

    def save_state(self):
        """Save task tracker state"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, task_id: str, task_data: Dict):
        """Add a new task to track"""
        self.tasks[task_id] = {
            'id': task_id,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'data': task_data,
            'dependencies': []
        }
        self.save_state()

    def update_task_status(self, task_id: str, status: str):
        """Update task status"""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = status
            self.tasks[task_id]['updated'] = datetime.now().isoformat()
            self.save_state()

    def add_dependency(self, task_id: str, depends_on: str):
        """Add task dependency"""
        if task_id in self.tasks:
            if 'dependencies' not in self.tasks[task_id]:
                self.tasks[task_id]['dependencies'] = []
            self.tasks[task_id]['dependencies'].append(depends_on)
            self.save_state()

    def get_pending_tasks(self) -> List[str]:
        """Get list of pending tasks with no dependencies"""
        pending = []
        for task_id, task in self.tasks.items():
            if task['status'] == 'pending':
                # Check if all dependencies are completed
                deps = task.get('dependencies', [])
                if all(self.tasks.get(dep, {}).get('status') == 'completed' for dep in deps):
                    pending.append(task_id)
        return pending

    def get_in_progress_tasks(self) -> List[str]:
        """Get list of in-progress tasks"""
        return [tid for tid, task in self.tasks.items() if task['status'] == 'in_progress']

    def get_completed_tasks(self) -> List[str]:
        """Get list of completed tasks"""
        return [tid for tid, task in self.tasks.items() if task['status'] == 'completed']

    def all_tasks_complete(self) -> bool:
        """Check if all tasks are complete"""
        if not self.tasks:
            return True
        return all(task['status'] == 'completed' for task in self.tasks.values())

    def get_task_summary(self) -> Dict:
        """Get summary of all tasks"""
        return {
            'total': len(self.tasks),
            'pending': len([t for t in self.tasks.values() if t['status'] == 'pending']),
            'in_progress': len([t for t in self.tasks.values() if t['status'] == 'in_progress']),
            'completed': len([t for t in self.tasks.values() if t['status'] == 'completed'])
        }

    def generate_completion_report(self) -> str:
        """Generate completion report"""
        summary = self.get_task_summary()

        report = f"""# Task Completion Report

**Generated:** {datetime.now().isoformat()}

## Summary
- Total Tasks: {summary['total']}
- Completed: {summary['completed']}
- In Progress: {summary['in_progress']}
- Pending: {summary['pending']}

## Completion Rate
{(summary['completed'] / summary['total'] * 100) if summary['total'] > 0 else 0:.1f}%

## Task Details

"""

        for task_id, task in self.tasks.items():
            status_emoji = {
                'completed': '✓',
                'in_progress': '⏳',
                'pending': '○'
            }.get(task['status'], '?')

            report += f"### {status_emoji} {task_id}\n"
            report += f"- Status: {task['status']}\n"
            report += f"- Created: {task['created']}\n"
            report += f"- Updated: {task['updated']}\n"
            if task.get('dependencies'):
                report += f"- Dependencies: {', '.join(task['dependencies'])}\n"
            report += "\n"

        return report

    def clear_completed_tasks(self):
        """Remove completed tasks from tracker"""
        self.tasks = {tid: task for tid, task in self.tasks.items() if task['status'] != 'completed'}
        self.save_state()

if __name__ == "__main__":
    # Test task tracker
    tracker = TaskTracker()

    # Add test tasks
    tracker.add_task("task1", {"description": "Process email"})
    tracker.add_task("task2", {"description": "Create invoice"})
    tracker.add_task("task3", {"description": "Send report"})

    # Add dependency
    tracker.add_dependency("task3", "task2")

    # Update statuses
    tracker.update_task_status("task1", "completed")
    tracker.update_task_status("task2", "in_progress")

    # Print summary
    print(tracker.get_task_summary())
    print("\nPending tasks:", tracker.get_pending_tasks())
    print("All complete?", tracker.all_tasks_complete())

    # Generate report
    print("\n" + tracker.generate_completion_report())
