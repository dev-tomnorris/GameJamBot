"""Configuration constants and settings for the Game Jam Assistant bot."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN must be set in .env file")

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# Bot Configuration
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
DEFAULT_TONE = os.getenv("DEFAULT_TONE", "encouraging")

# Database Configuration (Phase 3)
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/jam_assistant.db")

# Generation Settings
MIN_CONSTRAINTS = 3
MAX_CONSTRAINTS = 7
DEFAULT_JAM_DURATION = 48  # hours

# AI Settings
AI_TIMEOUT = 30  # seconds
AI_MAX_RETRIES = 3
ENABLE_AI_FALLBACK = True

# Check-in Intervals (Phase 3)
CHECKIN_INTERVALS = [6, 12, 24, 36, 48]  # hours

