# Game Jam Assistant Discord Bot

A Discord bot that assists game developers during game jams by generating creative game concepts, providing encouraging/sarcastic commentary, and tracking jam progress. The bot uses local AI (Ollama) to create unique, entertaining constraints and concepts that spark creativity.

## Features

### Phase 1: Template-Based Generation
- `/generate-concept` - Generate random game concepts using template system
- `/generate-constraint` - Add an additional constraint to an existing concept
- `/help` - Show available commands and usage

### Phase 2: AI Integration
- AI-powered concept generation with Ollama
- Context-aware concept generation
- Personality-driven responses (encouragement, sarcasm, developer humor)
- `/vibe-check` - Get AI commentary on your current progress/mood
- Automatic fallback to template system if AI is unavailable

## Prerequisites

1. **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
2. **Discord Developer Account** - [Discord Developer Portal](https://discord.com/developers/applications)
3. **Ollama** (for Phase 2 AI features) - [Install Ollama](https://ollama.ai/)

## Setup

### 1. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Game Jam Assistant")
3. Navigate to the "Bot" section
4. Click "Add Bot"
5. Enable these "Privileged Gateway Intents":
   - ✅ Message Content Intent
6. Copy the bot token (keep this secret!)
7. Navigate to "OAuth2" → "URL Generator"
8. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
9. Select permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Slash Commands
10. Copy the generated URL and use it to invite the bot to your server

### 2. Local Setup

1. **Clone or download this project**

2. **Create a `.env` file** in the project root:
   ```bash
   # Copy the example (if available) or create manually
   ```

3. **Add your Discord bot token to `.env`**:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2:3b
   DEFAULT_TONE=encouraging
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Ollama** (for Phase 2 AI features):
   ```bash
   # Install Ollama from https://ollama.ai/
   # Then pull a model:
   ollama pull llama3.2:3b
   # Or use mistral:
   ollama pull mistral:7b
   ```

6. **Run the bot**:
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables (.env)

```env
# Required
DISCORD_TOKEN=your_discord_bot_token_here

# Ollama Configuration (Phase 2+)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Bot Configuration
BOT_PREFIX=!
DEFAULT_TONE=encouraging  # encouraging, sarcastic, neutral

# Database (Phase 3 - not yet implemented)
DATABASE_PATH=./data/jam_assistant.db
```

### Config Constants (config.py)

You can modify these constants in `config.py`:
- `MIN_CONSTRAINTS = 3` - Minimum constraints per concept
- `MAX_CONSTRAINTS = 7` - Maximum constraints per concept
- `AI_TIMEOUT = 30` - AI request timeout in seconds
- `AI_MAX_RETRIES = 3` - Number of retry attempts for AI calls
- `ENABLE_AI_FALLBACK = True` - Fallback to templates if AI fails

## Usage

### Commands

#### `/generate-concept [genre] [difficulty]`
Generate a random game concept with constraints.

**Options:**
- `genre` (optional) - Specify a genre (platformer, rpg, puzzle, etc.)
- `difficulty` (optional) - Easy, Medium, Hard, or Insane

**Example:**
```
/generate-concept genre:platformer difficulty:hard
```

#### `/generate-constraint`
Add one more constraint to your existing concept.

**Example:**
```
/generate-constraint
```

#### `/vibe-check [message]`
Get AI commentary on your current progress/mood.

**Options:**
- `message` (optional) - Your current status or situation

**Example:**
```
/vibe-check message:I've been stuck on this bug for 3 hours
```

#### `/help`
Show available commands and usage information.

## Project Structure

```
game-jam-assistant/
├── main.py                 # Entry point, bot initialization
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
│
├── cogs/                  # Discord.py cogs (command groups)
│   ├── __init__.py
│   ├── concept.py        # Concept generation commands
│   └── utility.py        # Help and utility commands
│
├── generators/           # Generation logic
│   ├── __init__.py
│   ├── template_generator.py  # Phase 1 template system
│   └── ai_generator.py        # Phase 2 AI generation
│
├── ai/                   # AI integration
│   ├── __init__.py
│   ├── ollama_client.py  # Ollama API interface
│   └── prompts.py        # Prompt templates
│
└── utils/               # Utility functions
    ├── __init__.py
    └── formatters.py    # Message formatting helpers
```

## Troubleshooting

### Bot won't connect
- Check that `DISCORD_TOKEN` is set correctly in `.env`
- Verify the token hasn't been regenerated in Discord Developer Portal
- Check that the bot has the correct intents enabled

### AI features not working
- Ensure Ollama is running: `ollama serve`
- Verify the model is installed: `ollama list`
- Check `OLLAMA_BASE_URL` in `.env` matches your Ollama setup
- The bot will automatically fall back to template generation if AI is unavailable

### Commands not appearing
- Wait a few minutes after starting the bot for commands to sync
- Try restarting the bot
- Check that the bot has "Use Slash Commands" permission in your server

## Development

### Running in Development
```bash
python main.py
```

### Logs
The bot logs to both `bot.log` file and console output.

### Testing
Test commands in your Discord server or use Discord's test mode.

## Future Enhancements (Phase 3)

- `/start-jam` - Begin tracking a game jam
- `/update-progress` - Log progress updates
- `/jam-status` - Check current jam status
- `/jam-complete` - Mark jam as complete
- Periodic check-ins with AI-generated commentary

## License

This project is open source. Feel free to modify and use as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the design document (`game-jam-assistant-design.md`)
3. Check Discord.py and Ollama documentation

## Credits

Built with:
- [discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [Ollama](https://ollama.ai/) - Local LLM inference
- Python 3.10+

