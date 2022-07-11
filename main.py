import re
from collections import Counter

import chess.pgn
from matplotlib.sankey import Sankey


def main():
    games = load_games()

    first_moves = Counter(game.next().san() for game in games)

    openings = Counter(game.headers["Opening"] for game in games)

    opening_categories = []
    for opening in openings:
        if match := re.search(r"(.*):", opening):
            opening_categories.append(match.group(1))
        else:
            opening_categories.append(opening)
    opening_categories = Counter(opening_categories)


def load_games():
    games = []
    with open("./candidates_2022_all_games.pgn", "r") as all_games_pgn:
        while True:
            game = chess.pgn.read_game(all_games_pgn)
            if game is None:
                break
            # ensure player names are consistent
            for colour in ["White", "Black"]:
                player = game.headers[colour]
                if match := re.search(r"(.+), (.+)", player):
                    game.headers[colour] = match.group(2) + " " + match.group(1)

            games.append(game)

    white_players = Counter([i.headers["White"] for i in games])
    black_players = Counter([i.headers["Black"] for i in games])

    assert all(i == 7 for i in white_players.values())
    assert all(i == 7 for i in black_players.values())
    assert len(white_players) == len(black_players) == 8
    assert len(games) == 56

    return games


if __name__ == "__main__":
    main()

"""
TODO

- bar chart of first moves
- bar chart of opening categories
- bar char of openings proper
- Sankey diagram of moves
- W/D/L bar chart for each opening
"""
