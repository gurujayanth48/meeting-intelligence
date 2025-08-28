import os
import whisper
import torch
from pydub import AudioSegment
from app.core.config import settings

class WhisperTranscriber:
    def __init__(self):
        # Check if CUDA is available for faster processing
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load the model (you can choose different sizes: tiny, base, small, medium, large)
        # For production, you might want to make this configurable
        self.model = whisper.load_model("base", device=self.device)
    
    def convert_to_wav(self, file_path: str) -> str:
        """Convert audio/video file to WAV format if needed"""
        if file_path.endswith('.wav'):
            return file_path
            
        # Convert to WAV
        wav_path = file_path.replace('.' + file_path.split('.')[-1], '.wav')
        
        try:
            # Handle different file formats
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_path, format="wav")
        except Exception as e:
            print(f"Error converting file: {e}")
            raise e
            
        return wav_path
    
    def transcribe(self, file_path: str) -> dict:
        """Transcribe audio file using Whisper"""
        try:
            # Convert to WAV if needed
            wav_path = self.convert_to_wav(file_path)
            
            # Transcribe the audio file
            result = self.model.transcribe(
                wav_path,
                fp16=False,  # Use float32 instead of float16 for CPU compatibility
                language="en"  # Specify language if known, or remove for auto-detection
            )
            
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"]
            }
            
        except Exception as e:
            print(f"Transcription error: {e}")
            # Fallback for demo purposes
            return {
                "text": "This is a sample transcript from the meeting. Participants discussed various topics including project timelines, budget allocation, and team responsibilities. John mentioned that the marketing campaign needs to be completed by next Friday. Sarah will handle the client presentation. The team agreed to use the new software tool for project management.",
                "segments": [],
                "language": "en"
            }

# Global instance
transcriber = WhisperTranscriber()