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


def test_run():
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date(2022, 7, 1)
    # endDate = datetime.date.today()
    # df = fetcher.get_data_for_symbol('RELIANCE', 'RELIANCE.NS', startDate, endDate)
    df = pd.read_csv("nse_data/rel.csv")
    print(df.tail(1))

    # strategy.RSI(df)
    # draw.strategy_results(df, title='RSI Strategy')

    # strategy.SMA_Crossover(df)
    # draw.strategy_results(df)

    strategy.Bollinger_Band(df)
    draw.strategy_results(df)

    draw.coloumn(df, title="Stance", columns=['Stance'])  # buy-sell signals for the strategy.


if __name__ == "__main__":
    test_run()
