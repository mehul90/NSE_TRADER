import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# import fetch_data as fetcher
import draw
import compute
import strategy


# get , compute , draw.


def compare_results():
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date(2022, 7, 1)
    # endDate = datetime.date.today()
    # df = fetcher.get_data_for_symbol('RELIANCE', 'RELIANCE.NS', startDate, endDate)
    df = pd.read_csv("nse_data/hdfc.csv")
    print(df.tail(1))

    df = strategy.RSI(df)
    draw.strategy_results(df, title='RSI Strategy')

    # df = strategy.sma_crossover(df, fast=21, slow=5)
    # draw.strategy_results(df)

    # df = strategy.macd(df, fast=12, slow=26)
    # draw.strategy_results(df)

    # df = strategy.ema_crossover(df)
    # draw.strategy_results(df)

    # df = strategy.Bollinger_Band(df)
    # draw.strategy_results(df)

    draw.coloumn(df, title="Stance", columns=['Stance', 'Date'])  # buy-sell signals for the strategy.


if __name__ == "__main__":
    compare_results()
