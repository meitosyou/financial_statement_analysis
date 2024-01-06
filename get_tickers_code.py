import pandas as pd

def get_sp500_tikcers():# WikipediaからS&P 500の銘柄リストを取得
    sp500_table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_tickers = sp500_table[0]['Symbol']
    return sp500_tickers


def get_nikkei225_tickers():
    # 指定されたURLから日経225の銘柄リストを取得
    #nikkei225_table = pd.read_html('https://topforeignstocks.com/indices/the-components-of-the-nikkei-225-index/')
    #nikkei225_tickers = nikkei225_table[0]['Code']
    # 日本の株式市場のティッカーにはサフィックスが必要な場合がある
    #nikkei225_tickers = [str(ticker) + '.T' for ticker in nikkei225_tickers]
    nikkei225 = pd.read_excel("./tickers_list/Japan-Nikkei-225-Index-Constituents-Jan-1-2021.xlsx", header=0)
    nikkei225_tickers = [str(ticker) + '.T' for ticker in nikkei225["Code"].tolist()]
    return nikkei225_tickers


def get_nasdaq_tickers():
    ### nasdaqst = pd.read_csv("nasdaq_stock.csv", header=0)
    nasdaqst = pd.read_excel("./tickers_list/nasdaq_stock.xlsx", header=0)
    ### 株コード "NA" はnanと認識されてしまうので、とりあえず取り除きました。
    ### 株コード "TRUE" は True というブール変数と認識されてしまうので、とりあえず取り除きました。
    nasdaqst_tickers = nasdaqst["Symbol"]
    return nasdaqst_tickers

def get_japan_tickers():
    jpst = pd.read_excel("./tickers_list/japan_stock.xlsx", header=0)
    jpst_tickers = jpst["コード"]
    jpst_tickers = [str(ticker) + '.T' for ticker in jpst_tickers]
    return jpst_tickers

def get_india_tickers():
    idst = pd.read_excel("./tickers_list/india_stock_original.xlsx", header = 0)
    idst_tickers = idst["Symbol"]
    idst_tickers = [str(ticker) + '.NS' for ticker in idst_tickers]
    return idst_tickers

def get_indonecia_tickers():
    idnst = pd.read_excel("./tickers_list/indonecia_stock.xlsx", header=0)
    idnst_tickers = idnst["Kode"]
    idnst_tickers = [str(ticker) + '.JK' for ticker in idnst_tickers]
    return idnst_tickers

def get_china_tickers():
    china = pd.read_excel("./tickers_list/china_stock.xlsx", header=0)
    china_tickers = china["コード"]
    china_tickers_mod = china_tickers[1::2]
    def format_number_to_digits(number, digit_count=4):
        """
        数字を指定した桁数になるようにゼロで埋めた文字列に変換する関数。
        小数部は無視されます。

        :param number: 変換したい数字
        :param digit_count: 桁数
        :return: ゼロで埋めた文字列
        """
        # 整数部を指定した桁数になるようにゼロで埋める
        formatted_integer = str(int(number)).zfill(digit_count)

        return formatted_integer
    
    china_tickers_mod2 = [format_number_to_digits(ticker) + '.HK' for ticker in china_tickers_mod]
    # china_tickers_mod = china_tickers[1::2]
    return china_tickers_mod2

# tikcers_list = get_china_tickers()
#print(tikcers_list)