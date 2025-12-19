"""Template-based game concept generator for Phase 1."""

import random
from typing import Dict, Optional, List
from config import MIN_CONSTRAINTS, MAX_CONSTRAINTS


# Category lists from design document
GENRES = [
    "Platformer", "Puzzle", "RPG", "Roguelike", "Metroidvania", "Visual Novel",
    "Tower Defense", "Card Game", "Rhythm", "Racing", "Fighting", "Stealth",
    "Survival", "Strategy", "Adventure", "Point-and-Click", "Idle", "Management",
    "Simulation", "Horror", "Action", "Shooter", "Sports", "Educational"
]

SETTINGS = [
    "Space station", "Medieval castle", "Cyberpunk city", "Underwater",
    "Post-apocalyptic", "Fantasy forest", "Desert wasteland", "Corporate office",
    "Haunted mansion", "School", "Laboratory", "Alien planet", "Dream world",
    "Tiny world (microscopic)", "Giant world (macro)", "Inside a computer",
    "Ancient ruins", "Suburban neighborhood", "Abandoned factory", "Museum",
    "Library", "Prison", "Hospital", "Airport", "Shopping mall", "Theme park",
    "Cemetery", "Beach", "Mountain peak", "Underground cave", "Floating island"
]

MECHANICS = [
    "Time loop", "Gravity manipulation", "Portal creation", "Shape-shifting",
    "Resource management", "Dialogue choices", "Crafting system", "Permadeath",
    "Procedural generation", "Limited inventory", "One-button control",
    "Memory-based puzzles", "Physics-based", "Asymmetric multiplayer",
    "Deck building", "Turn-based combat", "Real-time strategy", "Stealth mechanics",
    "Parkour movement", "Building/construction", "Trading", "Farming",
    "Cooking", "Fishing", "Exploration", "Combat", "Puzzle solving"
]

THEMES = [
    "Isolation", "Friendship", "Betrayal", "Discovery", "Loss", "Growth",
    "Rebellion", "Mystery", "Horror", "Comedy", "Nostalgia", "Existential",
    "Environmental", "Political", "Love", "Fear", "Hope", "Greed", "Redemption",
    "Sacrifice", "Identity", "Memory", "Time", "Death", "Rebirth"
]

SPECIAL_CONSTRAINTS = [
    "No text or dialogue allowed",
    "Only 3 colors",
    "Everything is circles",
    "One-button gameplay",
    "No jumping",
    "Reverse controls",
    "Real-time only (no pause)",
    "All assets must be ASCII art",
    "No sound effects",
    "Enemies are friendly",
    "You play as the environment",
    "Speed increases constantly",
    "Everything moves in slow motion",
    "Only black and white",
    "No UI elements",
    "First-person only",
    "Top-down only",
    "Side-scrolling only",
    "No death/failure state",
    "Permadeath (one life)",
    "No save system",
    "Time limit per level",
    "Only mouse controls",
    "Only keyboard controls",
    "No tutorial",
    "Silent protagonist",
    "No inventory",
    "Infinite respawns",
    "No health system",
    "Only one enemy type"
]

TIME_LIMITS = [24, 48, 72, 96, 120, 144]


class TemplateGenerator:
    """Generates game concepts using template-based random selection."""
    
    def __init__(self):
        self.genres = GENRES
        self.settings = SETTINGS
        self.mechanics = MECHANICS
        self.themes = THEMES
        self.constraints = SPECIAL_CONSTRAINTS
        self.time_limits = TIME_LIMITS
    
    def generate_concept(
        self,
        genre: Optional[str] = None,
        difficulty: str = "medium"
    ) -> Dict[str, str]:
        """
        Generate a random game concept with constraints.
        
        Args:
            genre: Optional specific genre to use
            difficulty: Difficulty level (easy, medium, hard, insane)
                      Affects number of constraints
        
        Returns:
            Dictionary containing concept fields
        """
        # Select genre
        selected_genre = genre if genre and genre.lower() in [g.lower() for g in self.genres] else random.choice(self.genres)
        
        # Select other elements
        setting = random.choice(self.settings)
        mechanic = random.choice(self.mechanics)
        theme = random.choice(self.themes)
        time_limit = random.choice(self.time_limits)
        
        # Select constraint based on difficulty
        constraint = random.choice(self.constraints)
        
        return {
            "genre": selected_genre,
            "setting": setting,
            "mechanic": mechanic,
            "theme": theme,
            "constraint": constraint,
            "time_limit": str(time_limit),
            "difficulty": difficulty.lower()
        }
    
    def generate_additional_constraint(self) -> str:
        """
        Generate a single additional constraint.
        
        Returns:
            Constraint string
        """
        return random.choice(self.constraints)
    
    def _select_constraints(self, difficulty: str) -> int:
        """
        Determine number of constraints based on difficulty.
        
        Args:
            difficulty: Difficulty level
        
        Returns:
            Number of constraints to include
        """
        difficulty = difficulty.lower()
        
        if difficulty == "easy":
            return MIN_CONSTRAINTS
        elif difficulty == "medium":
            return (MIN_CONSTRAINTS + MAX_CONSTRAINTS) // 2
        elif difficulty == "hard":
            return MAX_CONSTRAINTS - 1
        elif difficulty == "insane":
            return MAX_CONSTRAINTS
        else:
            return (MIN_CONSTRAINTS + MAX_CONSTRAINTS) // 2


# Global instance
template_generator = TemplateGenerator()

