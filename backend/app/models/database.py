from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meeting(Base):
    """Meeting database model"""
    __tablename__ = "meetings"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # File info
    audio_filename = Column(String, nullable=False)
    audio_path = Column(String, nullable=True)
    audio_duration_seconds = Column(Float, nullable=True)
    
    # Processing
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    topics = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String, default="uploading")
    error_message = Column(Text, nullable=True)
    
    # LLM info
    llm_provider = Column(String, nullable=True)
    
    # Analytics
    word_count = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Meeting(id={self.id}, title={self.title}, status={self.status}, provider={self.llm_provider})>"
