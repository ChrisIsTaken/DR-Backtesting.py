import pandas as pd
from backtesting import Strategy
from backtesting import Backtest

# Load data from CSV file into a DataFrame
#data = pd.read_csv("data.csv", header=None, parse_dates=[['Date', 'Time']], names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])
#data = pd.read_csv("data.csv", index_col=['Date', 'Opentime'], parse_dates=True)
data = pd.read_csv("data.csv", parse_dates=[['Date', 'Time']], names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"])
#data.set_index(['Date', 'Time'], inplace=True)

# Define your strategy
class MyStrategy(Strategy):
    def init(self):
        print("Reached init(self)")

    def next(self):
        print("Reached next(self")
        # Your strategy logic here
        # For example, you can use the data to generate signals
        

# Create a Backtest object using the data and the strategy
bt = Backtest(data, MyStrategy, cash=100000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()
