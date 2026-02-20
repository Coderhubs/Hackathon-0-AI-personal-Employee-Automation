#!/usr/bin/env python3
"""
Multi-Agent Coordinator - Platinum Tier
Coordinates multiple specialized agents for complex tasks
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class AgentType(Enum):
    """Types of specialized agents"""
    RESEARCHER = "researcher"  # Gathers information
    EXECUTOR = "executor"      # Executes actions
    MONITOR = "monitor"        # Monitors systems
    PLANNER = "planner"        # Creates plans
    REVIEWER = "reviewer"      # Reviews outputs

class AgentStatus(Enum):
    """Agent status"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class Agent:
    """Represents a specialized agent"""

    def __init__(self, agent_id: str, agent_type: AgentType, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.tasks_completed = 0
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'agent_id': self.agent_id,
            'type': self.agent_type.value,
            'capabilities': self.capabilities,
            'status': self.status.value,
            'current_task': self.current_task,
            'tasks_completed': self.tasks_completed,
            'created_at': self.created_at.isoformat()
        }

class MultiAgentCoordinator:
    """
    Coordinates multiple specialized agents.

    Features:
    - Agent registration and discovery
    - Task routing based on capabilities
    - Load balancing
    - Agent health monitoring
    """

    def __init__(self, base_dir="AI_Employee_Vault"):
        self.base_dir = Path(base_dir)
        self.agents: Dict[str, Agent] = {}
        self.task_queue = []
        self.completed_tasks = []

        # Platinum Tier folders
        self.platinum_dir = Path("Platinum_Tier")
        self.logs = self.platinum_dir / "Logs"
        self.logs.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs / 'coordinator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MultiAgentCoordinator')

        # Initialize default agents
        self._initialize_default_agents()

    def _initialize_default_agents(self):
        """Initialize default agent pool"""
        default_agents = [
            Agent("researcher-1", AgentType.RESEARCHER,
                  ["web_search", "data_analysis", "information_gathering"]),
            Agent("executor-1", AgentType.EXECUTOR,
                  ["email_sending", "file_operations", "api_calls"]),
            Agent("monitor-1", AgentType.MONITOR,
                  ["system_health", "watcher_status", "error_detection"]),
            Agent("planner-1", AgentType.PLANNER,
                  ["task_planning", "workflow_design", "strategy"]),
            Agent("reviewer-1", AgentType.REVIEWER,
                  ["quality_check", "approval_review", "validation"])
        ]

        for agent in default_agents:
            self.register_agent(agent)
            self.logger.info(f"Initialized agent: {agent.agent_id} ({agent.agent_type.value})")

    def register_agent(self, agent: Agent):
        """Register a new agent"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.agent_id}")

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)

    def get_agents_by_type(self, agent_type: AgentType) -> List[Agent]:
        """Get all agents of a specific type"""
        return [agent for agent in self.agents.values()
                if agent.agent_type == agent_type]

    def get_available_agent(self, required_capability: str) -> Optional[Agent]:
        """
        Find an available agent with the required capability.

        Uses load balancing to distribute tasks evenly.
        """
        # Find agents with the capability
        capable_agents = [
            agent for agent in self.agents.values()
            if required_capability in agent.capabilities
            and agent.status == AgentStatus.IDLE
        ]

        if not capable_agents:
            return None

        # Return agent with fewest completed tasks (load balancing)
        return min(capable_agents, key=lambda a: a.tasks_completed)

    def assign_task(self, task: Dict, required_capability: str) -> Optional[str]:
        """
        Assign task to an appropriate agent.

        Returns agent_id if successful, None if no agent available.
        """
        agent = self.get_available_agent(required_capability)

        if not agent:
            self.logger.warning(f"No available agent for capability: {required_capability}")
            self.task_queue.append(task)
            return None

        # Assign task
        agent.status = AgentStatus.BUSY
        agent.current_task = task

        self.logger.info(f"Assigned task to {agent.agent_id}: {task.get('description', 'No description')}")

        return agent.agent_id

    def complete_task(self, agent_id: str, result: Dict):
        """Mark task as complete for an agent"""
        agent = self.get_agent(agent_id)

        if not agent:
            self.logger.error(f"Agent not found: {agent_id}")
            return

        # Update agent
        agent.status = AgentStatus.IDLE
        agent.tasks_completed += 1
        completed_task = agent.current_task
        agent.current_task = None

        # Log completion
        self.completed_tasks.append({
            'agent_id': agent_id,
            'task': completed_task,
            'result': result,
            'completed_at': datetime.now().isoformat()
        })

        self.logger.info(f"Task completed by {agent_id}")

        # Process queued tasks
        self._process_queue()

    def _process_queue(self):
        """Process queued tasks"""
        if not self.task_queue:
            return

        # Try to assign queued tasks
        remaining_queue = []
        for task in self.task_queue:
            capability = task.get('required_capability', 'general')
            agent_id = self.assign_task(task, capability)

            if not agent_id:
                remaining_queue.append(task)

        self.task_queue = remaining_queue

    def get_system_status(self) -> Dict:
        """Get overall system status"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(self.agents),
            'agents_by_status': {},
            'agents_by_type': {},
            'queued_tasks': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'agents': []
        }

        # Count by status
        for status_type in AgentStatus:
            count = sum(1 for a in self.agents.values() if a.status == status_type)
            status['agents_by_status'][status_type.value] = count

        # Count by type
        for agent_type in AgentType:
            count = sum(1 for a in self.agents.values() if a.agent_type == agent_type)
            status['agents_by_type'][agent_type.value] = count

        # Agent details
        status['agents'] = [agent.to_dict() for agent in self.agents.values()]

        return status

    def route_task(self, task_description: str, task_type: str) -> str:
        """
        Intelligent task routing based on task type.

        Returns the agent_id that should handle the task.
        """
        # Determine required capability based on task type
        capability_map = {
            'research': 'web_search',
            'email': 'email_sending',
            'monitor': 'system_health',
            'plan': 'task_planning',
            'review': 'quality_check'
        }

        required_capability = capability_map.get(task_type, 'general')

        task = {
            'description': task_description,
            'type': task_type,
            'required_capability': required_capability,
            'created_at': datetime.now().isoformat()
        }

        agent_id = self.assign_task(task, required_capability)

        if agent_id:
            return f"Task assigned to {agent_id}"
        else:
            return f"Task queued (no available agent with capability: {required_capability})"

    def run_demo(self):
        """Run a demo of the multi-agent system"""
        self.logger.info("=== Multi-Agent Coordinator Demo ===")

        # Show initial status
        status = self.get_system_status()
        self.logger.info(f"System initialized with {status['total_agents']} agents")

        # Simulate task routing
        tasks = [
            ("Research latest AI trends", "research"),
            ("Send email to client", "email"),
            ("Check system health", "monitor"),
            ("Create execution plan", "plan"),
            ("Review approval request", "review")
        ]

        for description, task_type in tasks:
            result = self.route_task(description, task_type)
            self.logger.info(result)

        # Show final status
        status = self.get_system_status()
        self.logger.info(f"Active agents: {status['agents_by_status']['busy']}")
        self.logger.info(f"Queued tasks: {status['queued_tasks']}")

def main():
    """Main entry point"""
    coordinator = MultiAgentCoordinator()

    print("=" * 70)
    print("Multi-Agent Coordinator - Platinum Tier")
    print("=" * 70)
    print()

    # Run demo
    coordinator.run_demo()

    print()
    print("=" * 70)
    print("Multi-agent system operational")
    print("=" * 70)

if __name__ == "__main__":
    main()
