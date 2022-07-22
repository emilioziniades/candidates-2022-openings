class OpeningToFirstMove:
    def __init__(self):
        self.first_move_to_opening = {
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
        self.opening_to_first_move = {
            opening: move
            for move, openings in self.first_move_to_opening.items()
            for opening in openings
        }

    def __getitem__(self, opening):
        first_move = self.opening_to_first_move[opening]
        return first_move
