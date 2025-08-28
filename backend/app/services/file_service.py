import os
import uuid
from typing import Tuple
from app.core.config import settings
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

def save_uploaded_file(file, meeting_id: str) -> str:
    """Save uploaded file and return file path"""
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    file_extension = file.filename.split('.')[-1]
    file_path = os.path.join(settings.UPLOAD_DIR, f"{meeting_id}.{file_extension}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path

def is_video_file(file_path: str) -> bool:
    """Check if file is a video"""
    video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']
    extension = file_path.split('.')[-1].lower()
    return extension in video_extensions

def extract_audio_from_video(video_path: str) -> str:
    """Extract audio from video file"""
    audio_path = video_path.replace('.' + video_path.split('.')[-1], '.wav')
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    return audio_path

def segment_audio(audio_path: str, max_duration: int = 300) -> list:
    """Segment audio file into chunks"""
    audio = AudioSegment.from_file(audio_path)
    segments = []
    
    for i, chunk in enumerate(audio[::max_duration * 1000]):
        segment_path = audio_path.replace('.wav', f'_segment_{i}.wav')
        chunk.export(segment_path, format="wav")
        segments.append(segment_path)
    
    return segments