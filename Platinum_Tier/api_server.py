#!/usr/bin/env python3
"""
API Server - Platinum Tier
FastAPI server for webhooks and external integrations
"""

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import logging
from datetime import datetime
from pathlib import Path
import json
import asyncio

# Import integrations
import sys
sys.path.append(str(Path(__file__).parent))

from Voice.vapi_integration import VapiIntegration
from Memory.vector_store import VectorStore

# Initialize FastAPI
app = FastAPI(
    title="Platinum AI Employee API",
    description="Enterprise AI Employee System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vapi = VapiIntegration()
vector_store = VectorStore(provider="chromadb")

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

class TaskCreate(BaseModel):
    content: str
    priority: Optional[int] = 5
    metadata: Optional[Dict] = None

class ConversationQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5

# Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Platinum AI Employee API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/tasks")
async def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    """
    Create a new task.

    This endpoint allows external systems to create tasks
    that will be processed by the AI Employee.
    """
    try:
        # Create task file
        base_dir = Path("Platinum_Tier")
        needs_action = base_dir / "Needs_Action"
        needs_action.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task_file = needs_action / f"API_TASK_{timestamp}.txt"

        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task.content)

        # Add metadata if provided
        if task.metadata:
            metadata_file = needs_action / f"API_TASK_{timestamp}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(task.metadata, f, indent=2)

        logger.info(f"Task created: {task_file.name}")

        return {
            "status": "success",
            "task_id": f"API_TASK_{timestamp}",
            "message": "Task created successfully"
        }

    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/webhook")
async def voice_webhook(request: Request):
    """
    Vapi voice webhook endpoint.

    Receives events from Vapi voice calls.
    """
    try:
        data = await request.json()
        logger.info(f"Voice webhook received: {data.get('message', {}).get('type')}")

        # Handle webhook
        response = await vapi.handle_webhook(data)

        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"Error handling voice webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice/call")
async def initiate_call(phone_number: str, assistant_id: str, context: Optional[Dict] = None):
    """
    Initiate an outbound voice call.

    Args:
        phone_number: Phone number to call
        assistant_id: Vapi assistant ID
        context: Optional context for the call
    """
    try:
        call_id = await vapi.make_outbound_call(phone_number, assistant_id, context)

        if call_id:
            return {
                "status": "success",
                "call_id": call_id,
                "message": "Call initiated successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to initiate call")

    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/add")
async def add_conversation(conversation_id: str, text: str, metadata: Optional[Dict] = None):
    """
    Add conversation to long-term memory.

    Args:
        conversation_id: Unique conversation ID
        text: Conversation text
        metadata: Optional metadata
    """
    try:
        success = vector_store.add_conversation(conversation_id, text, metadata)

        if success:
            return {
                "status": "success",
                "conversation_id": conversation_id,
                "message": "Conversation added to memory"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add conversation")

    except Exception as e:
        logger.error(f"Error adding conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/search")
async def search_memory(query: ConversationQuery):
    """
    Search long-term memory for similar conversations.

    Args:
        query: Search query
        top_k: Number of results to return
    """
    try:
        results = vector_store.search_similar(query.query, top_k=query.top_k)

        return {
            "status": "success",
            "query": query.query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
async def memory_stats():
    """Get memory statistics"""
    try:
        stats = vector_store.get_stats()

        return {
            "status": "success",
            "stats": stats
        }

    except Exception as e:
        logger.error(f"Error getting memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voice/analytics")
async def voice_analytics(days: int = 7):
    """Get voice call analytics"""
    try:
        analytics = await vapi.get_call_analytics(days=days)

        return {
            "status": "success",
            "period_days": days,
            "analytics": analytics
        }

    except Exception as e:
        logger.error(f"Error getting voice analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def system_status():
    """Get overall system status"""
    try:
        # Check various components
        status = {
            "api": "operational",
            "voice": "operational",
            "memory": "operational",
            "timestamp": datetime.now().isoformat()
        }

        # Get memory stats
        try:
            memory_stats = vector_store.get_stats()
            status["memory_vectors"] = memory_stats.get("total_vectors", 0)
        except:
            status["memory"] = "degraded"

        # Get voice stats
        try:
            voice_analytics = await vapi.get_call_analytics(days=1)
            status["voice_calls_today"] = voice_analytics.get("total_calls", 0)
        except:
            status["voice"] = "degraded"

        return status

    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Startup/shutdown events

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info("Platinum AI Employee API starting...")
    logger.info("Voice integration initialized")
    logger.info("Vector store initialized")
    logger.info("API server ready")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("Platinum AI Employee API shutting down...")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
