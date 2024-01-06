
from yahoo_fin import stock_info as si
import yfinance as yf

import webbrowser

def get_stock_split(ticker):
    stock = yf.Ticker(ticker)
    # 株式分割情報を取得
    splits = stock.splits

    if not splits.empty:
        print("株式分割が存在します。")
        print(splits)
        return splits
    else:
        print("株式分割は存在しません。")
        return None

def get_predict_data(ticker):
    # yahoo_finからデータを取得
    earnings_estimate = si.get_analysts_info(ticker)['Earnings Estimate']

    # 業績予想を表示
    print(earnings_estimate)

    # 予実が乗っている
    earnings_history = si.get_analysts_info(ticker)['Earnings History']
    print(earnings_history)
    # 日付が、決算の最新の日付と同じやつを探す。
    # そいつの予実を符号が＋であるという条件を加える。
    return earnings_estimate, earnings_history

import yfinance as yf


def get_industry(ticker):
    # yfinanceを使用して銘柄の情報を取得
    stock_info = yf.Ticker(ticker)

    # 銘柄の業種を取得
    industry = stock_info.info["industry"] #'sector'

    print(f"{ticker}の業種は: {industry}")

def get_dividend_yield(ticker):# 配当利回りを取得
    stock_info = yf.Ticker(ticker)
    dividend_yield = stock_info.info['trailingAnnualDividendYield']
    # 結果を表示
    print(f"{ticker}の配当利回り: {dividend_yield * 100:.2f}%")
    return dividend_yield * 100

def get_sector(ticker):
    # yfinanceを使用して銘柄の情報を取得
    stock_info = yf.Ticker(ticker)
    
    if "sector" in stock_info.info:
        # 銘柄の業種を取得
        sector = stock_info.info["sector"] #'sector'

        #print(f"{ticker}の業種は: {sector}")
        return sector
    else:
        return None

def open_url_in_browser(url):
    # 指定したURLを新しいウィンドウで開く
    webbrowser.open_new(url)

if __name__ == "__main__": 
    ticker_sample = "6501.T"
    # 例としてAAPL（アップル）の株式分割情報を取得
    get_stock_split(ticker_sample)

    get_predict_data(ticker_sample)

    get_industry(ticker_sample)

