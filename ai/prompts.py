"""Prompt templates for AI generation."""


CONCEPT_GENERATION_PROMPT = """You are a creative game jam assistant helping developers come up with interesting game concepts.

Generate a unique game concept in this EXACT format:

Genre: [genre name]
Setting: [setting description]
Core Mechanic: [brief, open-ended mechanic - keep it concise, 2-5 words max]
Theme: [theme/tone]
Special Constraint: [one creative constraint]

Guidelines:
- Core Mechanic should be brief and open-ended (e.g., "Time manipulation", "Gravity switching", "Resource trading") - give developers creative freedom
- Be CREATIVE and UNEXPECTED - don't limit yourself to common genres, settings, or mechanics. Think outside the box!
- AVOID repetitive settings - vary your settings significantly. Don't repeatedly use libraries, bookstores, or similar knowledge-based locations. Explore diverse environments!
- Genres can be unique combinations or new concepts (e.g., "Rhythm-based Metroidvania", "Cozy Horror", "Reverse Tower Defense")
- Settings should be diverse and creative (e.g., "Inside a living organism", "A world made of sound", "A collapsing space station", "A city that rebuilds itself daily", "The space between thoughts", "A factory that produces emotions", "An ocean of clouds")
- Mechanics should be innovative and open-ended to spark creativity
- Themes can be abstract or unique (e.g., "Impermanence", "Miscommunication", "The uncanny")
- Constraints should be creative and challenging
- Make the constraints synergize in interesting ways
- Keep the scope realistic for a {duration}-hour jam

Tone: {tone} (encouraging/sarcastic/neutral)

IMPORTANT: Respond ONLY in the format above with the 5 fields. Do not write a full game description or narrative. Just provide the 5 structured fields.

Generate the concept now:"""


CONSTRAINT_GENERATION_PROMPT = """You are a creative game jam assistant. A developer is working on a game with these constraints:

{existing_concept}

Generate one additional creative constraint that complements the existing concept and makes it more interesting or challenging. The constraint should:
- Work well with the existing elements
- Add a new layer of challenge or creativity
- Be realistic for a game jam scope

Tone: {tone}

Provide just the constraint description (1-2 sentences):"""


COMMENTARY_PROMPT = """You are a game jam assistant bot with personality. A developer just shared this update:

"{user_message}"

{context_info}

Provide a brief (2-3 sentence) response that:
1. Acknowledges their progress or situation
2. Provides light commentary (be {tone})
3. Keeps them motivated

Be concise, friendly, and match the {tone} tone. Response:"""


VIBE_CHECK_PROMPT = """You are a game jam assistant bot with personality. A developer is checking in with you:

"{user_message}"

Provide a brief, {tone} response (2-4 sentences) that:
- Acknowledges their situation
- Provides encouragement, humor, or practical advice (depending on tone)
- Keeps them motivated to continue

Be concise and engaging. Response:"""


def format_concept_prompt(
    duration: int = 48,
    tone: str = "encouraging",
    genre: str = None
) -> str:
    """
    Format the concept generation prompt.
    
    Args:
        duration: Jam duration in hours
        tone: Response tone (encouraging/sarcastic/neutral)
        genre: Optional specific genre
    
    Returns:
        Formatted prompt string
    """
    prompt = CONCEPT_GENERATION_PROMPT.format(
        duration=duration,
        tone=tone
    )
    
    if genre:
        prompt = f"Genre preference: {genre}\n\n" + prompt
    
    return prompt


def format_constraint_prompt(
    existing_concept: str,
    tone: str = "encouraging"
) -> str:
    """
    Format the constraint generation prompt.
    
    Args:
        existing_concept: Description of existing concept
        tone: Response tone
    
    Returns:
        Formatted prompt string
    """
    return CONSTRAINT_GENERATION_PROMPT.format(
        existing_concept=existing_concept,
        tone=tone
    )


def format_commentary_prompt(
    user_message: str,
    context_info: str = "",
    tone: str = "encouraging"
) -> str:
    """
    Format the commentary prompt.
    
    Args:
        user_message: User's message/update
        context_info: Additional context (time elapsed, etc.)
        tone: Response tone
    
    Returns:
        Formatted prompt string
    """
    return COMMENTARY_PROMPT.format(
        user_message=user_message,
        context_info=context_info or "No additional context provided.",
        tone=tone
    )


def format_vibe_check_prompt(
    user_message: str,
    tone: str = "encouraging"
) -> str:
    """
    Format the vibe check prompt.
    
    Args:
        user_message: User's status message
        tone: Response tone
    
    Returns:
        Formatted prompt string
    """
    return VIBE_CHECK_PROMPT.format(
        user_message=user_message or "Just checking in",
        tone=tone
    )

