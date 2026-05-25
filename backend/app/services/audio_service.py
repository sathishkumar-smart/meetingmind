import os
from pathlib import Path
from typing import Tuple

from app.core.config import settings


class AudioService:
    """Service for audio processing"""

    UPLOAD_DIR = Path("uploads/audio")

    def __init__(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def validate_audio_file(self, filename: str, file_size_bytes: int) -> Tuple[bool, str]:
        """Validate audio file format and size"""
        max_size_bytes = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
        if file_size_bytes > max_size_bytes:
            return False, f"File too large. Max {settings.MAX_AUDIO_SIZE_MB}MB allowed"

        ext = Path(filename).suffix.lower().lstrip(".")
        if ext not in settings.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(settings.SUPPORTED_FORMATS)}"

        return True, "Valid"

    def save_audio_file(self, file_content: bytes, filename: str) -> str:
        """Save uploaded audio file"""
        file_path = self.UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            f.write(file_content)
        return str(file_path)

    def get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration using librosa"""
        try:
            import librosa
            duration = librosa.get_duration(filename=audio_path)
            return float(duration)
        except Exception as e:
            print(f"⚠️  Could not read duration: {e}")
            return 0.0

    async def transcribe_audio(self, audio_path: str) -> Tuple[str, int]:
        """Transcribe audio using Whisper"""
        try:
            import whisper
            
            # Load Whisper model
            model = whisper.load_model("base")
            
            # Transcribe
            result = model.transcribe(audio_path, language="en")
            
            transcript = result["text"]
            word_count = len(transcript.split())
            
            return transcript, word_count
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            raise
    
    def cleanup_audio_file(self, file_path: str) -> bool:
        """Delete audio file after processing"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
