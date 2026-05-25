from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MeetingCreate(BaseModel):
    """Schema for creating a meeting"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ActionItem(BaseModel):
    """Single action item"""
    task: str
    owner: Optional[str] = None


class MeetingResponse(BaseModel):
    """Full meeting response"""
    id: str
    title: str
    description: Optional[str]
    audio_filename: str
    audio_duration_seconds: Optional[float]
    transcript: Optional[str]
    summary: Optional[str]
    action_items: Optional[str]
    topics: Optional[str]
    status: str
    word_count: Optional[int]
    llm_provider: Optional[str]
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class TranscriptionResponse(BaseModel):
    """Transcription result"""
    meeting_id: str
    transcript: str
    duration_seconds: float
    word_count: int
    status: str


class SummaryResponse(BaseModel):
    """Summary result"""
    meeting_id: str
    summary: str
    action_items: List[ActionItem]
    key_points: List[str]
    topics: List[str]


class LLMStatusResponse(BaseModel):
    """LLM status information"""
    active_provider: str
    ollama_available: bool
    groq_available: bool
    ollama_model: Optional[str]
    groq_model: Optional[str]
