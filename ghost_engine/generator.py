# ghost_engine/generator.py
import random

# Simulated story generation for offline/free testing
def generate_story(prompt: str, style: str) -> str:
    """
    Generates a placeholder story in the given style without API.
    """
    starters = {
        "Horror": [
            "It was a dark and stormy night...",
            "Shadows crept across the abandoned hallway...",
            "A cold wind whispered through the empty house..."
        ],
        "Sci-Fi": [
            "In the year 3026, humanity colonized Mars...",
            "The spaceship glided silently through the asteroid field...",
            "AI beings debated the fate of the universe..."
        ],
        "Romance": [
            "Under the glowing sunset, their hands met...",
            "A soft melody filled the quiet café as they locked eyes...",
            "Love blossomed where least expected..."
        ],
        "Adventure": [
            "The jungle was thick, but our hero pressed onward...",
            "Mountains loomed as the expedition reached its peak...",
            "With a leap of faith, the treasure seeker descended into the cave..."
        ],
        "Comedy": [
            "He slipped on a banana peel and somehow landed in a pie...",
            "The talking dog refused to fetch the newspaper...",
            "A series of unfortunate yet hilarious events unfolded..."
        ]
    }

    # Pick a random starter from the chosen style
    starter = random.choice(starters.get(style, ["Once upon a time..."]))

    # Simulate story extension
    filler = " " + " ".join([f"{prompt}... continues." for _ in range(random.randint(2, 5))])

    return starter + filler

