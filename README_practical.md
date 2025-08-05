# データ分析環境 - 実践ガイド

## 🎯 プロジェクトの目的

このプロジェクトは、実際のデータを取り込んで分析できる統合データ分析環境を提供します。

### 主な機能

1. **データインポート** - 様々なソースからデータを取り込む
2. **データ前処理** - クリーニング、変換、統合
3. **データ分析** - 統計分析、時系列分析、ネットワーク分析
4. **可視化** - インタラクティブなグラフとダッシュボード
5. **レポート作成** - 分析結果の自動レポート生成

## 🚀 クイックスタート

### Ubuntu (WSL)環境での起動

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/Users/kazum/data-analysis-env

# 仮想環境を有効化
source venv/bin/activate

# アプリケーションを起動
streamlit run integrated_analysis_workflow.py
```

## 📊 実践的な使用例

### 1. 売上データの分析

```bash
# データインポートツールを起動
streamlit run data_importer.py
```

1. CSVファイルをアップロード（例：売上データ.csv）
2. エンコーディングを「shift-jis」に設定（日本語ファイルの場合）
3. データをプレビューして保存

### 2. 統合分析ワークフローの実行

```bash
# 統合分析ワークフローを起動
streamlit run integrated_analysis_workflow.py
```

#### ワークフローのステップ

1. **データ読み込み**
   - 保存したデータファイルを選択
   - または新規ファイルをアップロード

2. **データ探索**
   - 基本統計量の確認
   - 欠損値の可視化と処理
   - 相関分析

3. **データ分析**
   - 統計分析（t検定、回帰分析など）
   - 時系列分析（トレンド、季節性）
   - グループ分析（カテゴリ別集計）
   - ネットワーク分析（関係性の可視化）

4. **可視化**
   - 散布図、折れ線グラフ、棒グラフ
   - ヒートマップ、箱ひげ図
   - 3D散布図

5. **レポート作成**
   - 分析結果の自動レポート生成
   - Markdown形式でダウンロード
   - 処理済みデータの保存

### 3. 実データの取り込み例

#### A. Excelファイルから売上データを分析

```python
# data_importer.pyで以下を実行：
# 1. 「ファイルアップロード」タブを選択
# 2. 売上データ.xlsxをアップロード
# 3. シート名を指定（例：「2024年売上」）
# 4. データを確認して保存
```

#### B. Web APIからリアルタイムデータを取得

```python
# data_importer.pyの「Web API」タブで：
# 1. APIエンドポイントを入力
# 2. 認証情報を設定（APIキーなど）
# 3. データを取得して保存
```

#### C. データベースから直接取得

```python
# data_importer.pyの「データベース接続」タブで：
# 1. PostgreSQL/MySQLを選択
# 2. 接続情報を入力
# 3. SQLクエリを実行してデータ取得
```

## 🛠️ カスタマイズ方法

### 新しい分析機能の追加

1. `integrated_analysis_workflow.py`の「ステップ3: データ分析」セクションに追加

```python
elif analysis_type == "カスタム分析":
    st.subheader("カスタム分析")
    # ここに新しい分析ロジックを追加
```

### 新しいデータソースの追加

1. `data_importer.py`に新しいタブを追加

```python
with tab6:  # 新しいタブ
    st.header("新しいデータソース")
    # データ取得ロジックを実装
```

## 📁 ファイル構成

```
data-analysis-env/
├── venv/                          # Python仮想環境
├── data/
│   ├── raw/                      # 生データ
│   ├── processed/                # 処理済みデータ
│   └── temp/                     # 一時ファイル
├── output/                       # 分析結果の出力
├── integrated_analysis_workflow.py  # メイン分析ワークフロー
├── data_importer.py              # データインポートツール
├── data_preprocessing.py         # データ前処理ツール
├── network_demo.py              # ネットワーク分析デモ
├── graphviz_demo.py             # Graphvizデモ
├── claude_data_assistant.py     # Claude連携データアシスタント
├── requirements.txt             # 必要なPythonパッケージ
└── README_practical.md          # このファイル
```

## 🔧 トラブルシューティング

### よくある問題と解決方法

1. **日本語ファイルが文字化けする**
   - エンコーディングを「shift-jis」または「cp932」に変更

2. **メモリ不足エラー**
   - 大きなファイルは分割して処理
   - `chunksize`パラメータを使用して部分読み込み

3. **グラフが表示されない**
   - ブラウザのJavaScriptを有効化
   - 別のブラウザで試す

4. **分析結果が保存されない**
   - `data/processed/`フォルダの書き込み権限を確認
   - ディスク容量を確認

## 📚 参考資料

- [Pandas公式ドキュメント](https://pandas.pydata.org/)
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)
- [NetworkX公式ドキュメント](https://networkx.org/)
- [Plotly公式ドキュメント](https://plotly.com/python/)

## 🤝 サポート

問題が発生した場合は、以下を確認してください：

1. エラーメッセージの詳細
2. 使用しているデータの形式
3. 実行したステップの順序

より詳細なサポートが必要な場合は、エラーログと共に報告してください。
