from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import asyncio
from app.database import get_db, SessionLocal
from app.services.meeting_service import MeetingService
from app.services.audio_service import AudioService
from app.services.llm_service import llm_service
from app.schemas.meeting import MeetingCreate, MeetingResponse

router = APIRouter(prefix="/api/v1/meetings", tags=["meetings"])
audio_service = AudioService()


@router.post("", response_model=MeetingResponse)
async def create_meeting(
    title: str = Form(...),
    description: str = Form(None),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload audio and create a new meeting"""
    # Validate file
    content = await audio_file.read()
    is_valid, message = audio_service.validate_audio_file(audio_file.filename, len(content))
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Create meeting record
    meeting_data = MeetingCreate(title=title, description=description)
    meeting = MeetingService.create_meeting(db, meeting_data, audio_file.filename)
    
    # Save audio file
    file_path = audio_service.save_audio_file(content, f"{meeting.id}_{audio_file.filename}")
    meeting.audio_path = file_path
    db.commit()
    
    # Get audio duration
    meeting.audio_duration_seconds = audio_service.get_audio_duration(file_path)
    db.commit()
    
    # Start processing in background (background task opens its own session)
    MeetingService.update_meeting_status(db, meeting.id, "processing")
    asyncio.create_task(process_meeting_async(meeting.id, file_path))
    
    return meeting


@router.get("", response_model=list[MeetingResponse])
def list_meetings(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all meetings"""
    meetings = MeetingService.list_meetings(db, skip, limit)
    return meetings

@router.get("/search")
def search_meetings(
    query: str,
    db: Session = Depends(get_db)
):
    """Search meetings by title, description, or content"""
    from app.services.meeting_service import MeetingService
    
    meetings = MeetingService.search_meetings(db, query)
    return meetings

@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Get meeting by ID"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Delete a meeting"""
    success = MeetingService.delete_meeting(db, meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"message": "Meeting deleted successfully"}


@router.get("/{meeting_id}/summary")
def get_summary(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Get meeting summary"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if not meeting.summary:
        raise HTTPException(status_code=202, detail="Summary not ready yet")
    
    import json
    return {
        "meeting_id": meeting.id,
        "summary": meeting.summary,
        "action_items": json.loads(meeting.action_items) if meeting.action_items else [],
        "topics": json.loads(meeting.topics) if meeting.topics else [],
        "llm_provider": meeting.llm_provider
    }


@router.get("/{meeting_id}/transcript")
def get_transcript(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Get meeting transcript"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if not meeting.transcript:
        raise HTTPException(status_code=202, detail="Transcript not ready yet")
    
    return {
        "meeting_id": meeting.id,
        "transcript": meeting.transcript,
        "word_count": meeting.word_count,
        "duration_seconds": meeting.audio_duration_seconds
    }


async def process_meeting_async(meeting_id: str, audio_path: str):
    """Process meeting: transcribe and summarize"""
    db = SessionLocal()
    try:
        # Transcribe audio
        transcript, word_count = await audio_service.transcribe_audio(audio_path)
        MeetingService.update_meeting_transcript(db, meeting_id, transcript, word_count)

        # Get active LLM provider
        provider = await llm_service.get_active_provider()

        # Summarize with LLM
        summary_data = await llm_service.summarize(transcript)
        MeetingService.update_meeting_processing(db, meeting_id, summary_data, provider)

    except Exception as e:
        MeetingService.update_meeting_status(db, meeting_id, "failed", str(e))
    finally:
        db.close()

@router.get("/{meeting_id}/export/markdown")
def export_markdown(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Export meeting as Markdown"""
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    from app.services.export_service import ExportService
    markdown_content = ExportService.to_markdown(meeting)
    
    return {
        "filename": f"{meeting.title}.md",
        "content": markdown_content
    }


@router.get("/{meeting_id}/export/pdf")
def export_pdf(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Export meeting as PDF"""
    from fastapi.responses import FileResponse
    from io import BytesIO
    
    meeting = MeetingService.get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    from app.services.export_service import ExportService
    pdf_bytes = ExportService.to_pdf(meeting)
    
    # Return as downloadable file
    return FileResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        filename=f"{meeting.title}.pdf"
    )