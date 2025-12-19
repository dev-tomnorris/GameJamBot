"""Message formatting helpers for Discord bot responses."""

from typing import Dict, Optional


def format_concept_message(concept: Dict[str, str], is_ai: bool = False) -> str:
    """
    Format a game concept into a Discord message.
    
    Args:
        concept: Dictionary containing concept fields (genre, setting, mechanic, theme, constraint, time_limit)
        is_ai: Whether this is an AI-generated concept (affects formatting)
    
    Returns:
        Formatted message string
    """
    if is_ai and "description" in concept:
        # AI-generated format with description
        message = "🎮 Game Jam Concept Generator 🎮\n\n"
        message += concept.get("description", "")
        
        if "explanation" in concept:
            message += f"\n\n{concept['explanation']}"
        
        if "time_limit" in concept:
            message += f"\n\nTime Limit: {concept['time_limit']} hours"
        
        if "difficulty" in concept:
            message += f"\nDifficulty: {concept['difficulty'].title()}"
        
        # Add closing message
        closing_messages = [
            "Now stop reading and start coding! ⏰",
            "Good luck, you'll need it! 🎲",
            "Time to make something awesome! 🚀",
        ]
        import random
        message += f"\n\n{random.choice(closing_messages)}"
        
        return message
    else:
        # Template-based format
        message = "🎮 Game Jam Concept Generator 🎮\n\n"
        message += f"**Genre:** {concept.get('genre', 'Unknown')}\n"
        message += f"**Setting:** {concept.get('setting', 'Unknown')}\n"
        message += f"**Core Mechanic:** {concept.get('mechanic', 'Unknown')}\n"
        message += f"**Theme:** {concept.get('theme', 'Unknown')}\n"
        
        if "constraint" in concept:
            message += f"**Special Constraint:** {concept['constraint']}\n"
        
        if "time_limit" in concept:
            message += f"**Time Limit:** {concept['time_limit']} hours\n"
        
        message += "\nGood luck, you'll need it! 🎲"
        
        return message


def format_constraint_message(constraint: str) -> str:
    """
    Format an additional constraint message.
    
    Args:
        constraint: The constraint text
    
    Returns:
        Formatted message string
    """
    message = f"**Additional Constraint:** {constraint}\n\n"
    
    closing_messages = [
        "May the odds be ever in your favor... 📐",
        "Just when you thought it couldn't get harder... 😏",
        "Because why make it easy? 🎯",
        "Your game just got more interesting! 🎨",
    ]
    import random
    message += random.choice(closing_messages)
    
    return message


def format_error_message(error: str) -> str:
    """
    Format an error message for the user.
    
    Args:
        error: Error description
    
    Returns:
        Formatted error message
    """
    return f"❌ **Error:** {error}\n\nPlease try again or use `/help` for assistance."


def format_help_message() -> str:
    """
    Format the help message with all available commands.
    
    Returns:
        Formatted help message
    """
    message = "🎮 **Game Jam Assistant Bot** 🎮\n\n"
    message += "**Available Commands:**\n\n"
    
    message += "`/generate-concept [genre] [difficulty]`\n"
    message += "Generate a random game concept with constraints.\n"
    message += "• `genre` (optional): Specify a genre (platformer, rpg, puzzle, etc.)\n"
    message += "• `difficulty` (optional): Easy, Medium, Hard, Insane\n\n"
    
    message += "`/generate-constraint`\n"
    message += "Add one more constraint to your existing concept.\n\n"
    
    message += "`/vibe-check [message]`\n"
    message += "Get AI commentary on your current progress/mood.\n"
    message += "• `message` (optional): Your current status or situation\n\n"
    
    message += "`/help`\n"
    message += "Show this help message.\n\n"
    
    message += "---\n"
    message += "Need help? The bot uses AI to generate creative concepts and provide encouragement during your game jams!"
    
    return message

