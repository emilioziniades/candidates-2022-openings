COLOURS = {
    "c4": "#114B5F",
    "d4": "#317B22",
    "e4": "#F3A712",
    "Nf3": "#CC001B",
    "white_win": "#FFFFFF",
    "draw": "#767676",
    "black_win": "#000000",
}

FIRST_MOVE_TO_OPENING = {
    "c4": [
        "English Opening",
    ],
    "d4": [
        "Queen's Gambit Declined",
        "Grünfeld Defense",
        "Catalan Opening",
        "Nimzo-Indian Defense",
        "Semi-Slav Defense",
        "Tarrasch Defense",
    ],
    "e4": [
        "Sicilian Defense",
        "Ruy Lopez",
        "Italian Game",
        "Russian Game",
        "Four Knights Game",
    ],
    "Nf3": [
        "King's Indian Attack",
    ],
}

OPENING_TO_FIRST_MOVE = {
    opening: move
    for move, openings in FIRST_MOVE_TO_OPENING.items()
    for opening in openings
}
