import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings with Ollama + Groq support"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_TITLE: str = "MeetingMind API"
    API_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./meetings.db")
    
    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto")  # auto, ollama, groq
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama2-70b-4096")
    
    # Audio Processing
    MAX_AUDIO_SIZE_MB: int = int(os.getenv("MAX_AUDIO_SIZE_MB", "50"))
    SUPPORTED_FORMATS: list = os.getenv("SUPPORTED_FORMATS", "mp3,wav,m4a,ogg").split(",")
    
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Features
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    def validate(self):
        """Validate required settings"""
        if self.LLM_PROVIDER == "auto":
            if not self.GROQ_API_KEY:
                print("⚠️  Warning: GROQ_API_KEY not set. Ollama must be running for fallback.")
        elif self.LLM_PROVIDER == "groq":
            if not self.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY required when LLM_PROVIDER=groq")

settings = Settings()
settings.validate()
