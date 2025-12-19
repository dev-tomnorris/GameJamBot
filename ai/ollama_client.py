"""Ollama API client for AI-powered generation."""

import logging
import requests
from typing import Optional
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, AI_TIMEOUT, AI_MAX_RETRIES

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_url = f"{self.base_url}/api/generate"
    
    def is_available(self) -> bool:
        """
        Check if Ollama service is available.
        
        Returns:
            True if Ollama is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        timeout: int = AI_TIMEOUT
    ) -> Optional[str]:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: The prompt to send to the model
            model: Model to use (defaults to configured model)
            timeout: Request timeout in seconds
        
        Returns:
            Generated text, or None if generation failed
        """
        model = model or self.model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        # Retry logic
        last_error = None
        for attempt in range(AI_MAX_RETRIES):
            try:
                logger.debug(f"Ollama API call (attempt {attempt + 1}/{AI_MAX_RETRIES})")
                response = requests.post(
                    self.api_url,
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "").strip()
                    
                    if generated_text:
                        logger.debug("Ollama generation successful")
                        return generated_text
                    else:
                        logger.warning("Ollama returned empty response")
                        return None
                else:
                    error_msg = f"Ollama API returned status {response.status_code}: {response.text}"
                    logger.warning(error_msg)
                    last_error = error_msg
            
            except requests.exceptions.Timeout:
                logger.warning(f"Ollama request timed out (attempt {attempt + 1}/{AI_MAX_RETRIES})")
                last_error = "Request timeout"
            
            except requests.exceptions.ConnectionError:
                logger.warning(f"Ollama connection error (attempt {attempt + 1}/{AI_MAX_RETRIES})")
                last_error = "Connection error"
            
            except Exception as e:
                logger.error(f"Unexpected error in Ollama API call: {e}", exc_info=True)
                last_error = str(e)
        
        logger.error(f"Ollama generation failed after {AI_MAX_RETRIES} attempts: {last_error}")
        return None


# Global instance
ollama_client = OllamaClient()

