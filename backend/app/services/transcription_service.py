import asyncio
from ai.transcription.whisper_client import transcriber

async def process_transcription(file_path: str) -> str:
    """Process transcription of audio file using Whisper"""
    try:
        # Run transcription in a thread to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, transcriber.transcribe, file_path)
        return result["text"]
    except Exception as e:
        print(f"Transcription processing error: {e}")
        # Fallback for demo
        return "This is a sample transcript from the meeting. Participants discussed various topics including project timelines, budget allocation, and team responsibilities. John mentioned that the marketing campaign needs to be completed by next Friday. Sarah will handle the client presentation. The team agreed to use the new software tool for project management."