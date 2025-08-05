# データ分析環境（NetworkX + Graphviz + Streamlit）

このプロジェクトは、DevContainerを使用してNetworkX、Graphviz、Streamlitなどのデータ分析ツールをすぐに使える環境です。

## 🚀 使い方

### 1. 事前準備
- Docker Desktop をインストールしてください
- VSCode または Cursor をインストールしてください
- VSCode/Cursor の拡張機能「Dev Containers」をインストールしてください

### 2. 環境の起動
1. VSCode/Cursor でこのフォルダ（`C:\Users\kazum\data-analysis-env`）を開く
2. 左下の緑色のボタンをクリックし、「Reopen in Container」を選択
3. 初回は環境構築に数分かかります

### 3. サンプルアプリの実行

#### NetworkXデモ
```bash
streamlit run network_demo.py
```

#### Graphvizデモ
```bash
streamlit run graphviz_demo.py
```

#### Claude連携アプリ
```bash
streamlit run claude_network_app.py
```

#### データ前処理アプリ
```bash
streamlit run data_preprocessing.py
```

#### Claudeデータ分析アシスタント
```bash
streamlit run claude_data_assistant.py
```

ブラウザが自動的に開き、`http://localhost:8501` でアプリが表示されます。

## 🧹 データ前処理機能

### データフォルダ構成
```
data/
├── raw/          # 元データを配置
├── processed/    # 前処理済みデータ
└── temp/         # 一時ファイル
```

### 前処理アプリの機能
`data_preprocessing.py` では以下の前処理が可能です：
- **データ診断**: データ型、欠損値、統計情報の確認
- **欠損値処理**: 削除、平均値/中央値/最頻値での補完
- **データ型変換**: 数値、文字列、日付型への変換
- **異常値検出**: IQR法、標準偏差法での検出と処理
- **処理済みデータの保存**: CSV、Excel、JSON形式での出力

### Claudeによる前処理支援
`claude_data_assistant.py` を使用すると、Claudeに自然な言葉で依頼できます：
- 「欠損値の傾向を分析して」
- 「外れ値を検出して可視化して」
- 「このデータに適した前処理を提案して」
- 「ネットワーク分析用にデータを変換して」

## 🤖 Claude連携機能

### 1. Claude API連携
`claude_network_app.py` を使用すると、Claudeと対話しながらネットワーク分析ができます。

#### 使い方：
1. [Anthropic Console](https://console.anthropic.com/) でAPIキーを取得
2. アプリのサイドバーにAPIキーを入力
3. チャット欄で質問（例：「10個のノードを持つランダムグラフを作成して」）

#### 環境変数での設定：
```bash
# .envファイルを作成
cp .env.example .env
# .envファイルにAPIキーを記入
```

### 2. Claude Desktop連携（MCP）
`mcp_integration.py` で設定方法を確認できます。

Claude Desktopアプリと連携することで：
- 環境情報の確認
- コードの実行依頼
- ファイルの操作

などが自然な対話形式で行えます。

## 📁 ファイル構成

```
data-analysis-env/
├── .devcontainer/
│   ├── devcontainer.json    # DevContainerの設定
│   └── Dockerfile           # 環境のベースイメージ設定
├── data/                    # データフォルダ
│   ├── raw/                # 元データ
│   ├── processed/          # 処理済みデータ
│   └── temp/               # 一時ファイル
├── requirements.txt         # Pythonパッケージのリスト
├── network_demo.py         # NetworkXのデモアプリ
├── graphviz_demo.py        # Graphvizのデモアプリ
├── claude_network_app.py   # Claude API連携アプリ
├── data_preprocessing.py   # データ前処理アプリ
├── claude_data_assistant.py # Claudeデータ分析アシスタント
├── mcp_integration.py      # MCP連携説明アプリ
├── .env.example           # 環境変数のテンプレート
└── README.md              # このファイル
```

## 🛠️ インストールされているツール

### データ分析
- **NumPy**: 数値計算の基礎ライブラリ
- **Pandas**: データ分析・操作ツール
- **Matplotlib**: グラフ描画ライブラリ
- **Seaborn**: 統計的グラフ描画

### ネットワーク分析
- **NetworkX**: グラフ/ネットワーク分析
- **Graphviz**: グラフ可視化ツール

### Web表示
- **Streamlit**: Pythonで簡単にWebアプリを作成
- **Plotly**: インタラクティブなグラフ作成

### AI連携
- **Anthropic**: Claude API クライアント

### その他
- **Jupyter**: ノートブック環境
- **SciPy**: 科学技術計算
- **scikit-learn**: 機械学習ライブラリ

## 💡 自分のコードを書く

新しいPythonファイルを作成して、以下のようにStreamlitアプリを作れます：

```python
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("私のネットワーク分析アプリ")

# ここにコードを書く
```

実行：
```bash
streamlit run あなたのファイル名.py
```

## 🔧 トラブルシューティング

### ポート8501が使用中の場合
別のポートを指定して実行：
```bash
streamlit run network_demo.py --server.port 8502
```

### パッケージを追加したい場合
1. `requirements.txt` にパッケージ名を追加
2. コンテナ内で `pip install -r requirements.txt` を実行

### Claude API連携でエラーが出る場合
- APIキーが正しいか確認
- インターネット接続を確認
- APIの利用制限に達していないか確認

### データが読み込めない場合
- ファイルのエンコーディングを確認（日本語はShift-JISの可能性）
- CSVの区切り文字を確認（タブ区切りの可能性）
- Excelファイルの場合、シート名を確認

## 📚 参考リンク
- [NetworkX ドキュメント](https://networkx.org/)
- [Graphviz ドキュメント](https://graphviz.org/)
- [Streamlit ドキュメント](https://streamlit.io/)
- [Anthropic API ドキュメント](https://docs.anthropic.com/)
- [Pandas ドキュメント](https://pandas.pydata.org/)