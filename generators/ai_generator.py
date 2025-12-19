"""AI-powered game concept generator with template fallback."""

import logging
import re
from typing import Dict, Optional
from ai.ollama_client import ollama_client
from ai import prompts
from generators.template_generator import template_generator
from config import DEFAULT_TONE, ENABLE_AI_FALLBACK

logger = logging.getLogger(__name__)


class AIGenerator:
    """Generates game concepts using AI with template fallback."""
    
    def __init__(self):
        self.ollama = ollama_client
        self.template_gen = template_generator
    
    def generate_concept(
        self,
        genre: Optional[str] = None,
        difficulty: str = "medium",
        tone: str = None
    ) -> Dict[str, str]:
        """
        Generate a game concept using AI, with template fallback.
        
        Args:
            genre: Optional specific genre
            difficulty: Difficulty level
            tone: Response tone (defaults to configured tone)
        
        Returns:
            Dictionary containing concept fields
        """
        tone = tone or DEFAULT_TONE
        
        # Check if AI is available
        if not self.ollama.is_available():
            logger.info("Ollama not available, using template generator")
            if ENABLE_AI_FALLBACK:
                return self.template_gen.generate_concept(genre=genre, difficulty=difficulty)
            else:
                return {"error": "AI service unavailable"}
        
        try:
            # Generate prompt
            duration = 48  # Default duration
            prompt = prompts.format_concept_prompt(
                duration=duration,
                tone=tone,
                genre=genre
            )
            
            # Call AI
            logger.debug("Generating concept with AI")
            response = self.ollama.generate(prompt)
            
            if response:
                # Parse AI response into concept dict
                concept = self._parse_ai_concept(response, genre, difficulty, tone, duration)
                return concept
            else:
                logger.warning("AI generation returned None, falling back to template")
                if ENABLE_AI_FALLBACK:
                    return self.template_gen.generate_concept(genre=genre, difficulty=difficulty)
                else:
                    return {"error": "AI generation failed"}
        
        except Exception as e:
            logger.error(f"Error in AI concept generation: {e}", exc_info=True)
            if ENABLE_AI_FALLBACK:
                logger.info("Falling back to template generator")
                return self.template_gen.generate_concept(genre=genre, difficulty=difficulty)
            else:
                return {"error": f"Generation error: {str(e)}"}
    
    def generate_constraint(
        self,
        existing_concept: Optional[str] = None,
        tone: str = None
    ) -> str:
        """
        Generate an additional constraint using AI, with template fallback.
        
        Args:
            existing_concept: Description of existing concept (optional)
            tone: Response tone
        
        Returns:
            Constraint string
        """
        tone = tone or DEFAULT_TONE
        
        # Check if AI is available
        if not self.ollama.is_available():
            logger.info("Ollama not available, using template generator")
            if ENABLE_AI_FALLBACK:
                return self.template_gen.generate_additional_constraint()
            else:
                return "AI service unavailable"
        
        try:
            # If no existing concept provided, use a generic one
            if not existing_concept:
                existing_concept = "A game jam project in progress"
            
            prompt = prompts.format_constraint_prompt(
                existing_concept=existing_concept,
                tone=tone
            )
            
            logger.debug("Generating constraint with AI")
            response = self.ollama.generate(prompt)
            
            if response:
                # Clean up the response
                constraint = response.strip()
                # Remove quotes if present
                constraint = constraint.strip('"\'')
                return constraint
            else:
                logger.warning("AI constraint generation failed, using template")
                if ENABLE_AI_FALLBACK:
                    return self.template_gen.generate_additional_constraint()
                else:
                    return "AI generation failed"
        
        except Exception as e:
            logger.error(f"Error in AI constraint generation: {e}", exc_info=True)
            if ENABLE_AI_FALLBACK:
                return self.template_gen.generate_additional_constraint()
            else:
                return f"Generation error: {str(e)}"
    
    def generate_commentary(
        self,
        user_message: str,
        context_info: str = "",
        tone: str = None
    ) -> str:
        """
        Generate AI commentary on user progress/mood.
        
        Args:
            user_message: User's message/update
            context_info: Additional context (time elapsed, etc.)
            tone: Response tone
        
        Returns:
            Commentary string
        """
        tone = tone or DEFAULT_TONE
        
        # Check if AI is available
        if not self.ollama.is_available():
            logger.warning("Ollama not available for commentary")
            return "AI service unavailable. Keep up the great work!"
        
        try:
            prompt = prompts.format_commentary_prompt(
                user_message=user_message,
                context_info=context_info,
                tone=tone
            )
            
            logger.debug("Generating commentary with AI")
            response = self.ollama.generate(prompt)
            
            if response:
                return response.strip()
            else:
                return "Keep pushing forward! You've got this! 💪"
        
        except Exception as e:
            logger.error(f"Error in AI commentary generation: {e}", exc_info=True)
            return "Keep up the great work! 🚀"
    
    def generate_vibe_check(
        self,
        user_message: str = "",
        tone: str = None
    ) -> str:
        """
        Generate AI response for vibe check command.
        
        Args:
            user_message: User's status message (optional)
            tone: Response tone
        
        Returns:
            Vibe check response string
        """
        tone = tone or DEFAULT_TONE
        
        # Check if AI is available
        if not self.ollama.is_available():
            logger.warning("Ollama not available for vibe check")
            return "AI service unavailable, but I'm here to cheer you on! 🎮"
        
        try:
            prompt = prompts.format_vibe_check_prompt(
                user_message=user_message or "Just checking in",
                tone=tone
            )
            
            logger.debug("Generating vibe check with AI")
            response = self.ollama.generate(prompt)
            
            if response:
                return response.strip()
            else:
                return "You're doing great! Keep it up! 💪"
        
        except Exception as e:
            logger.error(f"Error in AI vibe check generation: {e}", exc_info=True)
            return "Stay strong and keep coding! 🚀"
    
    def _parse_ai_concept(
        self,
        response: str,
        genre: Optional[str],
        difficulty: str,
        tone: str,
        duration: int
    ) -> Dict[str, str]:
        """
        Parse AI response into structured concept dictionary.
        
        Args:
            response: AI-generated text
            genre: Genre if specified
            difficulty: Difficulty level
            tone: Response tone
            duration: Jam duration
        
        Returns:
            Concept dictionary
        """
        # Try to extract structured information, but also preserve the full description
        concept = {
            "description": response,
            "difficulty": difficulty,
            "time_limit": str(duration),
            "is_ai": True
        }
        
        # Try to extract genre if mentioned
        if genre:
            concept["genre"] = genre
        else:
            # Try to find genre in response
            for g in template_generator.genres:
                if g.lower() in response.lower():
                    concept["genre"] = g
                    break
        
        # Try to extract explanation if present
        explanation_keywords = ["why", "because", "this works", "synergy", "interesting"]
        sentences = response.split('.')
        explanation_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in explanation_keywords):
                explanation_sentences.append(sentence.strip())
        
        if explanation_sentences:
            concept["explanation"] = " ".join(explanation_sentences)
        
        return concept


# Global instance
ai_generator = AIGenerator()

