from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class MeetingBase(BaseModel):
    filename: str

class MeetingCreate(MeetingBase):
    meeting_id: str

class MeetingResponse(MeetingBase):
    id: int
    meeting_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class MeetingDetailsResponse(MeetingResponse):
    transcript: Optional[str] = None
    action_items: Optional[List[Dict[str, Any]]] = None
    decisions: Optional[List[Dict[str, Any]]] = None
    participants: Optional[List[Dict[str, Any]]] = None
    topics: Optional[List[str]] = None

class UploadResponse(BaseModel):
    meeting_id: str
    status: str

class StatusResponse(BaseModel):
    status: str
    progress: int

class SearchRequest(BaseModel):
    query: str
    meeting_id: Optional[str] = None

class SearchResult(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    distance: float

class SearchResponse(BaseModel):
    results: List[SearchResult]