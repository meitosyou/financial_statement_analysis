import yfinance as yf
import pandas as pd


class StockPriceAnalysis:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_kessan_price(self, kessan_day):
        # 指定された決算日から株価を取得
        start_period = pd.Timestamp(kessan_day) + pd.Timedelta(days=30)
        end_period = pd.Timestamp(kessan_day) + pd.Timedelta(days=45)
        start_history = self.stock.history(start=start_period, end=end_period)['Close']
        if start_history.empty:
            return None
        else:
            return start_history.iloc[-1]
    
    def get_next_kessan_price(self, kessan_day):
        start_period = pd.Timestamp(kessan_day) + pd.Timedelta(days=120)
        end_period = pd.Timestamp(kessan_day) + pd.Timedelta(days=135)
        end_history = self.stock.history(start=start_period, end=end_period)['Close']
        if end_history.empty:
            return None
        else:
            return end_history.iloc[-1]
    
    def get_price_change(self, kessan_day):
        start_price = self.get_kessan_price(kessan_day)
        end_price = self.get_next_kessan_price(kessan_day)
        if start_price is not None and end_price is not None:
            # 株価上昇率の計算
            rising_percentage = (end_price - start_price) / start_price * 100
            # 上昇かどうか
            rise_or_fall = (rising_percentage >= 0)
            return rising_percentage, rise_or_fall
        else:
            return None     
