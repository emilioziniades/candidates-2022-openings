import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COLOURS = {
    "c4": "#114B5F",
    "d4": "#317B22",
    "e4": "#F3A712",
    "Nf3": "#CC001B",
}


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
    category_names = ["white_win", "draw", "black_win"]

    # test results
    results = {
        "QGD": [30, 20, 50],
        "Ruy Lopez": [50, 30, 20],
    }

    # real results
    perf_df = df.groupby(["opening_category"]).sum().drop(columns=["result"])
    perf_df["total"] = perf_df[["white_win", "draw", "black_win"]].sum(axis=1)
    for res in category_names:
        perf_df[f"{res}_percent"] = perf_df[res] / perf_df["total"] * 100
    results = perf_df.drop(
        [
            "white_win",
            "draw",
            "black_win",
            "total",
        ],
        axis=1,
    ).to_dict("index")
    results = {
        opening: list(percentages.values()) for opening, percentages in results.items()
    }
    results = dict(
        sorted(
            results.items(), key=lambda p: df["opening_category"].value_counts()[p[0]]
        )
    )

    labels = list(results.keys())
    labels = [rf"{i} ($\bf{df['opening_category'].value_counts()[i]}$)" for i in labels]
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    colours = ["#FFFFFF", "#767676", "#000000"]

    fig, ax = plt.subplots()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, 100)
    for i, (colour, colname) in enumerate(zip(colours, category_names)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(
            labels,
            widths,
            left=starts,
            color=colour,
            label=colname.replace("_", " ").capitalize(),
            height=0.7,
            edgecolor="black",
        )
        text_colour = "black" if colour == "#FFFFFF" else "white"
        bar_labels = [f"{j:.1f}%" if j != 0 else "" for j in data[:, i]]
        ax.bar_label(rects, labels=bar_labels, label_type="center", color=text_colour)

    ax.set_title("Opening performance (number of games)", loc="left", pad=30)
    ax.legend(
        ncol=len(category_names),
        bbox_to_anchor=(0, 1),
        loc="lower left",
        fontsize="small",
    )
    ax.set_yticks(labels)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    fig.savefig("figures/opening_performance.png", dpi=300)
