import uuid
import asyncio
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.meeting import Meeting
from app.api.models import (
    MeetingCreate, MeetingResponse, MeetingDetailsResponse,
    UploadResponse, StatusResponse, SearchRequest, SearchResponse
)
from app.services.file_service import save_uploaded_file, is_video_file, extract_audio_from_video
from app.services.transcription_service import process_transcription
from app.services.extraction_service import process_extraction
from app.services.search_service import store_meeting_vectors

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload meeting recording file"""
    meeting_id = str(uuid.uuid4())
    
    # Save file
    file_path = save_uploaded_file(file, meeting_id)
    
    # If video, extract audio
    if is_video_file(file_path):
        file_path = extract_audio_from_video(file_path)
    
    # Create meeting record
    meeting = Meeting(
        meeting_id=meeting_id,
        filename=file.filename,
        status="processing"
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    # Start background processing
    asyncio.create_task(process_meeting(meeting_id, file_path, db))
    
    return UploadResponse(meeting_id=meeting_id, status="processing")

@router.get("/meetings/{meeting_id}/status", response_model=StatusResponse)
async def get_meeting_status(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Get meeting processing status"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # In a real implementation, you'd track actual progress
    progress = 100 if meeting.status == "completed" else 50 if meeting.status == "processing" else 0
    
    return StatusResponse(status=meeting.status, progress=progress)

@router.get("/meetings/{meeting_id}", response_model=MeetingDetailsResponse)
async def get_meeting_details(
    meeting_id: str,
    db: Session = Depends(get_db)
):
    """Get meeting details and insights"""
    meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return meeting

@router.get("/meetings", response_model=List[MeetingResponse])
async def list_meetings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all meetings"""
    meetings = db.query(Meeting).offset(skip).limit(limit).all()
    return meetings

@router.post("/search", response_model=SearchResponse)
async def search_meetings(
    search_request: SearchRequest
):
    """Search meeting content"""
    from ai.search.chroma_client import search_client
    results = search_client.search(
        query=search_request.query,
        meeting_id=search_request.meeting_id
    )
    
    return SearchResponse(results=[
        {
            "id": results["ids"][i],
            "content": results["documents"][i],
            "metadata": results["metadatas"][i],
            "distance": results["distances"][i] if results["distances"] else 0
        }
        for i in range(len(results["documents"]))
    ])

async def process_meeting(meeting_id: str, file_path: str, db: Session):
    """Background task to process meeting"""
    try:
        # Update status
        meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if meeting:
            meeting.status = "processing"
            db.commit()
        
        # Transcription
        transcript = await process_transcription(file_path)
        
        # Information extraction
        insights = await process_extraction(transcript)
        
        # Update database
        if meeting:
            meeting.transcript = transcript
            meeting.action_items = insights.get("action_items", [])
            meeting.decisions = insights.get("decisions", [])
            meeting.participants = insights.get("participants", [])
            meeting.topics = insights.get("topics", [])
            meeting.status = "completed"
            db.commit()
        
        # Store in vector database
        store_meeting_vectors(meeting_id, transcript)
        
    except Exception as e:
        # Handle errors
        print(f"Meeting processing error for {meeting_id}: {e}")
        meeting = db.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if meeting:
            meeting.status = "failed"
            db.commit()