import random

ghost_lines = {
    "Horror": [
        "I sense something evil in this tale...",
        "Careful… some doors should stay closed.",
        "Your story feeds the darkness 👻"
    ],
    "Comedy": [
        "Even ghosts need a good laugh!",
        "This is oddly fun for a haunting.",
        "I almost forgot I’m supposed to be scary 😄"
    ],
    "Romance": [
        "Love lingers even beyond death...",
        "A warm glow in a cold afterlife.",
    ]
}

def ghost_reaction(style):
    if style in ghost_lines:
        return random.choice(ghost_lines[style])
    return "I am watching your story unfold..."
