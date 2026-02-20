#!/usr/bin/env python3
"""
Zone Router - Routes tasks to appropriate zone (cloud or local)
"""

import json
from pathlib import Path
from typing import Dict, Literal

class ZoneRouter:
    """
    Routes tasks to appropriate execution zone.

    Cloud zone: Monitoring, lightweight processing
    Local zone: Execution, browser automation, MCP calls
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / 'work_zone_config.json'

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.cloud_zone = self.config['cloud_zone']
        self.local_zone = self.config['local_zone']
        self.routing_rules = self.config['routing_rules']

    def route_task(self, task_type: str) -> Literal['cloud', 'local', 'both']:
        """
        Determine which zone should handle this task.

        Args:
            task_type: Type of task (e.g., 'email_detection', 'email_sending')

        Returns:
            'cloud', 'local', or 'both'
        """
        return self.routing_rules.get(task_type, 'local')

    def can_execute_in_cloud(self, task_type: str) -> bool:
        """Check if task can be executed in cloud zone"""
        zone = self.route_task(task_type)
        return zone in ['cloud', 'both']

    def can_execute_locally(self, task_type: str) -> bool:
        """Check if task can be executed locally"""
        zone = self.route_task(task_type)
        return zone in ['local', 'both']

    def requires_browser(self, task_type: str) -> bool:
        """Check if task requires browser automation"""
        browser_tasks = [
            'social_media_posting',
            'browser_automation',
            'whatsapp_messaging'
        ]
        return task_type in browser_tasks

    def requires_approval(self, task_type: str) -> bool:
        """Check if task requires human approval"""
        approval_tasks = [
            'email_sending',
            'social_media_posting',
            'payment_execution'
        ]
        return task_type in approval_tasks

    def get_zone_capabilities(self, zone: Literal['cloud', 'local']) -> Dict:
        """Get capabilities of a specific zone"""
        if zone == 'cloud':
            return self.cloud_zone
        elif zone == 'local':
            return self.local_zone
        else:
            return {}

    def validate_task_for_zone(self, task_type: str, zone: Literal['cloud', 'local']) -> bool:
        """
        Validate if a task can be executed in the specified zone.

        Args:
            task_type: Type of task
            zone: Target zone

        Returns:
            True if task can be executed in zone, False otherwise
        """
        zone_config = self.get_zone_capabilities(zone)

        # Check if task is in zone's task list
        if task_type in zone_config.get('tasks', []):
            return True

        # Check routing rules
        routed_zone = self.route_task(task_type)
        return routed_zone == zone or routed_zone == 'both'

if __name__ == "__main__":
    # Test zone router
    router = ZoneRouter()

    print("Testing Zone Router:")
    print(f"Email detection -> {router.route_task('email_detection')}")
    print(f"Email sending -> {router.route_task('email_sending')}")
    print(f"Social media posting -> {router.route_task('social_media_posting')}")
    print(f"Browser required for posting? {router.requires_browser('social_media_posting')}")
    print(f"Approval required for posting? {router.requires_approval('social_media_posting')}")

    print("\nCloud capabilities:")
    print(json.dumps(router.get_zone_capabilities('cloud'), indent=2))
