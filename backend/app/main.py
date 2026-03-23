# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes import chat, analytics
from app.services.bot_service import bot_service
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs on startup and shutdown.
    We initialize DB + bot service here — once, not per request.
    """
    print("🚀 Starting EI-AI Research API...")
    await init_db()
    bot_service.initialize()
    print("✅ API ready!")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title       = os.getenv("APP_NAME", "EI-AI Research API"),
    version     = os.getenv("APP_VERSION", "1.0.0"),
    description = "Emotionally Intelligent AI — Academic Research API",
    lifespan    = lifespan,
)

# CORS — allows your Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins  = [os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)

# Register routes
app.include_router(chat.router,      prefix="/api/chat",      tags=["Chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "status":  "running",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs":    "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}