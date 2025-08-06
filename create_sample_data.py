"""
サンプルデータ生成スクリプト
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# data/rawディレクトリを作成
os.makedirs("data/raw", exist_ok=True)

# 1. 売上データのサンプル
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
sales_data = pd.DataFrame({
    '日付': dates,
    '売上': np.random.normal(100000, 20000, len(dates)) + np.sin(np.arange(len(dates)) * 0.1) * 10000,
    '顧客数': np.random.poisson(50, len(dates)),
    '平均単価': np.random.normal(2000, 300, len(dates)),
    'カテゴリ': np.random.choice(['商品A', '商品B', '商品C'], len(dates))
})
sales_data.to_csv('data/raw/sales_data_2024.csv', index=False, encoding='utf-8')
print("✅ sales_data_2024.csv を作成しました")

# 2. ネットワークデータのサンプル
nodes = []
for i in range(20):
    nodes.append({
        'node_id': f'Node_{i}',
        'label': f'ノード{i}',
        'group': np.random.choice(['A', 'B', 'C']),
        'value': np.random.uniform(10, 100)
    })
nodes_df = pd.DataFrame(nodes)
nodes_df.to_csv('data/raw/network_nodes_sample.csv', index=False, encoding='utf-8')

edges = []
for i in range(30):
    source = np.random.randint(0, 20)
    target = np.random.randint(0, 20)
    if source != target:
        edges.append({
            'source': f'Node_{source}',
            'target': f'Node_{target}',
            'weight': np.random.uniform(0.1, 1.0)
        })
edges_df = pd.DataFrame(edges)
edges_df.to_csv('data/raw/network_edges_sample.csv', index=False, encoding='utf-8')
print("✅ network_nodes_sample.csv, network_edges_sample.csv を作成しました")

# 3. 顧客データのサンプル
customers = []
for i in range(1000):
    customers.append({
        '顧客ID': f'C{i:04d}',
        '年齢': np.random.randint(20, 70),
        '性別': np.random.choice(['男性', '女性']),
        '地域': np.random.choice(['東京', '大阪', '名古屋', '福岡', '札幌']),
        '購入回数': np.random.poisson(5),
        '総購入額': np.random.exponential(50000)
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv('data/raw/customer_data.csv', index=False, encoding='utf-8')
print("✅ customer_data.csv を作成しました")

print("\n📁 data/raw/ フォルダに以下のファイルを作成しました：")
print("  - sales_data_2024.csv（売上データ）")
print("  - network_nodes_sample.csv（ネットワークノード）")
print("  - network_edges_sample.csv（ネットワークエッジ）")
print("  - customer_data.csv（顧客データ）")
