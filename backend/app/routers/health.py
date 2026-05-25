from fastapi import APIRouter
from app.services.llm_service import llm_service
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    llm_status = await llm_service.get_status()
    
    return {
        "status": "healthy",
        "service": "MeetingMind API",
        "version": "1.0.0",
        "llm": llm_status
    }


@router.get("/llm-status")
async def llm_status():
    """Get LLM provider status"""
    return await llm_service.get_status()


@router.get("/info")
def service_info():
    """Service information"""
    return {
        "name": "MeetingMind",
        "version": "1.0.0",
        "description": "AI-powered meeting transcription and summarization",
        "llm_provider": settings.LLM_PROVIDER,
        "ollama_model": settings.OLLAMA_MODEL,
        "groq_model": settings.GROQ_MODEL,
        "capabilities": [
            "Audio upload and transcription",
            "AI-powered summarization (Ollama or Groq)",
            "Action item extraction",
            "Topic detection"
        ]
    }
