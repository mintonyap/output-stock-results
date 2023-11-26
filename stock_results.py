import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import datetime

from pandas_datareader import data as pdr
from pandas_market_calendars import get_calendar

class Stock:
    def __init__(self, ticker, entry_price, date_of_execution):
        yf.pdr_override()
        self.ticker = ticker
        self.entry_price = entry_price
        self.date_now = str(datetime.date.today())
        self.date_of_execution = datetime.datetime.strptime(date_of_execution, "%Y-%m-%d")
        self.number_of_holding_days = self.calculate_holding_days()
        self.number_of_trading_days = self.get_trading_days()
        self.stock_prices = pdr.get_data_yahoo(self.ticker, start = date_of_execution, end = self.date_now)['Adj Close']
        self.stock_prices = self.stock_prices[self.stock_prices.index.date >= self.date_of_execution.date()]
        self.last_prices = 0
        if not self.stock_prices.empty:
            self.last_price = self.stock_prices.iloc[-1]
        self.p_and_l = self.calculate_p_and_l()
        self.annualized_return = self.calculate_annualized_return()
        self.total_return = self.calculate_total_return()
        self.daily_percent_change = self.stock_prices.pct_change()
        self.sharpe = self.calculate_sharpe()
        self.cumsum = self.daily_percent_change.cumsum().apply(np.exp)
        self.max_gross_performance = self.cumsum.cummax()
        self.drawdown = self.max_gross_performance - self.cumsum
        self.max_drawdown_percentage = round((self.drawdown.max()*100), 2)
        self.compounded_annual_growth_rate_days = len(self.stock_prices) - 1
        if self.compounded_annual_growth_rate_days != 0:
            self.compounded_annual_growth_rate = round(((((self.stock_prices[-1]) / (self.stock_prices[0]))**(365.0/self.compounded_annual_growth_rate_days))- 1), 2)
        else:
            self.compounded_annual_growth_rate = None
    
    def calculate_p_and_l(self):
        p_and_l = self.last_price - self.entry_price
        if self.ticker.endswith('.SI'):
            p_and_l *= 100
        return p_and_l

    def calculate_holding_days(self):
        current_date = datetime.datetime.now()
        holding_days = (current_date - self.date_of_execution).days
        return holding_days
    
    def get_trading_days(self):
        exchange='NYSE'
        if self.ticker.endswith('.SI'):
            exchange='XSES'
        exchange_calendar = get_calendar(exchange)

        start_date = self.date_of_execution
        end_date = pd.to_datetime(datetime.datetime.now().strftime('%Y-%m-%d'))

        trading_days = exchange_calendar.valid_days(start_date, end_date)
        num_trading_days = len(trading_days)

        return num_trading_days
    
    def calculate_total_return(self):
        percentage_return = self.p_and_l / self.entry_price * 100
        if self.ticker.endswith('.SI'):
            percentage_return /= 100
        return round(percentage_return, 2)
    
    def calculate_annualized_return(self):
        percentage_return = self.p_and_l / self.entry_price
        if self.ticker.endswith('.SI'):
            percentage_return /= 100
        # annualized_return = ((1 + percentage_return) ** (365 / self.number_of_holding_days)) - 1
        annualized_return = percentage_return * np.sqrt(252)
        return annualized_return
    
    def calculate_sharpe(self):
        sharpe = self.daily_percent_change.mean() / self.daily_percent_change.std() * np.sqrt(self.number_of_trading_days) #252
        # if sharpe.isna():
        #     sharpe = 0
        return round(sharpe, 2)
    
    def calculate_max_drawdown(self):
        return self.max_drawdown_percentage
    
    def compounded_annual_growth_rate(self):
        return self.compounded_annual_growth_rate

stocks_data = [
    {"ticker": "D05.SI", "entry_price": 30.70, "date_of_execution": "2023-05-17"},
    {"ticker": "U11.SI", "entry_price": 27.63, "date_of_execution": "2023-05-17"},
    {"ticker": "AAPL", "entry_price": 179.21, "date_of_execution": "2023-08-08"},
    {"ticker": "AEHR", "entry_price": 41.22, "date_of_execution": "2023-08-17"},
    {"ticker": "AMD", "entry_price": 97.10, "date_of_execution": "2023-09-21"},
    {"ticker": "AVGO", "entry_price": 804.89, "date_of_execution": "2023-09-21"},
    {"ticker": "CMG", "entry_price": 1853.24, "date_of_execution": "2023-09-25"},
    {"ticker": "COST", "entry_price": 539.24, "date_of_execution": "2023-08-21"},
    {"ticker": "DHI", "entry_price": 111.57, "date_of_execution": "2023-09-15"},
    {"ticker": "GOOGL", "entry_price": 121.77, "date_of_execution": "2023-10-26"},
    {"ticker": "MCD", "entry_price": 279.97, "date_of_execution": "2023-09-01"},
    {"ticker": "MELI", "entry_price": 1090.10, "date_of_execution": "2023-07-10"},
    {"ticker": "META", "entry_price": 285.26, "date_of_execution": "2023-10-26"},
    {"ticker": "MSFT", "entry_price": 318.77, "date_of_execution": "2023-09-22"},
    {"ticker": "NVDA", "entry_price": 424.73, "date_of_execution": "2023-08-10"},
    {"ticker": "NVDA", "entry_price": 415.20, "date_of_execution": "2023-09-21"},
    {"ticker": "NVDA", "entry_price": 401.16, "date_of_execution": "2023-10-26"},
    {"ticker": "PLTR", "entry_price": 15.25, "date_of_execution": "2023-08-10"},
    {"ticker": "QQQ", "entry_price": 367.85, "date_of_execution": "2023-08-10"},
    {"ticker": "QQQ", "entry_price": 359.59, "date_of_execution": "2023-09-21"},
    {"ticker": "QQQ", "entry_price": 342.56, "date_of_execution": "2023-10-26"},
    {"ticker": "RACE", "entry_price": 297.92, "date_of_execution": "2023-09-07"},
    {"ticker": "SPY", "entry_price": 444.52, "date_of_execution": "2023-08-12"}, # 439.56 
    {"ticker": "SPY", "entry_price": 434.53, "date_of_execution": "2023-09-21"},
    {"ticker": "SPY", "entry_price": 411.99, "date_of_execution": "2023-10-26"},
    {"ticker": "TSLA", "entry_price": 205.32, "date_of_execution": "2023-10-26"},
    {"ticker": "UNH", "entry_price": 464.05, "date_of_execution": "2023-07-07"}
]

stocks_list = [Stock(stock_data["ticker"], stock_data["entry_price"], stock_data["date_of_execution"]) for stock_data in stocks_data]

data = {
    'Entry Price': [stock.entry_price for stock in stocks_list],
    'Last Price': [stock.last_price for stock in stocks_list],
    'P&L': [stock.p_and_l for stock in stocks_list],
    'Simple Return %': [stock.total_return for stock in stocks_list],
    # 'Annualized Return %': [stock.annualized_return for stock in stocks_list], # skip first 
    'Execution Date': [stock.date_of_execution.strftime('%Y-%m-%d') for stock in stocks_list],
    'Holding Days': [stock.number_of_holding_days for stock in stocks_list],
    'Trading Days': [stock.number_of_trading_days for stock in stocks_list],
    'Sharpe': [stock.sharpe for stock in stocks_list],
    'Max Drawdown %': [stock.max_drawdown_percentage for stock in stocks_list],
    'CAGR': [stock.compounded_annual_growth_rate for stock in stocks_list]
}

df = pd.DataFrame(data, index=[stock.ticker for stock in stocks_list])
df = df.round(2)
df = df.reset_index().rename(columns={'index': 'Symbol'})
today = datetime.datetime.today()
print("Total number of signalled stocks:", len(stocks_data))
print("Result as of", today)
date = datetime.datetime.today().date()
# print(df) # 

fig, ax = plt.subplots(figsize=(20, 15))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=['#f2f2f2']*len(df.columns))
plt.savefig(f'results_{date}.png', bbox_inches='tight', pad_inches=0.05)
plt.show()

sorted_df = df.sort_values(by=['Execution Date', 'Simple Return %'], ascending=[False, False])
print(sorted_df)

df.describe()
df["Simple Return %"].describe()