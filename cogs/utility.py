"""Utility commands for the Game Jam Assistant bot."""

import discord
from discord import app_commands
from discord.ext import commands
from utils.formatters import format_help_message


class UtilityCog(commands.Cog):
    """Utility commands including help."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Show available commands and usage information")
    async def help_command(self, interaction: discord.Interaction):
        """Display help message with all available commands."""
        help_text = format_help_message()
        await interaction.response.send_message(help_text)


async def setup(bot: commands.Bot):
    """Setup function for loading the cog."""
    await bot.add_cog(UtilityCog(bot))

