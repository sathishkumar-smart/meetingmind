from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import init_db
from app.routers import meetings, health


# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("✅ Database initialized")
    print(f"🎙️  MeetingMind API starting...")
    yield
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-powered meeting transcription with Ollama + Groq",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(meetings.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "🎙️ Welcome to MeetingMind API",
        "docs": "/docs",
        "health": "/health",
        "llm_status": "/llm-status"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
