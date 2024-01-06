import pandas as pd
import os

import get_tickers_code
import get_stock_price_index
import get_otherdata

class FinancialAnalysis:
    def __init__(self, ticker, folder_path="stock_data", internet_connect=True): # annual_income_statement, balance_sheet, cash_flow, 
        self.folder_path = folder_path
        self.ticker = ticker

        self.spa = get_stock_price_index.StockPriceAnalysis(ticker)


    def check_and_input_data(self):
        self.annual_income_statement = self.read_financial_statements(self.ticker, data_type="annual_income_statement") #annual_income_statement
        self.balance_sheet = self.read_financial_statements(self.ticker, data_type="balance_sheet") # balance_sheet
        self.cash_flow = self.read_financial_statements(self.ticker, data_type="cash_flow") # cash_flow
        
        if self.annual_income_statement is not None and self.balance_sheet is not None and self.cash_flow is not None:
            # print(self.ticker)
            # 日付の生合成をチェックし抽出
            self._date1 = self.annual_income_statement.index
            # self._date2 = self.balance_sheet.index
            # self._date3 = self.cash_flow.index
            self._date = self._date1
            
            # 財務データの抽出
            self.net_income_4_years = self.annual_income_statement['Net Income'][:]     # 純利益
            self.tot_revenue_4_years = self.annual_income_statement['Total Revenue'][:] # 総収入 = 売上高

            # self.equality_corrected = self.balance_sheet['Common Stock Equity'][:]      # 自己資本に近いもの (使わない方針)
            self.equality_corrected = self.balance_sheet["Total Equity Gross Minority Interest"][:] # 自己資本に近いもの

            self.total_assets = self.balance_sheet['Total Assets'][:] # 総資産 = 自己資本 + 負債
            self.cash_begin = self.cash_flow['Beginning Cash Position'][:] # 期首残高
            self.cash_end = self.cash_flow['End Cash Position'][:] # 期末残高
            
            self.get_operating_cash_flow()
            # self.free_cash_flow = self.cash_flow["Free Cash Flow"][:] # フリーキャッシュフロー
            # self.operating_cash_flow = self.cash_flow["Operating Cash Flow"][:] # 営業キャッシュフロー
            self.investing_cash_flow = self.cash_flow["Investing Cash Flow"][:] # 投資キャッシュフロー
            self.get_financing_cash_flow()
            # self.financing_cash_flow = self.cash_flow["Financing Cash Flow"][:] # 財務キャッシュフロー

            # self.eps = self.annual_income_statement["Basic EPS"][:]
            self.get_EPS()

            self.get_BPS()
            return True
        else:
            return False
        
    def get_operating_cash_flow(self):
        # もしOperating Cash Flowが利用可能な場合
        if "Operating Cash Flow" in self.cash_flow:# and self.cash_flow["Operating Cash Flow"]:
            self.operating_cash_flow = self.cash_flow["Operating Cash Flow"][:]
            self.free_cash_flow = self.cash_flow["Free Cash Flow"][:]
        else:
            # Operating Cash Flowが利用できない場合はFree Cash Flowを試す
            if "Free Cash Flow" in self.cash_flow:# and self.cash_flow["Free Cash Flow"]:
                self.free_cash_flow = self.cash_flow["Free Cash Flow"][:]
                self.operating_cash_flow = self.free_cash_flow
            else:
                # どちらも利用できない場合にはエラーメッセージを表示するか、何らかの処理を行う
                print("Error: Neither Operating Cash Flow nor Free Cash Flow is available.")
                self.free_cash_flow = None
                self.operating_cash_flow = None

    
    def get_financing_cash_flow(self):
        if "Financing Cash Flow" in self.cash_flow:
            self.financing_cash_flow = self.cash_flow["Financing Cash Flow"][:]
        else:
            self.financing_cash_flow = None

    def get_EPS(self):
        if "Basic EPS" in self.annual_income_statement:
            self.eps = self.annual_income_statement["Basic EPS"][:]
        elif 'Net Income' in self.annual_income_statement and "Share Issued" in self.balance_sheet:
            self.equality_corrected = self.annual_income_statement['Net Income'][:]
            self.total_stock_num = self.balance_sheet["Share Issued"][:]
            # Series1をSeries2で割る
            self.eps = self.equality_corrected.div(self.total_stock_num)
        else:
            self.eps = None

    def get_BPS(self):
        if "Total Equity Gross Minority Interest" in self.balance_sheet and "Share Issued" in self.balance_sheet:
            self.equality_corrected = self.balance_sheet["Total Equity Gross Minority Interest"][:]
            self.total_stock_num = self.balance_sheet["Share Issued"][:]
            # Series1をSeries2で割る
            self.bps = self.equality_corrected.div(self.total_stock_num)
        else:
            self.bps = None

    def read_financial_statements(self, ticker, data_type):
        files_pattern = f"{self.folder_path}/{ticker}/{data_type}.csv"
        if os.path.exists(files_pattern):
            return pd.read_csv(files_pattern, index_col=0)
        else:
            return None

    def validate_data(self):
        is_net_income_valid = len(self.net_income_4_years) >= 4 and not self.net_income_4_years.isnull().any() and all(self.net_income_4_years != 0)
        is_total_revenue_valid = len(self.tot_revenue_4_years) >= 4 and not self.tot_revenue_4_years.isnull().any() and all(self.tot_revenue_4_years != 0)
        is_price_valid = self.spa.get_kessan_price(self._date[0]) is not None and self.spa.get_next_kessan_price(self._date[0]) is not None
        is_othervalues = self.eps is not None and self.operating_cash_flow is not None and self.free_cash_flow is not None and self.financing_cash_flow is not None
        return is_net_income_valid and is_total_revenue_valid and is_price_valid and is_othervalues

    def check_40_percent_rule(self, thres =0.40):
        val = self.revenue_growth_rate + self.profit_growth_rate
        return val, val >= 0.4

    def check_net_income_growth(self, growth_years=3):
        return self.net_income_4_years.to_list(), all(self.net_income_4_years[i] > self.net_income_4_years[i+1] for i in range(growth_years))


    def check_roe(self, thres=0.10):
        val = (self.net_income_4_years[0] / self.equality_corrected[0])
        return val, val >= thres

    def check_roa(self, thres=0.05):
        val = (self.net_income_4_years[0] / self.total_assets[0])
        return val, val >= thres

    def check_positive_cash_flow(self, thres = 0):
        val2 = self.free_cash_flow[0]
        val1 = self.operating_cash_flow[0]
        return val1, val1 >= thres or val2 >= thres

    def check_cash_flow_margin(self, thres = 0.1):
        val = (self.free_cash_flow[0] / self.tot_revenue_4_years[0])
        return val, val >= thres

    def check_per(self, thres=15):
        start_price = self.spa.get_kessan_price(kessan_day=self._date[0])
        eps = self.eps[0]
        per = start_price / eps
        return per, per <= thres
    
    
    def check_profit_loss(self, thres=0):
        result_pl, is_profit = self.spa.get_price_change(kessan_day=self._date[0])
        return result_pl, is_profit

    def check_total_capital(self, thres=0.3):
        # print(self.total_capital[0])
        capital_adequacy_ratio = (self.equality_corrected[0] / self.total_assets[0])
        return capital_adequacy_ratio, capital_adequacy_ratio >= thres

    # ここからが新設の変数
    def check_pbr(self, thres=1.0):
        start_price = self.spa.get_kessan_price(kessan_day=self._date[0])
        bps = self.bps[0]
        per = start_price / bps
        return per, per <= thres
    
    def check_roe_increase(self):
        roe_after = (self.net_income_4_years[0] / self.equality_corrected[0])
        roe_before =  (self.net_income_4_years[1] / self.equality_corrected[1])
        return roe_after - roe_before, roe_after >= roe_before
    
    def check_asset_increse(self):
        # capital_adequacy_ratio = (self.total_capital[0] / self.total_assets[0])
        #asset_after  = self.total_assets[0]
        #asset_before = self.total_assets[1]
        asset_after = self.cash_end[0]
        asset_before = self.cash_begin[0]
        return asset_after - asset_before, asset_after >= asset_before

    def check_operating_over_investing(self):
        operating = self.operating_cash_flow[0]
        investing = self.investing_cash_flow[0]
        return operating - investing, operating >= investing
    
    def check_net_income_plus(self, growth_years=4):
        return self.net_income_4_years.to_list(), all(self.net_income_4_years[i] > 0 for i in range(growth_years))

    # 重要度が低いと判断した
    def check_tot_revenue_growth(self, growth_years=3):
        return self.tot_revenue_4_years.to_list(), all(self.tot_revenue_4_years[i] > self.tot_revenue_4_years[i+1] for i in range(growth_years))


    def analyze(self):
        if self.check_and_input_data():
            if self.validate_data():
                # 収益成長率と利益成長率の計算
                self.revenue_growth_rate = (self.tot_revenue_4_years[0] - self.tot_revenue_4_years[1]) / self.tot_revenue_4_years[1]
                self.profit_growth_rate = (self.net_income_4_years[0] - self.net_income_4_years[1]) / self.net_income_4_years[1]

                # 40%ルールのチェック
                _40_percent_rule_result, is_40_percent_rule_passed = self.check_40_percent_rule()

                # 純利益の成長をチェック
                net_income_growth_result, is_net_income_growing = self.check_net_income_growth()

                # ROE (自己資本利益率) のチェック
                roe_result, is_roe_high = self.check_roe()

                # ROA (総資産利益率) のチェック
                roa_result, is_roa_high = self.check_roa()

                # ポジティブなキャッシュフローのチェック
                positive_cash_flow_result, is_cash_flow_positive = self.check_positive_cash_flow()

                # キャッシュフローマージンのチェック
                cash_flow_margin_result, is_cash_flow_margin_high = self.check_cash_flow_margin()

                # PERのチェック
                PER_result, is_PER_low = self.check_per()

                # 自己資本比率のチェック
                capital_adequacy_ratio, is_capital_high = self.check_total_capital()

                PBR_result, is_PBR_low = self.check_pbr()

                roe_increase, is_roe_increase = self.check_roe_increase()

                asset_increase, is_asset_increase = self.check_asset_increse()

                compare_operate_invest, is_operating_over_increase = self.check_operating_over_investing()
                
                net_income_sign_result, is_net_income_positive = self.check_net_income_plus()

                tot_revenue_growth_result, is_tot_revenue_growing = self.check_tot_revenue_growth()


                # 損益のチェック
                result_pl, is_profit = self.check_profit_loss()

                sector = get_otherdata.get_sector(ticker=self.ticker)
                # 分析結果の集約と表示
                results = {
                    "Stock": (self.ticker, self.ticker),
                    "Date": (self._date[0], self._date[0]),
                    "Sector": (sector, sector),
                    "40 Percent Rule": (is_40_percent_rule_passed, _40_percent_rule_result),
                    "Net Income Growth": (is_net_income_growing, net_income_growth_result),
                    "ROE": (is_roe_high, roe_result),
                    "ROA": (is_roa_high, roa_result),
                    "Positive Cash Flow": (is_cash_flow_positive, positive_cash_flow_result),
                    "Cash Flow Margin": (is_cash_flow_margin_high, cash_flow_margin_result),
                    "PER": (is_PER_low, PER_result),
                    "Capital ratio": (is_capital_high, capital_adequacy_ratio),
                    "PBR": (is_PBR_low, PBR_result),
                    "ROE_increase": (is_roe_increase, roe_increase),
                    "Asset": (is_asset_increase, asset_increase),
                    "Oper_over_Invest": (is_operating_over_increase, compare_operate_invest),
                    "Net Income Sign": (is_net_income_positive, net_income_sign_result),
                    "Total Revenue": (is_tot_revenue_growing, tot_revenue_growth_result),
                    "profit loss": (is_profit, result_pl),
                }

                return results
            else:
                print("Data validation failed.")
                return {}
        else:
            print(f"Data not available for ticker: {self.ticker}")
            return {}
        

import pandas as pd

def analyze_all_tickers(ticker_list, ticker_list_name):
    eval_results = {}
    eval_values = {}
    i = 0
    for ticker in ticker_list:
        fa = FinancialAnalysis(ticker=ticker)
        financial_evals = fa.analyze()

        if financial_evals:  # データが存在する場合のみ処理
            eval_results[i] = {k: v[1] for k, v in financial_evals.items()}
            eval_values[i] = {k: v[0] for k, v in financial_evals.items()}
            i += 1
        else:
            print(f"Skipping analysis for {ticker} due to missing data.")

    # ブール値の評価結果をデータフレームに変換
    df_results = pd.DataFrame(eval_results).T
    df_values = pd.DataFrame(eval_values).T

    # データフレームをCSVファイルとして保存
    df_results.to_csv('./analysis_results/financial_analysis_results_{}.csv'.format(ticker_list_name), index=False)
    df_values.to_csv('./analysis_results/financial_analysis_values_{}.csv'.format(ticker_list_name), index=False)

    return df_results, df_values

if __name__ == "__main__": 
    ### (0) ティッカーコードのリストを取得する。
    # ticker_list = ["AAPL", "MSFT", "GOOG"]  # 例としてApple, Microsoft, Googleのティッカーを使用
    # ticker_list_name = "nikkei225"
    # ticker_list = get_tickers_code.get_nikkei225_tickers()
    # ticker_list_name = "sp500"
    # ticker_list = get_tickers_code.get_sp500_tikcers()
    # ticker_list_name = "japan"
    # ticker_list = get_tickers_code.get_japan_tickers()
    # ticker_list_name = "nasdaq"
    # ticker_list = get_tickers_code.get_nasdaq_tickers()
    # ticker_list_name = "india"
    # ticker_list = get_tickers_code.get_india_tickers()
    # ticker_list_name = "indonecia"
    # ticker_list = get_tickers_code.get_indonecia_tickers()

    ticker_list_name = "china"
    ticker_list = get_tickers_code.get_china_tickers()


    """
    ### () ある銘柄について財務諸表から評価を行う。
    ticker = ticker_list[0]
    fa = FinancialAnalysis(ticker=ticker)
    # 生のデータをDBに保存するのか？それとも判定結果だけ保存するのか？
    financial_evals = fa.analyze()
    print(ticker)
    print(financial_evals)
    """

    ### リストにあるすべての銘柄について財務諸表から評価を行う。
    all_results = analyze_all_tickers(ticker_list, ticker_list_name)

    # ¥ 複数年になったときでも対応できるように改造