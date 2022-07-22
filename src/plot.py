import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from util import OpeningToFirstMove, COLOURS


def plot_first_moves(df: pd.DataFrame) -> None:
    first_moves = df["first_move"].value_counts().to_dict()
    first_move, freq = zip(*sorted(first_moves.items(), key=lambda x: x[0].lower()))
    colours = [COLOURS[i] for i in first_move]

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
    opening_to_first_move = OpeningToFirstMove()

    def sort_by_first_move_and_frequency(opening):
        name, freq = opening
        first_move = opening_to_first_move[name]
        return first_move.lower(), 1 / freq

    opening_categories = df["opening_category"].value_counts().to_dict()
    opening_categories = sorted(
        opening_categories.items(),
        key=sort_by_first_move_and_frequency,
    )
    opening_cat, freq = zip(*opening_categories)
    colours = [COLOURS[opening_to_first_move[i]] for i in opening_cat]

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
    possible_results = ["white_win", "draw", "black_win"]
    perf_df = df.groupby(["opening_category"]).sum()
    perf_df["total"] = perf_df[possible_results].sum(axis=1)
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

    label = lambda i: rf"{i} ($\bf{df['opening_category'].value_counts()[i]}$)"
    labels = [label(i) for i in results.keys()]
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    colours = [COLOURS[i] for i in possible_results]

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