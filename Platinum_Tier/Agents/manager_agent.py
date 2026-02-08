#!/usr/bin/env python3
"""
Manager Agent - Platinum Tier
Orchestrates specialist agents and delegates tasks
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

class ManagerAgent:
    """
    Manager Agent coordinates all specialist agents.

    Responsibilities:
    - Task routing and delegation
    - Agent coordination
    - Load balancing
    - Priority management
    - Conflict resolution
    """

    def __init__(self, base_dir="Platinum_Tier"):
        self.base_dir = Path(base_dir)
        self.needs_action = self.base_dir / "Needs_Action"
        self.plans = self.base_dir / "Plans"
        self.logs = self.base_dir / "Logs"

        # Specialist agents registry
        self.agents = {
            'social_media': None,
            'accounting': None,
            'email': None,
            'voice': None,
            'general': None
        }

        # Task queue
        self.task_queue = asyncio.Queue()
        self.running = True

        self.setup_logging()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.logs / f"manager_agent_{datetime.now().strftime('%Y%m%d')}.log"
        self.logs.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ManagerAgent')

    def load_specialist_agents(self):
        """Load and initialize specialist agents"""
        try:
            # Import specialist agents
            from Agents.social_media_agent import SocialMediaAgent
            from Agents.accounting_agent import AccountingAgent
            from Agents.email_agent import EmailAgent

            self.agents['social_media'] = SocialMediaAgent()
            self.agents['accounting'] = AccountingAgent()
            self.agents['email'] = EmailAgent()

            self.logger.info("All specialist agents loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading specialist agents: {e}")

    def analyze_task(self, task_file: Path) -> Dict:
        """
        Analyze task and determine which agent should handle it.

        Returns:
            Dict with agent_type, priority, and task_data
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple keyword-based routing (can be enhanced with AI)
            task_info = {
                'file': task_file,
                'content': content,
                'agent_type': 'general',
                'priority': 5,  # 1-10, 10 is highest
                'timestamp': datetime.now().isoformat()
            }

            # Determine agent type
            content_lower = content.lower()

            if any(word in content_lower for word in ['facebook', 'instagram', 'twitter', 'social', 'post']):
                task_info['agent_type'] = 'social_media'
                task_info['priority'] = 7

            elif any(word in content_lower for word in ['invoice', 'payment', 'accounting', 'odoo', 'expense']):
                task_info['agent_type'] = 'accounting'
                task_info['priority'] = 9

            elif any(word in content_lower for word in ['email', 'gmail', 'message', 'reply']):
                task_info['agent_type'] = 'email'
                task_info['priority'] = 6

            elif any(word in content_lower for word in ['call', 'phone', 'appointment', 'voice']):
                task_info['agent_type'] = 'voice'
                task_info['priority'] = 8

            self.logger.info(f"Task analyzed: {task_file.name} -> {task_info['agent_type']} (priority: {task_info['priority']})")
            return task_info

        except Exception as e:
            self.logger.error(f"Error analyzing task {task_file}: {e}")
            return None

    async def delegate_task(self, task_info: Dict) -> bool:
        """
        Delegate task to appropriate specialist agent.

        Returns:
            True if delegation successful, False otherwise
        """
        try:
            agent_type = task_info['agent_type']
            agent = self.agents.get(agent_type)

            if not agent:
                self.logger.warning(f"No agent available for type: {agent_type}")
                return False

            # Delegate to specialist agent
            self.logger.info(f"Delegating task to {agent_type} agent")

            # Call agent's process method (async)
            result = await agent.process_task(task_info)

            if result:
                self.logger.info(f"Task successfully processed by {agent_type} agent")
                return True
            else:
                self.logger.error(f"Task processing failed by {agent_type} agent")
                return False

        except Exception as e:
            self.logger.error(f"Error delegating task: {e}")
            return False

    async def monitor_agents(self):
        """Monitor health of specialist agents"""
        while self.running:
            try:
                for agent_type, agent in self.agents.items():
                    if agent:
                        # Check agent health
                        health = await agent.health_check()
                        if not health:
                            self.logger.warning(f"Agent {agent_type} is unhealthy, attempting restart")
                            # Attempt to restart agent
                            await self.restart_agent(agent_type)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Error monitoring agents: {e}")
                await asyncio.sleep(30)

    async def restart_agent(self, agent_type: str):
        """Restart a specialist agent"""
        try:
            self.logger.info(f"Restarting {agent_type} agent")
            # Reload agent
            self.load_specialist_agents()
        except Exception as e:
            self.logger.error(f"Error restarting {agent_type} agent: {e}")

    async def process_queue(self):
        """Process task queue continuously"""
        while self.running:
            try:
                # Get task from queue
                task_info = await self.task_queue.get()

                # Delegate to appropriate agent
                success = await self.delegate_task(task_info)

                if success:
                    # Move task file to appropriate folder
                    task_file = task_info['file']
                    done_file = self.base_dir / "Done" / task_file.name
                    task_file.rename(done_file)
                else:
                    # Move to rejected or retry
                    rejected_file = self.base_dir / "Rejected" / task_file.name
                    task_file.rename(rejected_file)

                self.task_queue.task_done()

            except Exception as e:
                self.logger.error(f"Error processing queue: {e}")
                await asyncio.sleep(5)

    async def scan_needs_action(self):
        """Scan Needs_Action folder for new tasks"""
        while self.running:
            try:
                if not self.needs_action.exists():
                    await asyncio.sleep(5)
                    continue

                # Get all files
                files = [f for f in self.needs_action.iterdir() if f.is_file()]

                for file in files:
                    # Analyze task
                    task_info = self.analyze_task(file)

                    if task_info:
                        # Add to queue
                        await self.task_queue.put(task_info)
                        self.logger.info(f"Task added to queue: {file.name}")

                await asyncio.sleep(5)  # Scan every 5 seconds

            except Exception as e:
                self.logger.error(f"Error scanning Needs_Action: {e}")
                await asyncio.sleep(5)

    async def run(self):
        """Main run loop - Manager Agent never stops"""
        self.logger.info("Manager Agent starting - Platinum Tier")
        self.logger.info("Loading specialist agents...")

        self.load_specialist_agents()

        self.logger.info("Starting task processing...")

        # Start all async tasks
        tasks = [
            asyncio.create_task(self.scan_needs_action()),
            asyncio.create_task(self.process_queue()),
            asyncio.create_task(self.monitor_agents())
        ]

        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            self.logger.info("Manager Agent stopped by user")
            self.running = False
        except Exception as e:
            self.logger.error(f"Manager Agent error: {e}")

if __name__ == "__main__":
    manager = ManagerAgent()
    asyncio.run(manager.run())
