# Game Jam Assistant Discord Bot - Design Document

## Project Overview

### Purpose
A Discord bot that assists game developers during game jams by generating creative game concepts, providing encouraging/sarcastic commentary, and tracking jam progress. The bot uses local AI to create unique, entertaining constraints and concepts that spark creativity.

### Target Audience
- Game developers participating in game jams
- Game development communities and Discord servers
- Teams looking for creative inspiration during time-constrained development

### Key Goals
1. Generate entertaining and challenging game concepts on demand
2. Provide personality-driven commentary that keeps morale high during jams
3. Be easy to deploy and run locally
4. Leverage local AI for creative, dynamic content generation

---

## Core Features

### Phase 1: MVP (Template-Based)
- `/generate-concept` - Generate random game concepts using template system
- `/generate-constraint` - Add an additional constraint to an existing concept
- `/help` - Show available commands and usage
- Basic constraint categories: Genre, Setting, Mechanic, Theme, Time Limit, Special Rule

### Phase 2: AI Integration
- Replace template system with Ollama-powered generation
- Context-aware concept generation (remembers server's preferred genres/styles)
- More creative and unexpected combinations
- Personality-driven responses (encouragement, sarcasm, developer humor)

### Phase 3: Progress Tracking
- `/start-jam` - Begin tracking a game jam with name and duration
- `/update-progress` - Log progress updates
- `/jam-status` - Check current jam status and time remaining
- Periodic check-ins with AI-generated commentary
- `/jam-complete` - Mark jam as complete and generate summary

### Future Enhancements
- Team management (assign roles, track individual contributions)
- Scoped jam tracking (per-channel or per-team)
- Integration with GitHub/GitLab for automatic progress detection
- Playtesting feedback collection
- Post-mortem generation

---

## Technical Architecture

### High-Level Design
```
┌─────────────────┐
│  Discord Server │
└────────┬────────┘
         │ Commands
         ▼
┌─────────────────┐
│   Discord Bot   │
│   (discord.py)  │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌─────────────┐  ┌──────────────┐
│   Ollama    │  │   SQLite DB  │
│  Local LLM  │  │  (Optional)  │
└─────────────┘  └──────────────┘
```

### Components

**Discord Bot (main.py)**
- Handles Discord events and commands
- Manages command routing
- Formats and sends responses
- Uses discord.py library

**Concept Generator (concept_generator.py)**
- Phase 1: Template-based random selection
- Phase 2: Ollama API integration for AI generation
- Handles constraint combinations
- Maintains prompt templates for AI

**Progress Tracker (progress_tracker.py)** *(Phase 3)*
- Tracks active jams per server/channel
- Stores progress updates
- Calculates time remaining
- Triggers periodic check-ins

**AI Interface (ai_interface.py)** *(Phase 2)*
- Abstracts Ollama API calls
- Manages prompt construction
- Handles AI response parsing
- Error handling and fallbacks

---

## Commands & User Interactions

### Phase 1 Commands

#### `/generate-concept`
**Description:** Generate a random game concept with constraints

**Usage:**
```
/generate-concept
```

**Example Output:**
```
🎮 Game Jam Concept Generator 🎮

Genre: Roguelike
Setting: Underwater research station
Core Mechanic: Time loop
Theme: Isolation
Special Constraint: No text or dialogue allowed
Time Limit: 48 hours

Good luck, you'll need it! 🎲
```

**Options (Optional Parameters):**
- `genre` - Specify a genre (platformer, rpg, puzzle, etc.)
- `difficulty` - Easy, Medium, Hard, Insane (affects number of constraints)

#### `/generate-constraint`
**Description:** Add one more constraint to your existing concept

**Usage:**
```
/generate-constraint
```

**Example Output:**
```
Additional Constraint: All game objects must be geometric shapes only (no sprites)

May the odds be ever in your favor... 📐
```

#### `/help`
**Description:** Display available commands and usage information

---

### Phase 2 Enhancements

All Phase 1 commands remain, but generation is powered by AI:

#### `/generate-concept` (Enhanced)
- AI creates more creative, thematically coherent combinations
- Generates explanatory text about why constraints work together
- Personality-driven delivery (encouraging, sarcastic, or neutral)

**Example AI Output:**
```
🎮 Game Jam Concept Generator 🎮

Make a rhythm-based survival horror game set in an abandoned music conservatory where sound attracts monsters. The twist? You can only move on the beat.

Why this works: The tension between needing to make noise (rhythm gameplay) while silence keeps you safe creates natural horror game tension. The conservatory setting provides both musical instruments as mechanics and creepy architectural spaces.

Time Limit: 72 hours
Difficulty: Medium

Now stop reading and start coding! ⏰
```

#### `/vibe-check`
**Description:** Get AI commentary on your current progress/mood

**Usage:**
```
/vibe-check [optional status text]
```

**Example:**
```
User: /vibe-check I've been stuck on this bug for 3 hours
Bot: Ah yes, the classic "this should take 5 minutes" bug that becomes a three-hour philosophical journey. 

Here's the thing - if you've been at it for 3 hours, you're probably overthinking it. Take a 10-minute break, get some water, then rubber duck debug it out loud. The bug is quaking in fear already. 🦆
```

---

### Phase 3 Commands

#### `/start-jam`
**Description:** Begin tracking a game jam

**Usage:**
```
/start-jam <name> <duration_hours>
```

**Example:**
```
/start-jam "Pirate Jam" 48
```

**Response:**
```
🏴‍☠️ Pirate Jam has begun! 🏴‍☠️

Duration: 48 hours
Ends: Saturday, December 21 at 3:00 PM EST

I'll check in periodically to see how you're drowning... I mean, doing! 

Use /update-progress to log your updates.
```

#### `/update-progress`
**Description:** Log a progress update

**Usage:**
```
/update-progress <message>
```

**Example:**
```
/update-progress Basic movement working, added jumping
```

**Response:**
```
Progress logged! ✅

Time elapsed: 6 hours / 48 hours (12.5%)
Last update: "Basic movement working, added jumping"

You're 12% through and already have movement? Either you're crushing it or you haven't hit the game-breaking bugs yet. I'm betting on the latter. 😏
```

#### `/jam-status`
**Description:** Check current jam progress

**Response includes:**
- Time remaining
- Progress updates history
- AI-generated motivational/sarcastic commentary based on progress

#### `/jam-complete`
**Description:** Mark jam as complete

**Response includes:**
- Final statistics (duration, number of updates)
- AI-generated post-jam summary
- Encouragement to share the game

---

## AI Integration Strategy

### Model Selection
**Recommended:** Ollama with `llama3.2:3b` or `mistral:7b`
- Fast inference on local hardware
- Good balance of creativity and coherence
- Handles personality well

### Prompt Design Approach

#### Concept Generation Prompt Template
```python
CONCEPT_GENERATION_PROMPT = """You are a creative game jam assistant helping developers come up with interesting game concepts.

Generate a unique game concept that includes:
- Genre
- Setting
- Core mechanic
- Theme
- One creative constraint that makes it more challenging/interesting

Make the constraints synergize in interesting ways. Be creative and unexpected, but keep the scope realistic for a {duration}-hour jam.

Tone: {tone} (encouraging/sarcastic/neutral)

Generate the concept now:"""
```

#### Commentary Prompt Template
```python
COMMENTARY_PROMPT = """You are a game jam assistant bot with personality. A developer just shared this update:

"{user_message}"

Time into jam: {hours_elapsed}/{total_hours} hours
Previous updates: {update_history}

Provide a brief (2-3 sentence) response that:
1. Acknowledges their progress
2. Provides light commentary (be {tone})
3. Keeps them motivated

Response:"""
```

### AI Integration Points

**Where AI adds value:**
1. **Concept Generation** - Creates unique, coherent combinations
2. **Constraint Addition** - Generates complementary constraints
3. **Progress Commentary** - Context-aware encouragement/humor
4. **Vibe Checks** - Reads developer mood and responds appropriately
5. **Post-Jam Summaries** - Narrative wrap-up of the jam experience

**Where AI isn't needed:**
1. Command parsing
2. Time tracking calculations
3. Data storage/retrieval
4. Basic status displays

### Fallback Strategy
If Ollama is unavailable:
- Fall back to template-based generation (Phase 1 functionality)
- Display error message suggesting user check Ollama status
- Cache last successful AI response as emergency backup

---

## Data Models

### Jam Session (Phase 3)
```python
class JamSession:
    id: str  # UUID
    server_id: str  # Discord server ID
    channel_id: str  # Discord channel ID
    name: str  # Jam name
    start_time: datetime
    duration_hours: int
    updates: List[ProgressUpdate]
    completed: bool
    completed_time: Optional[datetime]
```

### Progress Update (Phase 3)
```python
class ProgressUpdate:
    id: str  # UUID
    jam_id: str  # Foreign key to JamSession
    timestamp: datetime
    user_id: str  # Discord user ID
    message: str
    hours_elapsed: float
```

### User Preferences (Future)
```python
class UserPreferences:
    user_id: str
    preferred_tone: str  # "encouraging", "sarcastic", "neutral"
    favorite_genres: List[str]
    difficulty_preference: str  # "easy", "medium", "hard", "insane"
```

---

## Development Phases

### Phase 1: MVP Template System (Week 1)
**Goal:** Get a working bot that generates concepts without AI

**Tasks:**
1. Set up Discord bot project structure
2. Implement basic discord.py bot with command handling
3. Create template-based concept generator with categories:
   - Genres (20+ options)
   - Settings (30+ options)
   - Mechanics (25+ options)
   - Themes (20+ options)
   - Special Constraints (30+ options)
4. Implement `/generate-concept` command
5. Implement `/generate-constraint` command
6. Implement `/help` command
7. Test in Discord server

**Deliverable:** Working bot that can join server and generate concepts

---

### Phase 2: AI Integration (Week 2)
**Goal:** Replace templates with AI-generated content

**Tasks:**
1. Set up Ollama interface module
2. Create prompt templates for concept generation
3. Implement AI-powered `/generate-concept`
4. Test and refine prompts for consistency
5. Add personality/tone variations
6. Implement `/vibe-check` command
7. Add error handling and fallback to template system
8. Performance testing (response times)

**Deliverable:** Bot with AI-powered creative generation

---

### Phase 3: Progress Tracking (Week 3-4)
**Goal:** Add jam tracking and progress features

**Tasks:**
1. Set up SQLite database
2. Implement JamSession and ProgressUpdate models
3. Create database interface layer
4. Implement `/start-jam` command
5. Implement `/update-progress` command
6. Implement `/jam-status` command
7. Implement `/jam-complete` command
8. Add periodic check-in system (scheduled tasks)
9. Implement AI commentary for progress updates
10. Test multi-server isolation

**Deliverable:** Full-featured jam assistant bot

---

## Tech Stack

### Core Dependencies
```
python >= 3.10
discord.py >= 2.3.0
requests >= 2.31.0  # For Ollama API
python-dotenv >= 1.0.0  # Environment variables
```

### Phase 3 Additions
```
sqlite3 (built-in)
```

### Development Tools
```
black  # Code formatting
pylint  # Linting
pytest  # Testing (optional, for unit tests)
```

### Required External Services
- **Discord Developer Account** - Bot token and application setup
- **Ollama** - Running locally for AI features

---

## Project Structure

```
game-jam-assistant/
├── main.py                 # Entry point, bot initialization
├── config.py              # Configuration and constants
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
├── README.md             # Setup and usage instructions
│
├── cogs/                 # Discord.py cogs (command groups)
│   ├── __init__.py
│   ├── concept.py        # Concept generation commands
│   ├── jam_tracking.py   # Jam tracking commands (Phase 3)
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
├── database/            # Database layer (Phase 3)
│   ├── __init__.py
│   ├── models.py        # Data models
│   └── db_manager.py    # Database operations
│
└── utils/               # Utility functions
    ├── __init__.py
    └── formatters.py    # Message formatting helpers
```

---

## Setup and Deployment

### Prerequisites
1. Python 3.10 or higher installed
2. Discord account with access to developer portal
3. Ollama installed and running (for Phase 2+)

### Discord Bot Setup
1. Go to https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Navigate to "Bot" section
4. Click "Add Bot"
5. Enable these "Privileged Gateway Intents":
   - Message Content Intent
6. Copy the bot token (keep this secret!)
7. Navigate to "OAuth2" → "URL Generator"
8. Select scopes: `bot`, `applications.commands`
9. Select permissions: `Send Messages`, `Read Message History`, `Use Slash Commands`
10. Copy generated URL and use it to invite bot to your server

### Local Setup
1. Clone/download the project
2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Add your Discord bot token to `.env`:
```
DISCORD_TOKEN=your_token_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Ensure Ollama is running (Phase 2+):
```bash
ollama serve
ollama pull llama3.2:3b
```

6. Run the bot:
```bash
python main.py
```

### Running the Bot
- Simply execute `python main.py` in the project directory
- Bot will connect to Discord and register slash commands
- Keep the terminal window open while bot is running
- Press Ctrl+C to stop the bot

### Deployment Options
**Local Development:** Run on your development machine
**Always-On:** Run on a dedicated machine (like your Jetson AGX Orin)
**Process Manager:** Use `screen`, `tmux`, or `systemd` for background execution

---

## Configuration

### Environment Variables (.env)
```bash
# Required
DISCORD_TOKEN=your_discord_bot_token_here

# Ollama Configuration (Phase 2+)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Bot Configuration
BOT_PREFIX=!  # For legacy commands if needed
DEFAULT_TONE=encouraging  # encouraging, sarcastic, neutral

# Database (Phase 3)
DATABASE_PATH=./data/jam_assistant.db
```

### Constants (config.py)
```python
# Generation settings
MIN_CONSTRAINTS = 3
MAX_CONSTRAINTS = 7
DEFAULT_JAM_DURATION = 48  # hours

# AI settings
AI_TIMEOUT = 30  # seconds
AI_MAX_RETRIES = 3
ENABLE_AI_FALLBACK = True

# Check-in intervals (Phase 3)
CHECKIN_INTERVALS = [6, 12, 24, 36, 48]  # hours
```

---

## Testing Strategy

### Manual Testing Checklist (Phase 1)
- [ ] Bot connects to Discord successfully
- [ ] `/generate-concept` produces varied, interesting concepts
- [ ] `/generate-constraint` adds complementary constraints
- [ ] `/help` displays all commands correctly
- [ ] Bot handles multiple servers correctly
- [ ] Commands work in both channels and DMs

### AI Testing (Phase 2)
- [ ] AI generates coherent, creative concepts
- [ ] Tone variations work as expected
- [ ] Fallback to templates when Ollama unavailable
- [ ] Response times are acceptable (< 5 seconds)
- [ ] AI responses are appropriate and on-topic

### Database Testing (Phase 3)
- [ ] Jams can be started, tracked, and completed
- [ ] Progress updates persist correctly
- [ ] Multiple concurrent jams work independently
- [ ] Data survives bot restarts

---

## Future Considerations

### Performance Optimization
- Cache AI responses for similar requests
- Implement request queuing for multiple simultaneous commands
- Consider async AI calls to prevent blocking

### Feature Expansions
- Team collaboration features
- Integration with itch.io for submission tracking
- Post-jam analytics and insights
- Community voting on generated concepts
- Themed concept packs (horror games, cozy games, etc.)

### Scalability
- If bot becomes popular, consider:
  - Moving to cloud hosting
  - Implementing rate limiting
  - Using Redis for caching
  - Sharding for multiple servers

---

## Success Metrics

### Phase 1
- Bot successfully deploys to Discord
- Users can generate concepts reliably
- Concepts are entertaining and varied

### Phase 2
- AI responses feel more creative than templates
- Users prefer AI-generated concepts
- Response time remains under 5 seconds

### Phase 3
- Users complete tracked jams
- Progress tracking provides value
- AI commentary enhances the jam experience

---

## Appendix

### Example Template Categories (Phase 1)

**Genres:**
Platformer, Puzzle, RPG, Roguelike, Metroidvania, Visual Novel, Tower Defense, Card Game, Rhythm, Racing, Fighting, Stealth, Survival, Strategy, Adventure, Point-and-Click, Idle, Management, Simulation

**Settings:**
Space station, Medieval castle, Cyberpunk city, Underwater, Post-apocalyptic, Fantasy forest, Desert wasteland, Corporate office, Haunted mansion, School, Laboratory, Alien planet, Dream world, Tiny world (microscopic), Giant world (macro), Inside a computer, Ancient ruins

**Mechanics:**
Time loop, Gravity manipulation, Portal creation, Shape-shifting, Resource management, Dialogue choices, Crafting system, Permadeath, Procedural generation, Limited inventory, One-button control, Memory-based puzzles, Physics-based, Asymmetric multiplayer, Deck building

**Themes:**
Isolation, Friendship, Betrayal, Discovery, Loss, Growth, Rebellion, Mystery, Horror, Comedy, Nostalgia, Existential, Environmental, Political, Love, Fear, Hope, Greed

**Special Constraints:**
No text/dialogue, Only 3 colors, Everything is circles, One-button gameplay, No jumping, Reverse controls, Real-time only (no pause), All assets must be ASCII art, No sound effects, Enemies are friendly, You play as the environment, Speed increases constantly, Everything moves in slow motion

### Useful Discord.py Resources
- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [discord.py Examples](https://github.com/Rapptz/discord.py/tree/master/examples)

### Ollama Resources
- [Ollama Documentation](https://ollama.ai/docs)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Model Library](https://ollama.ai/library)

---

## Version History

- **v0.1** - Initial design document
- **v1.0** - Phase 1 completion (template system)
- **v2.0** - Phase 2 completion (AI integration)
- **v3.0** - Phase 3 completion (progress tracking)

