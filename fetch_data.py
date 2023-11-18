import pandas_datareader.data as web
import yfinance as yf
import pandas as pd
import os
import datetime
import time
import dateutil
import nsepy

# scraps NSE website using beautiful soup.
# gets the following: https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?toDate=10-01-2017&symbolCount=1&dataType=PRICEVOLUMEDELIVERABLE&series=EQ&dateRange=&fromDate=01-01-2017&segmentLink=3&symbol=SBIN
# NO HAVE adjusted close, instead has turnover, no. of trades, VWAP, etc.
# get adjusted close from yahoo, using private func. below.

# NSE stopped supporting nsepy library
# search NSE symbol: https://www.nseindia.com/products/content/equities/equities/eq_security.html
"""def get_data_for_symbol(symbol, yahoo_symbol, startDate, endDate):
    directory = "nse_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = directory + "/" + symbol + str(startDate) + str(endDate) + ".csv"
    print(fileName)
    allow_reading_file = True
    if os.path.isfile(fileName) and allow_reading_file:
        # check symbol_date.csv, if present, read and return it
        print("reading from file:  " + fileName)
        df_temp = pd.read_csv(
            fileName, index_col="Date", parse_dates=True, na_values=["nan"]
        )

        return df_temp
    else:
        print("fetching data from API for " + symbol)
        # get data from API

        # doesn't return ALL data !!
        stock_data = nsepy.get_history(symbol=symbol, start=startDate, end=endDate)
        print("stock_data from NSE")
        print(stock_data.shape)
        print(stock_data.head())

        # get adjusted close from yahoo.
        df_temp = __download_data([yahoo_symbol], startDate, endDate)

        # JOIN adjusted close.
        stock_data = stock_data.join(df_temp)
        print(stock_data.shape)
        stock_data = stock_data.dropna(subset=["Adj Close"])
        print(stock_data.shape)
        # save to file
        stock_data.to_csv(fileName)

    # print stock_data
    return df_temp"""


# get from yahoo/google
# has limited data, but has adjusted close
# pass date objects
# search symbols here: https://finance.yahoo.com/lookup
# private function.
def __download_data(ticker, start, end, write_to_file=True):
    directory = "yahoo_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    fileName = directory + "/" + ticker[0] + ".csv"

    allow_reading_file = True
    if os.path.isfile(fileName) and allow_reading_file:
        # check symbol_date.csv, if present, read and return it
        print("reading from file:  " + fileName)
        df = pd.read_csv(
            fileName, index_col="Date", parse_dates=True, na_values=["nan"]
        )

        return df
    else:
        print("fetching data from API for " + ticker[0])
        # get data from API
        # panel_data = web.DataReader(ticker, "yahoo", startDate, endDate)
        df = yf.download(ticker[0], start=start, end=end)
        # final_df = panel_data["Adj Close"]
        # final_df = final_df.rename(columns={ticker[0]: "Adj Close"})

        if write_to_file:
            df.to_csv(fileName)

    print("final_df from Yahoo is:")
    print(df.shape)
    print(df.head())

    return df


def list_available_symbols():
    print("pending listAvailableSymbols")
    # list as table NSE symbol and matching Yahoo symbol.
    # possiblly save to file as well.


def update_data_for_symbol(symbol):
    print("pending")
    # read file, get data from last date to current date
    # append data to file.


if __name__ == "__main__":
    startDate = datetime.date(2000, 1, 1)
    endDate = datetime.date.today()
    print(__download_data(["RELIANCE.NS"], startDate, endDate).head())
    # get_data_for_symbol('RELIANCE', 'RELIANCE.NS', startDate, endDate)
