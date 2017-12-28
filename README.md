# NSE_TRADER
A basic implementation to download historic prices, apply a strategy, and see the strategy performance vis-a-vis the actual stock prices.

The code requires some clean-up.

The overview is as follows:
- Go to file strategy.py
- Get the historic data for the required script
- Parse this data as a pandas dataframe
- Apply an appropriate strategy that you want to test. The current code includes basic strategies like RSI crossover or Bollinger band.
- Generate trading signals for this strategy.
- Plot graph of portfolio growth , showing the original prices, versus the portfolio value if you trade by the signals.
- Fine-tune the strategy, run the code again, make money, and then make some more !!

A typical plot for Bollinger-band based strategy:

<img src="https://github.com/mehul90/NSE_TRADER/blob/master/images/ril_1.png">

Signals for the above strategy:

<img src="https://github.com/mehul90/NSE_TRADER/blob/master/images/ril_strategy_1.png">

This uses Pandas, NumPy, NSEPy, SciKit, MatPlotLib, and a host of other python libraries.

Feel free to add your custom strategies, optimized code for fetching data, improved graph plots, etc.

I am not a python programmer, nor am I an expert in trading or technical analysis. All ideas/suggestions/improvements are welcome.
