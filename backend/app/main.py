"""
HR AI Agent System — FastAPI Application Entry Point
=====================================================
Initializes the FastAPI app with CORS middleware, REST API routers,
and the WebSocket endpoint for real-time chat streaming.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

# ---------------------------------------------------------------------------
# Load environment variables from .env file (if present)
# ---------------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------------
# Application lifespan — startup / shutdown hooks
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    print("[STARTUP] HR AI Agent System starting up...")
    print(f"   OpenAI key configured: {'YES' if os.getenv('OPENAI_API_KEY') else 'MISSING'}")
    yield
    print("[SHUTDOWN] HR AI Agent System shutting down...")


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="HR AI Agent System",
    description="A comprehensive AI-powered HR management system with 11 specialized tool categories.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS Middleware — allow all origins for development
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register API routers
# ---------------------------------------------------------------------------

app.include_router(chat_router, prefix="/api")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "HR AI Agent System"}
