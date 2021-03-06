from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from util import OPENING_TO_FIRST_MOVE, COLOURS


def plot_first_moves(df: pd.DataFrame) -> None:
    # count first first moves
    first_moves = df["first_move"].value_counts().to_dict()
    first_move, freq = zip(*sorted(first_moves.items(), key=lambda x: x[0].lower()))
    colours = [COLOURS[i] for i in first_move]

    # plot bar chart
    fig, ax = plt.subplots()
    rects = ax.bar(first_move, freq, color=colours)
    ax.bar_label(rects, padding=3)
    ax.set_title("First moves by frequency")
    ax.set_xlabel("First move")
    ax.set_ylabel("Frequency")
    ax.set_ylim(0, max(freq) + 4)
    plt.tight_layout()
    fig.savefig("figures/first_moves.png", dpi=300)


def plot_opening_categories(df: pd.DataFrame) -> None:
    def first_move_and_inverse_frequency(opening: tuple[str, int]) -> tuple[str, float]:
        name, freq = opening
        first_move = OPENING_TO_FIRST_MOVE[name]
        return first_move.lower(), 1 / freq

    # count opening categories and sort by (first_move, inverse_frequency)
    opening_categories = df["opening_category"].value_counts().to_dict()
    opening_categories = sorted(
        opening_categories.items(),
        key=first_move_and_inverse_frequency,
    )
    opening_cat, freq = zip(*opening_categories)
    colours = [COLOURS[OPENING_TO_FIRST_MOVE[i]] for i in opening_cat]

    # plot bar chart
    fig, ax = plt.subplots()
    rects = ax.bar(opening_cat, freq, color=colours)
    ax.bar_label(rects)
    ax.tick_params(rotation=90)
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Opening category")
    ax.set_title("Opening categories by frequency, grouped by first move")
    ax.set_ylim(0, max(freq) + 2)
    plt.tight_layout()
    fig.savefig("figures/opening_categories.png", dpi=300)


def plot_opening_performance(df: pd.DataFrame) -> None:

    # determine number of white win/draw/black win results for each opening
    possible_results = ["white_win", "draw", "black_win"]
    perf_df = df.groupby(["opening_category"]).sum()
    perf_df["total"] = perf_df[possible_results].sum(axis=1)

    # stash totals for later
    total_row = perf_df.sum().drop(["result", "total"])
    total_games = total_row.sum()

    # calculate white win/draw/black win percentages
    for res in possible_results:
        perf_df[f"{res}_percent"] = perf_df[res] / perf_df["total"] * 100
    perf_df.drop(possible_results, axis=1, inplace=True)
    perf_df.drop(["total", "result"], axis=1, inplace=True)
    results = perf_df.to_dict("index")
    results = {
        opening: list(percentages.values()) for opening, percentages in results.items()
    }
    results = dict(
        sorted(
            results.items(),
            key=lambda p: df["opening_category"].value_counts()[p[0]],
        )
    )

    # generate labels of the form: Opening (n_games)
    def label(x: str, f: Callable[[str], int]) -> str:
        return rf"{x} ($\bf{f(x)}$)"

    def lookup_value_count(x: str) -> int:
        return df["opening_category"].value_counts()[x]

    labels = [label(i, lookup_value_count) for i in results.keys()]

    # convert results into array
    data = np.array(list(results.values()))

    # insert overall white/black/draw performance into labels and data
    total_row = total_row / total_row.sum() * 100
    labels.insert(0, label("Total", lambda _: total_games))
    data = np.vstack([total_row.tolist(), data])

    data_cum = data.cumsum(axis=1)
    colours = [COLOURS[i] for i in possible_results]

    # make hbars
    fig, ax = plt.subplots()
    for i, (colour, result) in enumerate(zip(colours, possible_results)):
        pretty_result = result.replace("_", " ").capitalize()
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(
            labels,
            widths,
            left=starts,
            color=colour,
            label=pretty_result,
            height=0.7,
            edgecolor="black",
        )
        text_colour = "black" if colour == "#FFFFFF" else "white"
        bar_labels = [f"{j:.1f}%" if j != 0 else "" for j in data[:, i]]
        ax.bar_label(
            rects,
            labels=bar_labels,
            label_type="center",
            color=text_colour,
        )

    # customize appearance
    ax.set_title("Opening performance (number of games)", loc="left", pad=30)
    ax.legend(
        ncol=len(possible_results),
        bbox_to_anchor=(0, 1),
        loc="lower left",
        fontsize="small",
    )
    ax.set_yticks(labels)
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, 100)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.tight_layout()
    fig.savefig("figures/opening_performance.png", dpi=300)
