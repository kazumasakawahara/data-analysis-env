# データフォルダ

このフォルダには分析対象のデータを保存してください。

## 📁 推奨するファイル形式
- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)
- テキスト (.txt)

## 📝 データの配置例
```
data/
├── raw/          # 元データ（変更しない）
│   ├── sales_2024.csv
│   └── customer_data.xlsx
├── processed/    # 前処理済みデータ
│   ├── sales_2024_cleaned.csv
│   └── customer_data_processed.csv
└── temp/         # 一時ファイル
```

## 🔧 前処理のサポート
Claudeに以下のような依頼ができます：
- 欠損値の確認と補完
- データ型の変換
- 異常値の検出と処理
- データの結合や変換
- 統計的な要約の作成