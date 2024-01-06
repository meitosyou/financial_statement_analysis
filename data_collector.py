import yfinance as yf
import os
import pandas as pd
import glob

import get_tickers_code

class StockDataCollector:
    def __init__(self, folder_path="stock_data"):
        self.folder_path = folder_path
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def get_annual_income_statement(self, stock):
        annual_income_statement = stock.financials.transpose()
        if annual_income_statement.columns.empty:
            return None, f"income statement data is not available or 4 years of data is not present."
        if not 'Net Income' in annual_income_statement.columns:
            return None, "no column of Net Income"
        if not 'Total Revenue' in annual_income_statement.columns:
            return None, "no column of Total Revenue"
        return annual_income_statement, None
    

    def get_balance_sheet(self, stock):
        balance_sheet = stock.balance_sheet
        if balance_sheet.index.empty:
            return None, "balance_sheet data is not available or 4 years of data is not present."
        if not 'Common Stock Equity' in balance_sheet.index:
            return None, "no column of Common Stock Equity"
        return balance_sheet, None
    

    def get_cash_flow(self, stock):
        cash_flow = stock.cashflow
        if cash_flow.index.empty:
            return None, "cash_flow data is not available or 4 years of data is not present."
        if not 'Beginning Cash Position' in cash_flow.index:
            return None, "no column of Beginning Cash Position"
        if not 'End Cash Position' in cash_flow.index:
            return None, "no column of End Cash Position"
        if not 'Free Cash Flow' in cash_flow.index:
            return None, "no column of Free Cash Flow"
        return cash_flow, None


    def get_all(self, ticker):
        stock = yf.Ticker(ticker)
        income_statement, error = self.get_annual_income_statement(stock)
        if error:
            print(f"Skipping income statement for {ticker}: {error}")
        else:
            self.save_data(ticker, income_statement, 'annual_income_statement')

        balance_sheet, error = self.get_balance_sheet(stock)
        if error:
            print(f"Skipping balance sheet for {ticker}: {error}")
        else:
            self.save_data(ticker, balance_sheet, 'balance_sheet')

        cash_flow, error = self.get_cash_flow(stock)
        if error:
            print(f"Skipping cash flow for {ticker}: {error}")
        else:
            self.save_data(ticker, cash_flow, 'cash_flow')

    def save_data(self, ticker, data, data_type):
        folder_name = f"{self.folder_path}/{ticker}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created.")

        # 最新の日付を取得
        latest_date = pd.to_datetime(data.columns[0]).strftime('%Y%m%d') if data_type != 'annual_income_statement' else pd.to_datetime(data.index[0]).strftime('%Y%m%d')
        filename = f"{folder_name}/{data_type}_{latest_date}.csv"

        # 同名のファイルが存在しない場合、ファイルを保存
        if not os.path.exists(filename):
            data.to_csv(filename)
            print(f"{data_type.capitalize()} data saved to {filename}")
        else:
            print(f"{filename} already exists.")

    def process_ticker_list(self, ticker_list):
        for ticker in ticker_list:
            print(f"Processing {ticker}")
            self.get_all(ticker)


class StockDataAggregator:
    def __init__(self, folder_path="stock_data"):
        self.folder_path = folder_path

    def aggregate_data(self, ticker, data_type):
        files_pattern = f"{self.folder_path}/{ticker}/{data_type}_*.csv"
        files = glob.glob(files_pattern)
        
        if not files:
            print(f"No files found for {ticker} and {data_type}")
            return

        if len(files) == 1:
            if data_type == 'annual_income_statement':
                df = pd.read_csv(files[0], index_col=0)
                # df = df.T #.read_csv(files[0], index_col=0)
                # new_column_names = ["Date"] + df.columns.tolist()[1:]
                # df.columns = new_column_names
                
            else:
                df_orig = pd.read_csv(files[0], header=0)
                df = df_orig.T
                df.columns = df.iloc[0,:]
                df = df[1:]
                # new_column_names = ["Date"] + df.columns.tolist()[1:]
                # df.columns = new_column_names
            # 単一ファイルの場合はそのファイルをコピー
            # pd.read_csv(files[0])
            df.to_csv(f"{self.folder_path}/{ticker}/{data_type}.csv", index=True)
            print(f"Single file copied for {ticker} and {data_type}")

        else: # ¥ 来年以降に検討
            # 複数のファイルを結合
            data_frames = []
            for file in files:
                if data_type == 'annual_income_statement':
                    df = pd.read_csv(file, index_col=0)
                else:
                    df = pd.read_csv(file, header=0)

                data_frames.append(df)

            combined_df = pd.concat(data_frames, axis=1).drop_duplicates().sort_index()
            combined_df.to_csv(f"{self.folder_path}/{ticker}/{data_type}.csv")
            print(f"Combined file created for {ticker} and {data_type}")

    def aggregate_all_data_types_for_ticker(self, ticker):
            for data_type in ['annual_income_statement', 'balance_sheet', 'cash_flow']:
                self.aggregate_data(ticker, data_type)
            print(f"All data types aggregated for {ticker}")

    def aggregate_all_tickers(self, ticker_list):
        for ticker in ticker_list:
            self.aggregate_all_data_types_for_ticker(ticker)
        print("Aggregation completed for all tickers")





if __name__ == "__main__": 
    ### (0) ティッカーコードのリストを取得する。
    # ticker_list = ["AAPL", "MSFT", "GOOG"]  # 例としてApple, Microsoft, Googleのティッカーを使用
    # ticker_list = get_tickers_code.get_nikkei225_tickers()
    # ticker_list = get_tickers_code.get_sp500_tikcers()
    # ticker_list = get_tickers_code.get_japan_tickers()
    # ticker_list = get_tickers_code.get_nasdaq_tickers()
    # ticker_list = get_tickers_code.get_india_tickers()
    # ticker_list = get_tickers_code.get_indonecia_tickers()
    ticker_list = get_tickers_code.get_china_tickers()
    
    ### (1) yfinance からデータを取得する.（インターネット接続が必要）
    collector = StockDataCollector()
    collector.process_ticker_list(ticker_list)

    ### (2) 日付付きのファイルを集約し扱うデータを定める
    aggregator = StockDataAggregator()
    aggregator.aggregate_all_tickers(ticker_list)