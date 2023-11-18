import pandas as pd
import datetime
import numpy as np

# https://github.com/nlsdfnbch/pandas-technical-indicators/blob/master/technical_indicators.py


def daily_returns(df):
    # how to read/interpret this ?
    print(df.head())
    # (tomorrow price/today price) - 1
    daily_return = (df / df.shift(1)) - 1
    print(daily_return.head())
    daily_return.ix[0, :] = 0
    return daily_return


def normalize(df, column="Adj Close"):
    # take column, normalize from earliest available date.
    print("pending normalize")


# moving average.
def running_average(df, windowsize):
    return df.rolling(windowsize).mean()


def exponential_moving_average(df, windowsize=60):
    # df['ewma'] = pd.ewma(df["avg"], span=60, freq="D")
    pd.ewma(df["Adj Close"], span=windowsize, freq="D")


def rolling_std_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    # take df, column name option, default value for window too.
    # return pd.rolling_std(values, window=window, center=False).mean()
    return values.rolling(window=window).mean()


def rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return values.rolling(window=window).std()


def bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    # TODO: Compute upper_band and lower_band
    upper_band = rm + rstd * 2  # pd.rolling_std(values, window=window)
    lower_band = rm - rstd * 2  # pd.rolling_std(values, window=window)
    return upper_band, lower_band


def RSI(series, period):
    # print series.size
    delta = series.diff().dropna()
    # print 'size after drop is '
    # print delta.size
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period - 1]] = np.mean(u[:period])  # first value is sum of avg gains
    u = u.drop(u.index[: (period - 1)])
    d[d.index[period - 1]] = np.mean(d[:period])  # first value is sum of avg losses
    d = d.drop(d.index[: (period - 1)])
    rs = (
        u.ewm(com=period - 1, adjust=False).mean()
        / d.ewm(com=period - 1, adjust=False).mean()
    )
    df = pd.DataFrame(100 - 100 / (1 + rs))

    # slice first period dates, create series with 50 as value, per date. then concat.
    prefixed_values = pd.Series(50, index=series.index.values[0:period])
    return pd.concat([prefixed_values, df.iloc[:, 0]])


def MACD(df, fast_ma=26, slow_ma=12, signal_period=9):
    df["30 mavg"] = pd.rolling_mean(df["Close"], 30)
    df["26 ema"] = pd.ewma(df["Close"], span=fast_ma)
    df["12 ema"] = pd.ewma(df["Close"], span=slow_ma)
    df["MACD"] = df["12 ema"] - df["26 ema"]
    df["Signal"] = pd.ewma(df["MACD"], span=signal_period)
    df["Crossover"] = df["MACD"] - df["Signal"]
    return df


# to be tested...
def stochastic_oscillator_k(df, k_window=14, d_window=3):
    # Create the "L14" column in the DataFrame
    df["Low_K"] = df["Low"].rolling(window=k_window).min()

    # Create the "H14" column in the DataFrame
    df["High_K"] = df["High"].rolling(window=k_window).max()

    # Create the "%K" column in the DataFrame
    df["%K"] = 100 * ((df["Close"] - df["Low_K"]) / (df["High_K"] - df["Low_K"]))

    # Create the "%D" column in the DataFrame
    df["%D"] = df["%K"].rolling(window=d_window).mean()


def ROC(df, n):
    M = df.diff(n - 1)
    N = df.shift(n - 1)
    ROC = pd.Series(((M / N) * 100), name="ROC_" + str(n))
    return ROC


def vortex_indicator(df, n):
    """Calculate the Vortex Indicator for given data.

    Vortex Indicator described here:
        http://www.vortexindicator.com/VFX_VORTEX.PDF
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = 0
    TR = [0]
    while i < df.index[-1]:
        Range = max(df.get_value(i + 1, "High"), df.get_value(i, "Close")) - min(
            df.get_value(i + 1, "Low"), df.get_value(i, "Close")
        )
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < df.index[-1]:
        Range = abs(df.get_value(i + 1, "High") - df.get_value(i, "Low")) - abs(
            df.get_value(i + 1, "Low") - df.get_value(i, "High")
        )
        VM.append(Range)
        i = i + 1
    VI = pd.Series(
        pd.rolling_sum(pd.Series(VM), n) / pd.rolling_sum(pd.Series(TR), n),
        name="Vortex_" + str(n),
    )
    df = df.join(VI)
    return df


def money_flow_index(df, n):
    """Calculate Money Flow Index and Ratio for given data.

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    PP = (df["High"] + df["Low"] + df["Close"]) / 3
    i = 0
    PosMF = [0]
    while i < df.index[-1]:
        if PP[i + 1] > PP[i]:
            PosMF.append(PP[i + 1] * df.get_value(i + 1, "Volume"))
        else:
            PosMF.append(0)
        i = i + 1
    PosMF = pd.Series(PosMF)
    TotMF = PP * df["Volume"]
    MFR = pd.Series(PosMF / TotMF)
    MFI = pd.Series(pd.rolling_mean(MFR, n), name="MFI_" + str(n))
    df = df.join(MFI)
    return df


def CCI(df):
    print("pending")


def Williams_percent_r(df):
    print("pending")


# ---------------------------------------------


def accumulated_close(df):
    # requires a column Stance, and Adj close

    pointer = df.iloc[0]  # first date as index.
    booked_profit = 0.00

    for index, row in df.iterrows():
        if row["Stance"] > 0:
            df.loc[index, "Accumulated Close"] = (
                df.loc[index, "Adj Close"] + booked_profit
            )
            pointer = index
            # print 'Buy and hold'
        elif row["Stance"] < 0:
            df.loc[index, "Accumulated Close"] = df.loc[pointer, "Accumulated Close"]
            booked_profit = (
                df.loc[pointer, "Accumulated Close"] - df.loc[index, "Adj Close"]
            )
            # print 'Sell and hold'
        else:
            df.loc[index, "Accumulated Close"] = df.loc[index, "Adj Close"]
            # print 'Waiting...'
