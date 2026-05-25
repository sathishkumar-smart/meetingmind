import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import Meeting
from app.schemas.meeting import MeetingCreate


class MeetingService:
    """Service for meeting business logic"""
    
    @staticmethod
    def create_meeting(db: Session, meeting_data: MeetingCreate, audio_filename: str) -> Meeting:
        """Create a new meeting record"""
        meeting_id = str(uuid.uuid4())
        
        meeting = Meeting(
            id=meeting_id,
            title=meeting_data.title,
            description=meeting_data.description,
            audio_filename=audio_filename,
            status="uploading"
        )
        
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        
        return meeting
    
    @staticmethod
    def get_meeting(db: Session, meeting_id: str) -> Meeting:
        """Get meeting by ID"""
        return db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    @staticmethod
    def list_meetings(db: Session, skip: int = 0, limit: int = 20):
        """List all meetings with pagination"""
        return db.query(Meeting).order_by(Meeting.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_meeting(db: Session, meeting_id: str) -> bool:
        """Delete a meeting"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            db.delete(meeting)
            db.commit()
            return True
        return False
    
    @staticmethod
    def update_meeting_transcript(db: Session, meeting_id: str, transcript: str, word_count: int) -> Meeting:
        """Update meeting with transcript"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.transcript = transcript
            meeting.word_count = word_count
            db.commit()
            db.refresh(meeting)
        return meeting
    
    @staticmethod
    def update_meeting_processing(
        db: Session, meeting_id: str, summary_data: dict, llm_provider: str
    ) -> Meeting:
        """Update meeting with processed data"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.summary = summary_data.get("summary", "")
            meeting.action_items = json.dumps(summary_data.get("action_items", []))
            meeting.topics = json.dumps(summary_data.get("topics", []))
            meeting.llm_provider = llm_provider
            meeting.status = "completed"
            meeting.processed_at = datetime.utcnow()
            db.commit()
            db.refresh(meeting)
        return meeting
    
    @staticmethod
    def update_meeting_status(db: Session, meeting_id: str, status: str, error_message: str = None) -> Meeting:
        """Update meeting status"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.status = status
            if error_message:
                meeting.error_message = error_message
            db.commit()
            db.refresh(meeting)
        return meeting
    
    @staticmethod
    def search_meetings(db: Session, query: str):
        """Search meetings by title, description, or transcript"""
        return db.query(Meeting).filter(
            (Meeting.title.ilike(f"%{query}%")) |
            (Meeting.description.ilike(f"%{query}%")) |
            (Meeting.transcript.ilike(f"%{query}%"))
        ).order_by(Meeting.created_at.desc()).all()