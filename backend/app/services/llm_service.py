import json
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings

class LLMService:
    """
    Smart LLM service that routes between Ollama (local) and Groq (cloud).
    
    Priority:
    1. Try Ollama locally (free, private)
    2. Fallback to Groq (free tier available)
    """
    
    def __init__(self):
        self.ollama_url = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.groq_api_key = settings.GROQ_API_KEY
        self.groq_model = settings.GROQ_MODEL
        self.active_provider = None
    
    async def check_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Ollama not available: {str(e)}")
            return False
    
    async def get_active_provider(self) -> str:
        """Determine which LLM provider to use"""
        if settings.LLM_PROVIDER == "ollama":
            return "ollama"
        elif settings.LLM_PROVIDER == "groq":
            return "groq"
        
        # Auto mode: try Ollama first
        if await self.check_ollama_available():
            self.active_provider = "ollama"
            print("✅ Using Ollama (local)")
            return "ollama"
        
        # Fallback to Groq
        if self.groq_api_key:
            self.active_provider = "groq"
            print("✅ Using Groq (cloud fallback)")
            return "groq"
        
        raise Exception("No LLM available! Install Ollama or set GROQ_API_KEY")
    
    async def _ollama_summarize(self, transcript: str) -> Dict[str, Any]:
        """Use Ollama for summarization"""
        prompt = f"""Analyze this meeting transcript and provide:

1. A brief 2-3 sentence summary
2. Key points (3-5 items)
3. Action items (with owner if mentioned)
4. Main topics discussed

Format as JSON with these exact keys: summary, key_points, action_items, topics

Transcript:
{transcript}

Respond ONLY with valid JSON, no markdown."""
        
        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    response_text = result.get("response", "")
                    
                    # Parse JSON from response
                    try:
                        if "{" in response_text and "}" in response_text:
                            json_start = response_text.find("{")
                            json_end = response_text.rfind("}") + 1
                            json_str = response_text[json_start:json_end]
                            return json.loads(json_str)
                    except:
                        pass
                    
                    # Fallback structure
                    return {
                        "summary": response_text[:500],
                        "key_points": ["Meeting analysis complete"],
                        "action_items": [],
                        "topics": ["General Discussion"]
                    }
                else:
                    raise Exception(f"Ollama error: {response.status_code}")
        except Exception as e:
            print(f"❌ Ollama error: {str(e)}")
            raise
    
    async def _groq_summarize(self, transcript: str) -> Dict[str, Any]:
        """Use Groq for summarization"""
        from groq import Groq
        
        prompt = f"""Analyze this meeting transcript and provide:

1. A brief 2-3 sentence summary
2. Key points (3-5 items)
3. Action items (with owner if mentioned)
4. Main topics discussed

Format as JSON with these exact keys: summary, key_points, action_items, topics

Transcript:
{transcript}

Respond ONLY with valid JSON."""
        
        try:
            client = Groq(api_key=self.groq_api_key)
            message = client.chat.completions.create(
                model=self.groq_model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.choices[0].message.content
            
            # Parse JSON from response
            try:
                if "{" in response_text and "}" in response_text:
                    json_start = response_text.find("{")
                    json_end = response_text.rfind("}") + 1
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except:
                pass
            
            # Fallback
            return {
                "summary": response_text[:500],
                "key_points": ["Meeting analysis complete"],
                "action_items": [],
                "topics": ["General Discussion"]
            }
        except Exception as e:
            print(f"❌ Groq error: {str(e)}")
            raise
    
    async def summarize(self, transcript: str) -> Dict[str, Any]:
        """
        Summarize transcript using best available LLM.
        Tries Ollama first, falls back to Groq.
        """
        provider = await self.get_active_provider()
        
        if provider == "ollama":
            try:
                return await self._ollama_summarize(transcript)
            except Exception as e:
                print(f"⚠️  Ollama failed, trying Groq: {str(e)}")
                if self.groq_api_key:
                    return await self._groq_summarize(transcript)
                raise
        else:
            return await self._groq_summarize(transcript)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current LLM status"""
        ollama_available = await self.check_ollama_available()
        groq_available = bool(self.groq_api_key)
        
        provider = await self.get_active_provider()
        
        return {
            "active_provider": provider,
            "ollama_available": ollama_available,
            "groq_available": groq_available,
            "ollama_model": self.ollama_model if ollama_available else None,
            "groq_model": self.groq_model if groq_available else None,
        }


# Global instance
llm_service = LLMService()
