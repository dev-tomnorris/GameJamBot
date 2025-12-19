"""Prompt templates for AI generation."""


CONCEPT_GENERATION_PROMPT = """You are a creative game jam assistant helping developers come up with interesting game concepts.

Generate a unique game concept that includes:
- Genre
- Setting
- Core mechanic
- Theme
- One creative constraint that makes it more challenging/interesting

Make the constraints synergize in interesting ways. Be creative and unexpected, but keep the scope realistic for a {duration}-hour jam.

Tone: {tone} (encouraging/sarcastic/neutral)

Format your response as a natural description of the game concept, followed by a brief explanation of why the constraints work together. Keep it concise and engaging.

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

