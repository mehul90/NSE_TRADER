import pandas as pd
import numpy as np
import math
import compute


# Create column Stance
# Create column Accumulated Close


def SMA_Crossover(df, fast=42, slow=252):
    # create the moving average values and
    # simultaneously append them to new columns in our existing DataFrame.
    df["42d"] = np.round(compute.running_average(df["Adj Close"], windowsize=42), 2)
    df["252d"] = np.round(compute.running_average(df["Adj Close"], windowsize=252), 2)

    # Generate stance: 0, -1, 1.
    df["42-252"] = df["42d"] - df["252d"]

    offset = 0
    # add condition to ensure first stance change is never -1.
    df["Stance"] = np.where(
        df["42-252"] > offset, 1, 0
    )  # 42ma being offset amount above 252 value.
    df["Stance"] = np.where(
        df["42-252"] < offset, -1, df["Stance"]
    )  # offset amount below 252 value
    # print df['Stance'].value_counts()

    # Generate accumulated closing price
    compute.accumulated_close(df)  # instead of everything below:

    # df_ma['Market Returns'] = np.log(df_ma['Adj Close'] / df_ma['Adj Close'].shift(1))
    # df_ma['Strategy'] = df_ma['Market Returns'] * df_ma['Stance'].shift(1)


def RSI(df, lowerCutoff=30, upperCutoff=70, period=14):
    df["RSI"] = pd.Series(compute.RSI(df["Adj Close"], period=period))
    df["Stance"] = 0
    offset = 0
    last_stance = 0
    upper_cutoff_set_once = False

    for index, row in df.iterrows():
        if row["RSI"] > upperCutoff:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row["RSI"] < lowerCutoff:
            last_stance = -1

        df.at[index, "Stance"] = last_stance

    compute.accumulated_close(df)


def Bollinger_Band(df):
    # 1. Compute rolling mean
    rolling_mean = compute.rolling_std_mean(df["Adj Close"], window=10)

    # 2. Compute rolling standard deviation
    rolling_std = compute.rolling_std(df["Adj Close"], window=10)

    # 3. Compute upper and lower bands
    upper_band, lower_band = compute.bollinger_bands(rolling_mean, rolling_std)

    df["Stance"] = 0
    last_stance = 0
    upper_cutoff_set_once = False

    upper_band.fillna(method="backfill", inplace=True)
    lower_band.fillna(method="backfill", inplace=True)

    df["Upper Band"] = upper_band
    df["Lower Band"] = lower_band

    for index, row in df.iterrows():
        if row["Adj Close"] > row["Upper Band"]:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row["Adj Close"] < row["Lower Band"]:
            last_stance = -1

        df.at[index, "Stance"] = last_stance

    compute.accumulated_close(df)


def MACD(df):
    print("Pending.")
