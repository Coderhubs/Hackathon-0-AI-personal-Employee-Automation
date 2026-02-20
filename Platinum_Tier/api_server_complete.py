#!/usr/bin/env python3
"""
REST API Server - Platinum Tier
FastAPI server for external integrations and webhooks
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import logging
from datetime import datetime
from pathlib import Path
import json
import sys

# Add Platinum_Tier to path
sys.path.append(str(Path(__file__).parent))

try:
    from agent_coordinator import MultiAgentCoordinator
    from memory_store import MemoryStore
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False
    print("Warning: Some Platinum components not available")

# Initialize FastAPI
app = FastAPI(
    title="Platinum AI Employee API",
    description="Enterprise AI Employee System with Multi-Agent Coordination",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
if COMPONENTS_AVAILABLE:
    coordinator = MultiAgentCoordinator()
    memory = MemoryStore()
else:
    coordinator = None
    memory = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('APIServer')

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    components: Dict[str, bool]

class TaskCreate(BaseModel):
    content: str
    task_type: str = "general"
    priority: Optional[int] = 5
    metadata: Optional[Dict] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
    assigned_agent: Optional[str] = None

class ConversationStore(BaseModel):
    content: str
    metadata: Optional[Dict] = None

class ConversationSearch(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AgentStatus(BaseModel):
    agent_id: str
    type: str
    status: str
    tasks_completed: int

# Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Platinum AI Employee API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components={
            "multi_agent": coordinator is not None,
            "memory_store": memory is not None,
            "api_server": True
        }
    )

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    """
    Create a new task for the AI Employee.

    The task will be routed to an appropriate agent based on task_type.
    """
    try:
        # Generate task ID
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create task file in vault
        base_dir = Path("AI_Employee_Vault")
        needs_action = base_dir / "Needs_Action"
        needs_action.mkdir(parents=True, exist_ok=True)

        task_file = needs_action / f"{task_id}.md"

        # Write task file
        task_content = f"""---
type: api_task
task_type: {task.task_type}
priority: {task.priority}
created: {datetime.now().isoformat()}
status: pending
---

# Task: {task_id}

{task.content}

## Metadata
{json.dumps(task.metadata or {}, indent=2)}
"""

        task_file.write_text(task_content)

        # Route to agent if coordinator available
        assigned_agent = None
        if coordinator:
            result = coordinator.route_task(task.content, task.task_type)
            assigned_agent = result.split("assigned to ")[-1] if "assigned to" in result else None

        logger.info(f"Created task: {task_id}")

        return TaskResponse(
            task_id=task_id,
            status="created",
            message=f"Task created and saved to {task_file}",
            assigned_agent=assigned_agent
        )

    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get task status"""
    try:
        # Check in Needs_Action
        base_dir = Path("AI_Employee_Vault")

        folders = ["Needs_Action", "Pending_Approval", "Approved", "Done"]

        for folder in folders:
            task_file = base_dir / folder / f"{task_id}.md"
            if task_file.exists():
                return {
                    "task_id": task_id,
                    "status": folder.lower().replace("_", " "),
                    "location": str(task_file),
                    "content": task_file.read_text()
                }

        raise HTTPException(status_code=404, detail="Task not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents", response_model=List[AgentStatus])
async def list_agents():
    """List all agents and their status"""
    if not coordinator:
        raise HTTPException(status_code=503, detail="Multi-agent coordinator not available")

    try:
        status = coordinator.get_system_status()

        agents = []
        for agent_data in status['agents']:
            agents.append(AgentStatus(
                agent_id=agent_data['agent_id'],
                type=agent_data['type'],
                status=agent_data['status'],
                tasks_completed=agent_data['tasks_completed']
            ))

        return agents

    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/status")
async def get_agent_system_status():
    """Get overall agent system status"""
    if not coordinator:
        raise HTTPException(status_code=503, detail="Multi-agent coordinator not available")

    try:
        return coordinator.get_system_status()
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/store")
async def store_conversation(data: ConversationStore):
    """Store a conversation in long-term memory"""
    if not memory:
        raise HTTPException(status_code=503, detail="Memory store not available")

    try:
        conversation_id = memory.store_conversation(
            data.content,
            data.metadata or {}
        )

        return {
            "conversation_id": conversation_id,
            "status": "stored",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to store conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/search")
async def search_conversations(query: ConversationSearch):
    """Search conversations using semantic similarity"""
    if not memory:
        raise HTTPException(status_code=503, detail="Memory store not available")

    try:
        results = memory.search(query.query, query.top_k)

        return {
            "query": query.query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        logger.error(f"Failed to search conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory system statistics"""
    if not memory:
        raise HTTPException(status_code=503, detail="Memory store not available")

    try:
        return memory.get_stats()
    except Exception as e:
        logger.error(f"Failed to get memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def webhook_handler(request: Dict):
    """
    Generic webhook handler for external integrations.

    Can receive webhooks from:
    - Zapier
    - Make.com
    - n8n
    - Custom integrations
    """
    try:
        logger.info(f"Received webhook: {request}")

        # Extract content
        content = request.get('content') or request.get('text') or str(request)

        # Create task
        task = TaskCreate(
            content=content,
            task_type="webhook",
            metadata={"source": "webhook", "raw": request}
        )

        # Process task
        result = await create_task(task, BackgroundTasks())

        return {
            "status": "received",
            "task_id": result.task_id,
            "message": "Webhook processed successfully"
        }

    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    logger.info("=" * 70)
    logger.info("Platinum AI Employee API Server")
    logger.info("=" * 70)
    logger.info(f"Multi-Agent Coordinator: {'Available' if coordinator else 'Not Available'}")
    logger.info(f"Memory Store: {'Available' if memory else 'Not Available'}")
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("=" * 70)

if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("Starting Platinum AI Employee API Server")
    print("=" * 70)
    print()
    print("API will be available at: http://localhost:8000")
    print("Documentation: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
