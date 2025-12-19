"""Concept generation commands for the Game Jam Assistant bot."""

import discord
from discord import app_commands
from discord.ext import commands
from generators.ai_generator import ai_generator
from config import DEFAULT_TONE
from utils.formatters import format_concept_message, format_constraint_message


class ConceptCog(commands.Cog):
    """Commands for generating game concepts and constraints."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
        name="generate-concept",
        description="Generate a random game concept with constraints"
    )
    @app_commands.describe(
        genre="Specify a genre (platformer, rpg, puzzle, etc.)",
        difficulty="Difficulty level: Easy, Medium, Hard, or Insane"
    )
    async def generate_concept(
        self,
        interaction: discord.Interaction,
        genre: str = None,
        difficulty: str = "medium"
    ):
        """Generate a game concept with constraints."""
        # Validate difficulty
        valid_difficulties = ["easy", "medium", "hard", "insane"]
        if difficulty.lower() not in valid_difficulties:
            difficulty = "medium"
        
        # Defer response since AI generation may take time
        await interaction.response.defer()
        
        try:
            # Generate concept using AI generator (with template fallback)
            concept = ai_generator.generate_concept(
                genre=genre,
                difficulty=difficulty,
                tone=DEFAULT_TONE
            )
            
            # Check for errors
            if "error" in concept:
                await interaction.followup.send(
                    f"❌ {concept['error']}\n\nFalling back to template generation...",
                    ephemeral=True
                )
                return
            
            # Determine if this is AI-generated
            is_ai = concept.get("is_ai", False)
            
            # Format and send message
            message = format_concept_message(concept, is_ai=is_ai)
            await interaction.followup.send(message)
        
        except Exception as e:
            error_msg = f"Failed to generate concept: {str(e)}"
            await interaction.followup.send(error_msg, ephemeral=True)
    
    @app_commands.command(
        name="generate-constraint",
        description="Add one more constraint to your existing concept"
    )
    async def generate_constraint(self, interaction: discord.Interaction):
        """Generate an additional constraint."""
        # Defer response since AI generation may take time
        await interaction.response.defer()
        
        try:
            # Generate constraint using AI generator (with template fallback)
            constraint = ai_generator.generate_constraint(tone=DEFAULT_TONE)
            
            if not constraint or constraint.startswith("AI"):
                # Fallback to template if AI failed
                from generators.template_generator import template_generator
                constraint = template_generator.generate_additional_constraint()
            
            message = format_constraint_message(constraint)
            await interaction.followup.send(message)
        
        except Exception as e:
            error_msg = f"Failed to generate constraint: {str(e)}"
            await interaction.followup.send(error_msg, ephemeral=True)
    
    @app_commands.command(
        name="vibe-check",
        description="Get AI commentary on your current progress/mood"
    )
    @app_commands.describe(
        message="Your current status or situation (optional)"
    )
    async def vibe_check(
        self,
        interaction: discord.Interaction,
        message: str = ""
    ):
        """Get AI commentary on current progress/mood."""
        # Defer response since AI generation may take time
        await interaction.response.defer()
        
        try:
            # Generate vibe check response using AI
            response = ai_generator.generate_vibe_check(
                user_message=message,
                tone=DEFAULT_TONE
            )
            
            await interaction.followup.send(response)
        
        except Exception as e:
            error_msg = f"Failed to generate vibe check: {str(e)}"
            await interaction.followup.send(error_msg, ephemeral=True)


async def setup(bot: commands.Bot):
    """Setup function for loading the cog."""
    await bot.add_cog(ConceptCog(bot))

