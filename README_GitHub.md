# NetworkX + Graphviz データ分析環境

DevContainerを使用したPythonデータ分析環境です。NetworkX、Graphviz、Streamlitを使用したネットワーク分析と、Claude AIとの連携によるデータ前処理支援機能を提供します。

## 🌟 特徴

- 🐳 **DevContainer対応**: VSCode/Cursorで即座に開発環境構築
- 🕸️ **ネットワーク分析**: NetworkXによるグラフ理論の実装
- 📊 **可視化**: Graphviz、Matplotlib、Streamlitによる美しい可視化
- 🤖 **AI支援**: Claude APIを使用した対話的なデータ分析
- 🧹 **データ前処理**: 欠損値処理、異常値検出などの自動化

## 🚀 クイックスタート

### 前提条件
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/) または [Cursor](https://cursor.sh/)
- VSCode拡張機能: Dev Containers

### セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-env.git
cd data-analysis-env
```

2. VSCode/Cursorで開く
```bash
code .  # または cursor .
```

3. 左下の緑色のボタンから「Reopen in Container」を選択

4. 環境構築完了後、アプリを起動
```bash
streamlit run network_demo.py
```

## 📱 アプリケーション

### 1. NetworkXデモ (`network_demo.py`)
- ランダムグラフ、スケールフリーネットワークなどの生成
- グラフの統計情報と可視化
- 中心性分析

### 2. Graphvizデモ (`graphviz_demo.py`)
- フローチャート作成
- 組織図の描画
- インタラクティブなグラフ構築

### 3. データ前処理 (`data_preprocessing.py`)
- データ診断レポート
- 欠損値の処理
- データ型変換
- 異常値検出と処理

### 4. Claude連携アプリ
- **ネットワーク分析** (`claude_network_app.py`)
- **データ分析アシスタント** (`claude_data_assistant.py`)

## 🔑 Claude AI連携

### APIキーの設定

1. [Anthropic Console](https://console.anthropic.com/)でAPIキーを取得

2. `.env`ファイルを作成
```bash
cp .env.example .env
```

3. `.env`ファイルにAPIキーを記入
```
ANTHROPIC_API_KEY=your-api-key-here
```

## 📁 プロジェクト構成

```
data-analysis-env/
├── .devcontainer/          # DevContainer設定
│   ├── devcontainer.json
│   └── Dockerfile
├── data/                   # データフォルダ（Gitで追跡されない）
│   ├── raw/               # 生データ
│   ├── processed/         # 処理済みデータ
│   └── temp/              # 一時ファイル
├── *.py                   # 各種アプリケーション
├── requirements.txt       # Pythonパッケージ
└── README.md             # このファイル
```

## 🛠️ 技術スタック

- **Python 3.11**
- **データ分析**: NumPy, Pandas, SciPy, scikit-learn
- **可視化**: Matplotlib, Seaborn, Plotly
- **ネットワーク分析**: NetworkX, Graphviz
- **Web UI**: Streamlit
- **AI**: Anthropic Claude API

## 📝 ライセンス

MIT License

## 🤝 貢献

プルリクエストを歓迎します！大きな変更の場合は、まずIssueを作成して変更内容を議論してください。

## 📧 連絡先

質問や提案がある場合は、Issueを作成してください。