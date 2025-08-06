# Claude Code 引き継ぎ書

## プロジェクト概要

このプロジェクトは、NetworkXとStreamlitを使用したデータ分析統合環境です。現在、基本的なデータ分析ワークフローは完成していますが、実務で使用するためにはさらなる機能拡張が必要です。

## 現在の構成

### メインアプリケーション
- `integrated_analysis_workflow.py` - 統合分析ワークフロー（メイン）
- `data_importer.py` - データインポートツール
- `data_preprocessing.py` - データ前処理ツール

### サポートモジュール
- `japanese_font_setup.py` - 日本語フォント設定
- `custom_colors.py` - カスタムカラーパレット

### ディレクトリ構造
```
data-analysis-env/
├── data/
│   ├── raw/        # 生データ
│   ├── processed/  # 処理済みデータ
│   └── temp/       # 一時ファイル
├── output/         # 分析結果
├── demo_archive/   # アーカイブしたデモファイル
└── venv/          # Python仮想環境
```

## 技術スタック
- Python 3.12
- Streamlit 1.31.0
- Pandas 2.2.0
- NetworkX 3.2.1
- Plotly 5.18.0
- Matplotlib 3.10.5
- Seaborn 0.13.2

## 実行環境
- Windows 11 + WSL (Ubuntu)
- 仮想環境: venv

## 実行方法
```bash
cd /mnt/c/Users/kazum/data-analysis-env
source venv/bin/activate
streamlit run integrated_analysis_workflow.py
```

## 現在の機能
1. データ読み込み（CSV、Excel）
2. データ探索（基本統計、欠損値、相関）
3. データ分析（統計、時系列、グループ、ネットワーク）
4. 可視化（各種グラフ）
5. レポート生成（Markdown形式）

## 既知の問題
- 大規模データ（100MB以上）の処理が遅い
- エラーハンドリングが不十分な箇所がある
- メモリ使用量の最適化が必要

## 改善要望
Task.mdファイルに詳細を記載しています。
