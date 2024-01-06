# TBA

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay



def train_decision_tree(X, y, max_depth=5, test_size=0.2, random_state=None):
    """
    決定木モデルを訓練し、テストデータでの精度を計算して可視化します。

    Parameters:
    - X: 説明変数のデータフレーム
    - y: 目的変数のデータフレームまたはシリーズ
    - max_depth: 決定木の深さ（デフォルトは5）
    - test_size: テストデータの割合（デフォルトは0.2）
    - random_state: 乱数のシード（デフォルトはNone）

    Returns:
    - accuracy: テストデータでの予測精度
    """
    # データの分割 (訓練データとテストデータ)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # 決定木のモデルの作成と訓練
    clf = DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(X_train, y_train)

    # テストデータでの予測
    y_pred = clf.predict(X_test)

    # 精度の計算
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # 混同行列の計算
    cm = confusion_matrix(y_test, y_pred)

    # 混同行列の可視化
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
    disp.plot(cmap='Blues', values_format='d')
    plt.title('Confusion Matrix')
    plt.show()
    """"
    # 樹形図の出力  
    plt.figure(figsize=(20, 10))
    plot_tree(clf, filled=True, feature_names=X.columns, class_names=str(clf.classes_))
    plt.show()
    """
    # 樹形図の出力
    plt.figure(figsize=(20, 10))
    plot_tree(clf, filled=True, feature_names=X.columns, class_names=[str(c) for c in clf.classes_])
    plt.show()

    # 各変数の重要度の取得
    feature_importance = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("Feature Importance:")
    print(feature_importance)

    # 各変数の重要度を棒グラフで表示
    plt.figure(figsize=(12, 6))
    feature_importance.plot(kind='bar')
    plt.title('Feature Importance')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.tight_layout()  # グラフがはみ出ないように調整

    plt.show()



import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def train_lightgbm(X, y, test_size=0.2, random_state=None):
    """
    LightGBMモデルを訓練し、テストデータでの精度と特徴の重要度を表示します。

    Parameters:
    - X: 説明変数のデータフレーム
    - y: 目的変数のデータフレームまたはシリーズ
    - test_size: テストデータの割合（デフォルトは0.2）
    - random_state: 乱数のシード（デフォルトはNone）

    Returns:
    - accuracy: テストデータでの予測精度
    - feature_importance: 各変数の重要度
    """
    # データの分割 (訓練データとテストデータ)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # LightGBMのデータセットに変換
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # パラメータの設定
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'min_data_in_leaf': 20,  # 例として追加したパラメータ
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }


    # モデルの訓練
    num_round = 100
    # モデルの訓練
    bst = lgb.train(params, train_data, num_boost_round=num_round, valid_sets=[test_data], 
                    callbacks=[lgb.early_stopping(stopping_rounds=10)])

    # テストデータでの予測
    y_pred_prob = bst.predict(X_test, num_iteration=bst.best_iteration)
    y_pred = [1 if prob > 0.5 else 0 for prob in y_pred_prob]

    # 精度の計算
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # 混同行列の計算
    cm = confusion_matrix(y_test, y_pred)

    # 混同行列の可視化
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
    disp.plot(cmap='Blues', values_format='d')
    plt.title('Confusion Matrix')
    plt.show()

    # 特徴の重要度の表示
    plt.figure(figsize=(10, 8))
    lgb.plot_importance(bst, importance_type='split', figsize=(10, 8))
    plt.show()

    return accuracy

def eval_data(df, df_num):
    print(df["profit loss"])
    print(df_num)
    # データ自体の性質評価
    profiting_ratio = df["profit loss"].mean()
    profiting_quantity_ratio = df_num["profit loss"].mean()
    # print(profiting_ratio, profiting_quantity_ratio)

    plt.figure(figsize=(10, 8))
    plt.hist(df_num["profit loss"])
    # plt.show()
    # data = data.set_index("Stock")
    # data.drop(columns=["Stock"])
    
    return profiting_ratio, profiting_quantity_ratio , plt

if __name__ == "__main__": 

    # CSVファイルのインポート
    # data_num = pd.read_csv("./analysis_results/financial_analysis_results_nikkei225.csv")
    # data = pd.read_csv("./analysis_results/financial_analysis_values_nikkei225.csv", header=0)
    # data_num = pd.read_csv("./analysis_results/financial_analysis_results_sp500.csv")
    # data = pd.read_csv("./analysis_results/financial_analysis_values_sp500.csv", header=0)
    data_num = pd.read_csv("./analysis_results/financial_analysis_results_japan.csv")
    data = pd.read_csv("./analysis_results/financial_analysis_values_japan.csv", header=0)
    
    profiting_ratio, profiting_quantity_ratio, plt = eval_data(data, data_num)

    print(profiting_ratio, profiting_quantity_ratio)
    plt.show()

    # 取得したデータを機械学習できるように加工
    columns_to_drop = ['Stock', 'Date', 'profit loss']
    X = data.drop(columns_to_drop, axis=1).astype(float)
    y = data['profit loss'].astype(float)
    print(X)
    print(y)

    # 機械学習の適用
    # 決定木
    train_decision_tree(X, y)
    # lightGBM
    train_lightgbm(X, y)


    # 機械学習がprofitと判断したのみ投資をした場合のパフォーマンス
    # 条件を全て満たすもののみに投資した場合のパフォーマンス

