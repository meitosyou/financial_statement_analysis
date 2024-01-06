import streamlit as st
import pandas as pd

import scoreing_AI
import get_otherdata

def main():
    # サンプルのデータフレームを作成
    #data = pd.read_csv("./analysis_results/financial_analysis_values_nikkei225.csv", header=0)
    #data_num = pd.read_csv("./analysis_results/financial_analysis_results_nikkei225.csv", header=0)
    
    # data = pd.read_csv("./analysis_results/financial_analysis_values_sp500.csv", header=0)
    # data_num = pd.read_csv("./analysis_results/financial_analysis_results_sp500.csv", header=0)
    data = pd.read_csv("./analysis_results/financial_analysis_values_japan.csv", header=0)
    data_num = pd.read_csv("./analysis_results/financial_analysis_results_japan.csv", header=0)
    # data = pd.read_csv("./analysis_results/financial_analysis_values_india.csv", header=0)
    # data_num = pd.read_csv("./analysis_results/financial_analysis_results_india.csv", header=0)
    # data = pd.read_csv("./analysis_results/financial_analysis_values_indonecia.csv", header=0)
    # data_num = pd.read_csv("./analysis_results/financial_analysis_results_indonecia.csv", header=0)

    df = pd.DataFrame(data)
    df_num = pd.DataFrame(data_num)
    # ウェブアプリケーションのタイトル
    
    # 構成銘柄
    # st.write(df["Stock"].tolist())
    # データフレームの表示
    
    st.title('データフレームの動的な表示')
    st.write('データフレーム全体:')
    st.write(df)
    

    # フィルター用のサイドバー
    st.sidebar.header('フィルター')
    select_sector = st.sidebar.multiselect("セクターを選択", df["Sector"].unique(), default=df['Sector'].unique())
    selected_cities1 = st.sidebar.multiselect('40%ルール', df['40 Percent Rule'].unique(), default=df['40 Percent Rule'].unique())
    selected_cities2 = st.sidebar.multiselect('純利益の連続増大', df['Net Income Growth'].unique(), default=df['Net Income Growth'].unique())
    selected_cities3 = st.sidebar.multiselect('ROE10%以上', df['ROE'].unique(), default=df['ROE'].unique())
    selected_cities4 = st.sidebar.multiselect('ROA5%以上', df['ROA'].unique(), default=df['ROA'].unique())
    selected_cities5 = st.sidebar.multiselect('営業キャッシュフローが正', df['Positive Cash Flow'].unique(), default=df['Positive Cash Flow'].unique())
    selected_cities6 = st.sidebar.multiselect('キャッシュフローマージン10%以上', df['Cash Flow Margin'].unique(), default=df['Cash Flow Margin'].unique())
    selected_cities7 = st.sidebar.multiselect('自己資本比率30%以上', df['Capital ratio'].unique(), default=df['Capital ratio'].unique())
    selected_cities8 = st.sidebar.multiselect('PER15倍以下と割安', df['PER'].unique(), default=df['PER'].unique())
    selected_cities9 = st.sidebar.multiselect('PBR1倍以下と割安', df['PBR'].unique(), default=df['PBR'].unique())
    selected_cities10 = st.sidebar.multiselect('ROEが増大', df['ROE_increase'].unique(), default=df['ROE_increase'].unique())
    selected_cities11 = st.sidebar.multiselect('資産が増大', df['Asset'].unique(), default=df['Asset'].unique())
    selected_cities12 = st.sidebar.multiselect('営業CFが投資CFを上回る', df['Oper_over_Invest'].unique(), default=df['Oper_over_Invest'].unique())
    selected_cities13 = st.sidebar.multiselect('純利益が4期連続プラス', df['Net Income Sign'].unique(), default=df['Net Income Sign'].unique())
    selected_cities14 = st.sidebar.multiselect('売上高が増え続ける', df['Total Revenue'].unique(), default=df['Total Revenue'].unique())
    selected_cities15 = st.sidebar.multiselect('決算後に株価が上昇している', df['profit loss'].unique(), default=df['profit loss'].unique())
    
    # 選択された都市でデータフレームを動的にフィルタリング
    filtered_df = df[
        (df['Sector'].isin(select_sector)) &
        (df['40 Percent Rule'].isin(selected_cities1)) &
        (df['Net Income Growth'].isin(selected_cities2)) &
        (df['ROE'].isin(selected_cities3)) &
        (df['ROA'].isin(selected_cities4)) &
        (df['Positive Cash Flow'].isin(selected_cities5)) &
        (df['Cash Flow Margin'].isin(selected_cities6)) &
        (df['Capital ratio'].isin(selected_cities7)) &
        (df['PER'].isin(selected_cities8)) &
        (df['PBR'].isin(selected_cities9)) &
        (df['ROE_increase'].isin(selected_cities10)) &
        (df['Asset'].isin(selected_cities11)) &
        (df['Oper_over_Invest'].isin(selected_cities12)) &
        (df['Net Income Sign'].isin(selected_cities13)) &
        (df['Total Revenue'].isin(selected_cities14)) &
        (df['profit loss'].isin(selected_cities15))
    ]

    filtered_df_num = df_num[
        (df['Sector'].isin(select_sector)) &
        (df['40 Percent Rule'].isin(selected_cities1)) &
        (df['Net Income Growth'].isin(selected_cities2)) &
        (df['ROE'].isin(selected_cities3)) &
        (df['ROA'].isin(selected_cities4)) &
        (df['Positive Cash Flow'].isin(selected_cities5)) &
        (df['Cash Flow Margin'].isin(selected_cities6)) &
        (df['Capital ratio'].isin(selected_cities7)) &
        (df['PER'].isin(selected_cities8)) &
        (df['PBR'].isin(selected_cities9)) &
        (df['ROE_increase'].isin(selected_cities10)) &
        (df['Asset'].isin(selected_cities11)) &
        (df['Oper_over_Invest'].isin(selected_cities12)) &
        (df['Net Income Sign'].isin(selected_cities13)) &
        (df['Total Revenue'].isin(selected_cities14)) &
        (df['profit loss'].isin(selected_cities15))
    ]
    # フィルタリングされたデータフレームの表示
    st.write('フィルタリングされたデータ:')
    st.write(filtered_df)
    st.write('フィルタリングされたデータ:(数値)')
    st.write(filtered_df_num)

    # ボタンを表示
    if st.button('フィルタリングされたデータのパフォーマンスを表示'):
        pl, pl_val, plt = scoreing_AI.eval_data(filtered_df, filtered_df_num)
        st.write("抽出された件数")
        st.write(len(filtered_df))
        st.write("利益を享受する株の割合")
        st.write(pl * 100)
        st.write("平均利益率")
        st.write(pl_val)
        st.pyplot(plt)

    display_ticker = st.text_input("銘柄コードを入力して下さい", value="6501.T")
    if st.button('その他の重要情報を表示'):

        st.write("配当利回り")
        dividend_yield = get_otherdata.get_dividend_yield(display_ticker)
        st.write(dividend_yield)

        st.write("下記の情報はある程度注目度の高い企業でないとそもそも情報がない")
        splits = get_otherdata.get_stock_split(display_ticker)
        st.write("株式分割情報")
        st.write(splits)

        estimate, history = get_otherdata.get_predict_data(display_ticker)
        st.write("売上などに関する予測情報")
        st.write(estimate)
        st.write("純利益の予実の歴史")
        st.write(history)
        

    ticker_code = st.text_input("株価コードを入力して下さい", value="6501.T")
    if st.button("ticker codeの株価を表示"):
        url = "https://finance.yahoo.com/quote/{}".format(ticker_code)
        if url:
            # 入力されたURLを開く
            get_otherdata.open_url_in_browser(url)
            st.success(f"Opened URL: {url}")
        else:
            st.warning("Please enter a valid URL.")

    # ユーザーにURLを入力させる
    japanese_ticker_code = st.number_input("四桁の株価コードを入力して下さい", min_value=1000, max_value=9999, value=6501)
    def add_zeros_to_first_digit(number):
        # 入力された数字が4桁でない場合はエラーを返す
        if not isinstance(number, int) or not (1000 <= number <= 9999):
            raise ValueError("Please enter a 4-digit number.")

        # 数字を文字列に変換し、最初の桁数に"000"を追加して返す
        result = str(number)[0] + "000"
        return int(result)
    
    if st.button("日本株の理論株価をサイトを表示"):
        url = "https://kabubiz.com/riron/{}/{}.php".format(add_zeros_to_first_digit(japanese_ticker_code), japanese_ticker_code)
        if url:
            # 入力されたURLを開く
            get_otherdata.open_url_in_browser(url)
            st.success(f"Opened URL: {url}")
        else:
            st.warning("Please enter a valid URL.")

    if st.button("メモ書き・保守事項の表示"):

        st.write("実際の判断は「fintech_research/投資分析」の中にあるシートを参照すること。")

        st.write("優先度高い事項")
        """
        * PSRを加える。
        * ヨーロッパの銘柄を選定できるようにする。（イギリス、フランス、ドイツあたり？）
        * 株価そのものを参照する(100株の値段が買える程度なのか)
        """

        st.write("システム保守事項は時期が来たら保守するところ")
        """
        * 現在はデータが4年分しかない前提だが、データが蓄積されてそれを活用することを想定して作り直す。
        * get_financial_statement の中に get_stock_price_index をして、株価とかPERをとる構成としている。
        * 今後、テクニカルとかPBRを加えるなら、get_stock_price_indexを増強する形で補強する。
        * profit loss を求めるために135日遅くデータ化される仕組みになっているのを解消する
        * 閾値は固定値を用いているが、自分で調整可能な形で動かせるようにするのもありかもしれない。
        * 類似する株を探す機能とかもあってもいいかもね
        """

        st.write("今後考慮していきたい変数")
        """
        (1) 加えたい変数
        * PSR = 時価総額を年間売上高で割ったもの。

        * 株式分割の有無(displayのみとした)
        * 純利益の予実(displayのみとした)
        * 配当利回り(displayのみとした)
        * 株価のトレンドとかの確認：yahoo financeより可視化
        * 理論株価＝（事業価値＋財産価値－有利子負債）÷発行済株式数（どこから数字取るべきか、、）：日本株については理論株価Webより取得
        * 理論株価Web に記載されている投資難易度

        (2) 他に考えたこと
        * 時価総額,純資産 ==> (企業の規模把握のため)
        * 理論株価は、決算書から何とか計算できないか？
        * 理論株価Web  の下余限地より低い
        * その他、株価自己回帰系のテクニカル指標
        * 社会動向的な指標(ロイターニュースと経済指標)
        * 決算書のテキストマイニングなど（現状日本株しか簡単に入手できないが。）
        * セクターベクトル（事業内容とかをテキストマイニング？）
        """

        st.write("残検証事項")
        """
        (1) 本当はシナリオ別に指標の組み合わせとか考えるべきでは？（セクター、社会動向？）
        * →　セクターごとの差を検証する。加えて、社会動向からセクターごとの予想みたいなのがあったらそれと照らし合わせてみたい。
        
        (2) ヨーロッパの銘柄もできるようにする。
        
        (3) テクニカルな指標も取り入れる PERとかPBRとかも含め 
        
        (4) 検討してきたAIはなぜ有意な差を生み出すことが難しいのか？
        * データが少ない、株価を予測するのに自己回帰系の変数を入れていない。　、
        * やり方１：条件を離散化して、それにポイントをつけて株価上昇確率をスコア化する（例えば機械学習させてSHAPとかで影響度を調べる、オッズポイントをつけて尤度を最大化するように定数係数を定める）
        * やり方２：条件を連続値のままにする、でもRFではうまくいってなかった。指標の閾値をベイズ最適？
        * ==> どちらでも、ほとんど精度の改善が見られない
        *  現状では単なる条件式絞り込みの方がうまくいっているように見える。
        """

if __name__ == '__main__':
    main()
