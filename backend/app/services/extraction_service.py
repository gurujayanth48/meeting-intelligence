import asyncio
from ai.extraction.llm_client import extract_meeting_insights

async def process_extraction(transcript: str) -> dict:
    """Process extraction of insights from transcript"""
    # Simulate processing time
    await asyncio.sleep(3)
    
    return extract_meeting_insights(transcript)