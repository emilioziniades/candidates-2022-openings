import re
from collections import Counter

import chess.pgn
import pandas as pd


Games = list[chess.pgn.Game]


def load_data() -> pd.DataFrame:
    games_file = "./data/candidates_2022_all_games.pgn"
    games = load_games(games_file)
    df = prepare_df(games)
    return df


def load_games(filename: str) -> Games:
    games = []
    with open(filename, "r") as all_games_pgn:
        while True:
            game = chess.pgn.read_game(all_games_pgn)
            if game is None:
                break
            # ensure player names are consistent: Ziniades, Emilio -> Emilio Ziniades
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


def prepare_df(games: Games) -> pd.DataFrame:
    def parse_result(result: str) -> int:
        results = {
            "1-0": 1,
            "1/2-1/2": 0,
            "0-1": -1,
        }
        return results[result]

    def parse_opening_category(opening: str) -> str:
        match = re.search(r"(.*):", opening)
        return match.group(1) if match else opening

    df = pd.DataFrame()
    df["result"] = [parse_result(game.headers["Result"]) for game in games]
    df["white_win"] = (df["result"] == 1).astype(int)
    df["draw"] = (df["result"] == 0).astype(int)
    df["black_win"] = (df["result"] == -1).astype(int)
    df["first_move"] = [game.next().san() for game in games]
    df["opening"] = [game.headers["Opening"] for game in games]
    df["opening_category"] = df["opening"].map(parse_opening_category)

    return df
