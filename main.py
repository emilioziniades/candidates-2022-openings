from prepare import load_data
from plot import plot_first_moves, plot_opening_categories, plot_opening_performance


def main() -> None:
    df = load_data()

    # plot_first_moves(df)
    plot_opening_categories(df)
    # plot_opening_performance(df)


if __name__ == "__main__":
    main()
