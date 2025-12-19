"""Main entry point for the Game Jam Assistant Discord bot."""

import asyncio
import logging
import sys
import discord
from discord.ext import commands
from config import DISCORD_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class GameJamBot(commands.Bot):
    """Main bot class for Game Jam Assistant."""
    
    def __init__(self):
        # Set up intents
        # Note: We only need default intents for slash commands
        # Message Content Intent is not needed for slash commands
        intents = discord.Intents.default()
        # intents.message_content = True  # Not needed for slash commands only
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None  # We have our own help command
        )
    
    async def setup_hook(self):
        """Called when the bot is starting up."""
        logger.info("Loading cogs...")
        
        # Load cogs
        try:
            await self.load_extension("cogs.utility")
            logger.info("Loaded utility cog")
        except Exception as e:
            logger.error(f"Failed to load utility cog: {e}")
        
        try:
            await self.load_extension("cogs.concept")
            logger.info("Loaded concept cog")
        except Exception as e:
            logger.error(f"Failed to load concept cog: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        logger.info(f"Bot is ready! Logged in as {self.user}")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Connected to {len(self.guilds)} server(s)")
        
        # Set bot status
        activity = discord.Game(name="Game Jams | /help")
        await self.change_presence(activity=activity)
    
    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a new server."""
        logger.info(f"Joined new server: {guild.name} (ID: {guild.id})")
    
    async def on_guild_remove(self, guild: discord.Guild):
        """Called when the bot leaves a server."""
        logger.info(f"Left server: {guild.name} (ID: {guild.id})")
    
    async def on_error(self, event, *args, **kwargs):
        """Global error handler."""
        logger.error(f"Error in event {event}: {args}, {kwargs}", exc_info=True)


async def main():
    """Main async function to run the bot."""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please create a .env file with your Discord bot token.")
        sys.exit(1)
    
    bot = GameJamBot()
    
    try:
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        await bot.close()
        logger.info("Bot closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown complete")

