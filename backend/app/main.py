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
from app.api import (
    recruitment, records, onboarding, payroll, 
    leave, performance, training, relations, compliance, analytics, engagement
)

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

# Mount Dashboard REST API routes
app.include_router(recruitment.router, prefix="/api/recruitment", tags=["recruitment"])
app.include_router(records.router, prefix="/api/records", tags=["records"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["onboarding"])
app.include_router(payroll.router, prefix="/api/payroll", tags=["payroll"])
app.include_router(leave.router, prefix="/api/leave", tags=["leave"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(relations.router, prefix="/api/relations", tags=["relations"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["compliance"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(engagement.router, prefix="/api/engagement", tags=["engagement"])


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "HR AI Agent System"}
