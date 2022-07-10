import pandas as pd
import numpy as np
import math
import compute


# Create column Stance
# Create column Accumulated Close

def SMA_Crossover(df, fast=42, slow=252):
    # create the moving average values and
    # simultaneously append them to new columns in our existing DataFrame.
    df.dropna()
    df['fast'] = np.round(compute.running_average(df['Adj Close'], windowsize=fast), 2)
    df['slow'] = np.round(compute.running_average(df['Adj Close'], windowsize=slow), 2)

    # Generate stance: 0, -1, 1.
    df['fast-slow'] = df['fast'] - df['slow']

    offset = 0
    # add condition to ensure first stance change is never -1.
    df['Stance'] = np.where(df['fast-slow'] > offset, 1, 0)  # 42ma being offset amount above 252 value.
    df['Stance'] = np.where(df['fast-slow'] < offset, -1, df['Stance'])  # offset amount below 252 value
    # print df['Stance'].value_counts()
    df.dropna(inplace=True)

    # Generate accumulated closing price
    compute.accumulated_close(df)  # instead of everything below:

    # df_ma['Market Returns'] = np.log(df_ma['Adj Close'] / df_ma['Adj Close'].shift(1))
    # df_ma['Strategy'] = df_ma['Market Returns'] * df_ma['Stance'].shift(1)

def sma_crossover(df, fast=21, slow=9):
    df['fast'] = compute.sma_indicator(df['Close'], window=fast)
    df['slow'] = compute.sma_indicator(df['Close'], window=slow)
    df['fast-slow'] = df['fast'] - df['slow']

    offset = 0
    df['Stance'] = np.where(df['fast-slow'] > offset, 1, 0)
    df['Stance'] = np.where(df['fast-slow'] < offset, -1, df['Stance'])
    df.dropna(axis=0, how='any', inplace=True)
    first_negative = True if df['Stance'].iloc[0] == -1 else False
    for index, value in df['Stance'].iteritems():
        if value < 0:
            df['Stance'].at[index] = 0
        else:
            break

    compute.accumulated_close(df)


def RSI(df, lowerCutoff=30, upperCutoff=70, period=14):
    # rsi_calc = compute.RSI(df['Adj Close'], period=period)
    # df['RSI'] = pd.Series(rsi_calc)
    df['Stance'] = 0
    df['RSI'] = compute.ta_RSI(df['Adj Close'], period=period)
    offset = 0
    last_stance = 0
    upper_cutoff_set_once = False

    for index, row in df.iterrows():
        if row['RSI'] > upperCutoff:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row['RSI'] < lowerCutoff:
            last_stance = -1

        df.at[index, 'Stance'] = last_stance

    compute.accumulated_close(df)


def Bollinger_Band(df):
    # 1. Compute rolling mean
    rolling_mean = compute.rolling_std_mean(df['Adj Close'], window=20)

    # 2. Compute rolling standard deviation
    rolling_std = compute.rolling_std(df['Adj Close'], window=20)

    # 3. Compute upper and lower bands
    # upper_band, lower_band = compute.bollinger_bands(rolling_mean, rolling_std)
    upper_band, lower_band = compute.bollinger_bands(rolling_mean, rolling_std)

    df['Stance'] = 0
    last_stance = 0
    upper_cutoff_set_once = False

    upper_band.fillna(method='backfill', inplace=True)
    lower_band.fillna(method='backfill', inplace=True)

    df['Upper Band'] = upper_band
    df['Lower Band'] = lower_band

    for index, row in df.iterrows():

        if row['Adj Close'] > row['Upper Band']:
            upper_cutoff_set_once = True
            last_stance = 1
        elif upper_cutoff_set_once and row['Adj Close'] < row['Lower Band']:
            last_stance = -1

        df.at[index, 'Stance'] = last_stance

    compute.accumulated_close(df)


def MACD(df):
    print('Pending.')
