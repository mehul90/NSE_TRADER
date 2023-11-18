import pandas as pd
import matplotlib.pyplot as plt

import compute


def test_draw():
    print("pending")


def column(df, title="Adj Close", columns=["Adj Close"]):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df[columns].plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel(title)
    plt.grid()
    plt.show()


def all_columns_for_df(df, isGridRequired=True):
    df.plot(grid=isGridRequired)
    plt.show()


def histogram_on_daily_returns(df):
    df = compute.daily_returns(df[["Adj Close"]])
    mean = df["Adj Close"].mean()
    std = df["Adj Close"].std()
    df["Adj Close"].hist(bins=100)
    plt.axvline(mean)
    plt.axvline(std)
    plt.axvline(-std)
    plt.show()


def histogram_on_RSI(df):
    print("pending")


def bollinger_bands_from_df(df, symbol="Adj Close"):
    # Compute Bollinger Bands
    # 1. Compute rolling mean
    rolling_mean = compute.rolling_std_mean(df[symbol], window=20)

    # 2. Compute rolling standard deviation
    rolling_std = compute.rolling_std(df[symbol], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = compute.bollinger_bands(rolling_mean, rolling_std)

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df[symbol].plot(title="Bollinger Bands", label=symbol)
    rolling_mean.plot(label="Rolling mean", ax=ax)
    upper_band.plot(label="upper band", ax=ax)
    lower_band.plot(label="lower band", ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.show()


def bollinger_bands_diff_from_df(df, symbol="Adj Close"):
    # 1. Compute rolling mean
    rm_SPY = compute.rolling_std_mean(df[symbol], window=20)

    # 2. Compute rolling standard deviation
    rstd_SPY = compute.rolling_std(df[symbol], window=20)

    # 3. Compute upper and lower bands
    upper_band, lower_band = compute.bollinger_bands(rm_SPY, rstd_SPY)

    diff = upper_band - lower_band

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df[symbol].plot(title="Bollinger Bands", label=symbol)
    # rm_SPY.plot(label='Rolling mean', ax=ax)
    # upper_band.plot(label='upper band', ax=ax)
    # lower_band.plot(label='lower band', ax=ax)
    diff.plot(label="diff", ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.grid()
    plt.show()


def sma(df, days=21):
    df_sma = compute.running_average(df[["Adj Close"]], days)
    ax = df_sma["Adj Close"].plot(title="SMA", fontsize=12, color="r")
    df["Adj Close"].plot(title="Close", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("SMA")
    plt.grid()
    plt.show()
    return ax


def rsi(df, days=14):
    df_RSI = compute.RSI(df[["Adj Close"]], days)
    print(df_RSI.head())
    ax = df_RSI.plot(title="RSI", fontsize=12, color="r")
    # df['Adj Close'].plot(title='Close', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("RSI")
    plt.axhline(y=80.0, color="b", linestyle="-")
    plt.axhline(y=20.0, color="b", linestyle="-")
    plt.grid()
    plt.show()
    return ax


def macd(df):
    df_macd = compute.MACD(df[["Close"]])
    print(df_macd.head())
    print(df_macd.shape)
    ax = df_macd["Crossover"].plot(title="Crossover", color="b")
    # df_macd['26 ema'].plot(title='MACD', fontsize=12, ax=ax, color='r')
    # df_macd['12 ema'].plot(title='12 ema', ax=ax, color='g')
    ax.set_xlabel("Date")
    ax.set_ylabel("MACD")
    plt.grid()
    plt.show()
    return ax


def strategy_results(df, title="Strategy Results"):
    # print df.tail(1)
    last_row = df.tail(1)

    result_series = last_row["Accumulated Close"] / last_row["Adj Close"]
    pct_change = result_series.values[0] * 100
    txn_count = df["Stance"].diff().value_counts().drop([0]).sum()

    ax = df[["Adj Close", "Accumulated Close"]].plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Prices")

    plt.text(
        0.05,
        0.9,
        "Txn. count: " + str(txn_count),
        fontsize=15,
        ha="left",
        va="center",
        transform=ax.transAxes,
    )
    plt.text(
        0.05,
        0.8,
        "% diff: " + str(pct_change),
        fontsize=15,
        ha="left",
        va="center",
        transform=ax.transAxes,
    )

    plt.grid()
    plt.show()

    # print gain, net trades,


if __name__ == "__main__":
    test_draw()
