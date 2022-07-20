import re
from collections import Counter

import chess.pgn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Games = list[chess.pgn.Game]

COLOURS = {
    "c4": "#114B5F",
    "d4": "#317B22",
    "e4": "#F3A712",
    "Nf3": "#CC001B",
}


def main() -> None:
    games = load_games()

    df = pd.DataFrame()
    df["result"] = [parse_result(game.headers["Result"]) for game in games]
    df["first_move"] = [game.next().san() for game in games]
    df["opening"] = [game.headers["Opening"] for game in games]
    df["opening_category"] = df["opening"].map(parse_opening_category)
    from IPython import embed; embed(colors='neutral')  # fmt: skip

    # plot_first_moves(df)
    plot_opening_categories(df)
    # plot_opening_performance()


def plot_first_moves(df: pd.DataFrame) -> None:
    first_moves = df["first_move"].value_counts().to_dict()
    first_move, freq = zip(*sorted(first_moves.items(), key=lambda x: x[0].lower()))
    colours = [COLOURS[i] for i in first_move]
    plt.bar(first_move, freq, color=colours)
    plt.show()


def plot_opening_categories(df: pd.DataFrame) -> None:
    first_move_to_opening = {
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
    opening_to_first_move = {
        opening: move
        for move, openings in first_move_to_opening.items()
        for opening in openings
    }

    opening_categories = df["opening_category"].value_counts().to_dict()

    opening_categories = sorted(
        opening_categories.items(),
        key=lambda x: (opening_to_first_move[x[0]].lower(), 1 / x[1]),
    )
    opening_cat, freq = zip(*opening_categories)
    colours = [COLOURS[opening_to_first_move[i]] for i in opening_cat]

    plt.bar(opening_cat, freq, color=colours)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def parse_result(result: str) -> int:
    results = {
        "1-0": 1,
        "1/2-1/2": 0,
        "0-1": -1,
    }
    return results[result]


def parse_opening_category(opening: str) -> str:
    if match := re.search(r"(.*):", opening):
        return match.group(1)
    else:
        return opening


def count_opening_categories(openings: Counter) -> Counter:
    opening_categories = []
    for opening in openings:
        if match := re.search(r"(.*):", opening):
            opening_categories.append(match.group(1))
        else:
            opening_categories.append(opening)
    return Counter(opening_categories)


def count_opening_performance(games: Games, openings: Counter) -> Counter:
    openings = count_opening_categories(openings).keys()


def plot_opening_performance() -> None:
    category_names = ["White win", "Draw", "Black win"]
    results = {
        "QGD": [30, 20, 50],
        "Ruy Lopez": [50, 30, 20],
    }
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    colours = ["#FFFFFF", "#BABABA", "#000000"]
    bg_colour = "#FCEAC5"

    fig, ax = plt.subplots(facecolor=bg_colour)
    ax.xaxis.set_visible(False)
    ax.set_facecolor(bg_colour)
    ax.set_xlim(0, 100)
    for i, (colour, colname) in enumerate(zip(colours, category_names)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(
            labels, widths, left=starts, color=colour, label=colname, height=0.3
        )
        text_colour = "black" if colour == "#FFFFFF" else "white"
        ax.bar_label(rects, label_type="center", color=text_colour, fmt="%d%%")

    ax.set_yticks(labels)

    plt.show()


def load_games() -> Games:
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
- W/D/L bar chart for each opening
"""
