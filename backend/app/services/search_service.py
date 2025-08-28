from typing import List
from ai.search.chroma_client import search_client

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def store_meeting_vectors(meeting_id: str, transcript: str):
    """Store meeting transcript in vector database"""
    chunks = chunk_text(transcript)
    search_client.add_documents(meeting_id, chunks)

def search_meeting_content(query: str, meeting_id: str = None):
    """Search meeting content"""
    return search_client.search(query, meeting_id)