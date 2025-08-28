import uuid
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="AI Meeting Intelligence Platform")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use database in production)
meetings = {}

class UploadResponse(BaseModel):
    meeting_id: str
    status: str

class StatusResponse(BaseModel):
    status: str
    progress: int

class MeetingDetails(BaseModel):
    meeting_id: str
    filename: str
    status: str
    transcript: Optional[str] = None
    action_items: Optional[List[dict]] = None
    decisions: Optional[List[dict]] = None
    participants: Optional[List[dict]] = None
    topics: Optional[List[str]] = None

@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload meeting recording file"""
    meeting_id = str(uuid.uuid4())
    
    # Create uploads directory if it doesn't exist
    os.makedirs("./uploads", exist_ok=True)
    
    # Save file
    file_path = f"./uploads/{meeting_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Store meeting info
    meetings[meeting_id] = {
        "meeting_id": meeting_id,
        "filename": file.filename,
        "status": "processing",
        "transcript": None,
        "action_items": None,
        "decisions": None,
        "participants": None,
        "topics": None
    }
    
    return UploadResponse(meeting_id=meeting_id, status="processing")

@app.get("/api/meetings/{meeting_id}/status", response_model=StatusResponse)
async def get_meeting_status(meeting_id: str):
    """Get meeting processing status"""
    if meeting_id not in meetings:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings[meeting_id]
    progress = 100 if meeting["status"] == "completed" else 50 if meeting["status"] == "processing" else 0
    
    # Simulate completion after first status check
    if meeting["status"] == "processing":
        # Simulate processing completion
        meetings[meeting_id]["status"] = "completed"
        meetings[meeting_id]["transcript"] = "This is a sample transcript from the meeting. Participants discussed various topics including project timelines, budget allocation, and team responsibilities. John mentioned that the marketing campaign needs to be completed by next Friday. Sarah will handle the client presentation. The team agreed to use the new software tool for project management."
        meetings[meeting_id]["action_items"] = [
            {"assignee": "John Smith", "task": "Complete marketing campaign", "deadline": "2023-12-15"},
            {"assignee": "Sarah Johnson", "task": "Prepare client presentation", "deadline": "2023-12-10"},
            {"assignee": "Mike Davis", "task": "Set up project management tool", "deadline": "2023-12-05"}
        ]
        meetings[meeting_id]["decisions"] = [
            {"decision": "Use new software tool for project management", "made_by": "Team consensus"},
            {"decision": "Allocate additional budget for marketing", "made_by": "Management"}
        ]
        meetings[meeting_id]["participants"] = [
            {"name": "John Smith", "role": "Marketing Lead"},
            {"name": "Sarah Johnson", "role": "Client Relations"},
            {"name": "Mike Davis", "role": "Technical Lead"}
        ]
        meetings[meeting_id]["topics"] = ["Project Timeline", "Budget Allocation", "Team Responsibilities", "Software Tools"]
        progress = 100
    
    return StatusResponse(status=meeting["status"], progress=progress)

@app.get("/api/meetings/{meeting_id}", response_model=MeetingDetails)
async def get_meeting_details(meeting_id: str):
    """Get meeting details and insights"""
    if meeting_id not in meetings:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings[meeting_id]
    return MeetingDetails(**meeting)

@app.get("/")
async def root():
    return {"message": "AI Meeting Intelligence Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)