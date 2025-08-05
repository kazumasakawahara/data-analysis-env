# データ分析統合環境

実際のデータを取り込んで分析できる統合データ分析環境です。

## 🚀 クイックスタート

### Ubuntu (WSL)環境での起動

```bash
# プロジェクトディレクトリに移動
cd /mnt/c/Users/kazum/data-analysis-env

# 仮想環境を有効化
source venv/bin/activate

# メインアプリケーションを起動
streamlit run integrated_analysis_workflow.py
```

## 📊 主要アプリケーション

### 1. 統合分析ワークフロー
```bash
streamlit run integrated_analysis_workflow.py
```
データの読み込みから分析、可視化、レポート作成まで一貫して実行できます。

### 2. データインポートツール
```bash
streamlit run data_importer.py
```
様々なソース（ファイル、データベース、API）からデータを取り込みます。

### 3. データ前処理ツール
```bash
streamlit run data_preprocessing.py
```
データのクリーニング、変換、欠損値処理を行います。

### 4. Claudeデータアシスタント
```bash
streamlit run claude_data_assistant.py
```
自然言語でデータ分析の指示ができます（要APIキー）。

## 📁 ディレクトリ構成

```
data-analysis-env/
├── data/                          # データディレクトリ
│   ├── raw/                      # 生データ
│   ├── processed/                # 処理済みデータ
│   └── temp/                     # 一時ファイル
├── output/                       # 分析結果の出力
├── integrated_analysis_workflow.py  # メイン分析ワークフロー
├── data_importer.py              # データインポートツール
├── data_preprocessing.py         # データ前処理ツール
├── claude_data_assistant.py      # Claude連携アシスタント
├── claude_network_app.py         # Claude連携ネットワーク分析
├── requirements.txt              # 必要なPythonパッケージ
├── venv/                         # Python仮想環境
└── demo_archive/                 # アーカイブしたデモファイル
```

## 🛠️ セットアップ

### 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### 環境変数の設定（Claude API使用時）

```bash
cp .env.example .env
# .envファイルにANTHROPIC_API_KEYを設定
```

## 📚 詳細ドキュメント

- [実践ガイド](README_practical.md) - 具体的な使用例とカスタマイズ方法

## 🤝 トラブルシューティング

### ポートが使用中の場合
```bash
streamlit run app.py --server.port 8502
```

### 日本語ファイルの文字化け
データインポート時にエンコーディングを「shift-jis」に設定してください。

### メモリ不足
大きなファイルは分割して処理するか、`data/temp/`フォルダを定期的にクリアしてください。
