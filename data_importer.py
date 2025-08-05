"""
データインポート統合ツール
様々なソースからデータを取り込んで分析可能な形式に変換
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime
import os
from pathlib import Path

st.set_page_config(
    page_title="データインポートツール",
    page_icon="📊",
    layout="wide"
)

st.title("📊 データインポート統合ツール")
st.markdown("様々なソースからデータを取り込んで、分析可能な形式に変換します。")

# データソースの選択
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "ファイルアップロード", 
    "データベース接続", 
    "Web API", 
    "Webスクレイピング",
    "サンプルデータ生成"
])

with tab1:
    st.header("📁 ファイルからのインポート")
    
    uploaded_file = st.file_uploader(
        "ファイルを選択",
        type=['csv', 'xlsx', 'json', 'txt'],
        help="CSV、Excel、JSON、テキストファイルに対応"
    )
    
    if uploaded_file is not None:
        # ファイル形式の判定と読み込み
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                # CSVの詳細設定
                col1, col2, col3 = st.columns(3)
                with col1:
                    encoding = st.selectbox(
                        "エンコーディング",
                        ['utf-8', 'shift-jis', 'cp932', 'euc-jp'],
                        help="日本語ファイルの場合はshift-jisやcp932を選択"
                    )
                with col2:
                    separator = st.selectbox(
                        "区切り文字",
                        [',', '\t', ';', '|'],
                        format_func=lambda x: {',' : 'カンマ', '\t': 'タブ', ';': 'セミコロン', '|': 'パイプ'}[x]
                    )
                with col3:
                    header_row = st.number_input(
                        "ヘッダー行",
                        min_value=0,
                        value=0,
                        help="0は1行目がヘッダー"
                    )
                
                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    sep=separator,
                    header=header_row
                )
                
            elif file_extension in ['xlsx', 'xls']:
                # Excelの詳細設定
                sheet_name = st.text_input(
                    "シート名",
                    value="Sheet1",
                    help="読み込むシート名を指定"
                )
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                
            elif file_extension == 'json':
                # JSONの読み込み
                data = json.load(uploaded_file)
                df = pd.json_normalize(data)
                
            else:
                st.error(f"未対応のファイル形式: {file_extension}")
                df = None
            
            if df is not None:
                st.success(f"✅ ファイルを読み込みました: {uploaded_file.name}")
                
                # データプレビュー
                st.subheader("データプレビュー")
                st.dataframe(df.head(10))
                
                # データ情報
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("行数", f"{len(df):,}")
                with col2:
                    st.metric("列数", f"{len(df.columns):,}")
                with col3:
                    st.metric("メモリ使用量", f"{df.memory_usage().sum() / 1024**2:.2f} MB")
                
                # データ型の確認と変換
                st.subheader("データ型の確認と変換")
                dtype_df = pd.DataFrame({
                    '列名': df.columns,
                    '現在の型': df.dtypes.astype(str),
                    '欠損値数': df.isnull().sum().values,
                    'ユニーク値数': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(dtype_df)
                
                # 保存オプション
                st.subheader("データの保存")
                col1, col2 = st.columns(2)
                with col1:
                    save_name = st.text_input(
                        "保存ファイル名",
                        value=f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                with col2:
                    save_format = st.selectbox(
                        "保存形式",
                        ['csv', 'xlsx', 'json', 'parquet']
                    )
                
                if st.button("データを保存", type="primary"):
                    save_path = Path("data/raw") / f"{save_name}.{save_format}"
                    
                    if save_format == 'csv':
                        df.to_csv(save_path, index=False, encoding='utf-8')
                    elif save_format == 'xlsx':
                        df.to_excel(save_path, index=False)
                    elif save_format == 'json':
                        df.to_json(save_path, orient='records', force_ascii=False)
                    elif save_format == 'parquet':
                        df.to_parquet(save_path, index=False)
                    
                    st.success(f"✅ データを保存しました: {save_path}")
                    
        except Exception as e:
            st.error(f"ファイルの読み込みエラー: {str(e)}")

with tab2:
    st.header("🗄️ データベース接続")
    
    db_type = st.selectbox(
        "データベースタイプ",
        ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB']
    )
    
    if db_type in ['PostgreSQL', 'MySQL']:
        col1, col2 = st.columns(2)
        with col1:
            host = st.text_input("ホスト", value="localhost")
            port = st.number_input(
                "ポート",
                value=5432 if db_type == 'PostgreSQL' else 3306
            )
            database = st.text_input("データベース名")
        with col2:
            username = st.text_input("ユーザー名")
            password = st.text_input("パスワード", type="password")
        
        query = st.text_area(
            "SQLクエリ",
            value="SELECT * FROM table_name LIMIT 100",
            height=100
        )
        
        if st.button("接続してデータ取得"):
            st.info("データベース接続機能は環境に応じて実装してください")
            # ここに実際のDB接続コードを追加
            
    elif db_type == 'SQLite':
        sqlite_file = st.file_uploader("SQLiteファイル", type=['db', 'sqlite'])
        if sqlite_file:
            st.info("SQLite接続機能は環境に応じて実装してください")
            
    else:  # MongoDB
        connection_string = st.text_input(
            "接続文字列",
            value="mongodb://localhost:27017/"
        )
        st.info("MongoDB接続機能は環境に応じて実装してください")

with tab3:
    st.header("🌐 Web API連携")
    
    api_type = st.selectbox(
        "APIタイプ",
        ['カスタムAPI', 'OpenData', 'Social Media', '金融データ']
    )
    
    if api_type == 'カスタムAPI':
        endpoint = st.text_input("APIエンドポイント")
        method = st.selectbox("HTTPメソッド", ['GET', 'POST'])
        
        # ヘッダー設定
        st.subheader("ヘッダー設定")
        headers = {}
        header_count = st.number_input("ヘッダー数", min_value=0, max_value=10, value=1)
        for i in range(header_count):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(f"キー{i+1}", key=f"header_key_{i}")
            with col2:
                value = st.text_input(f"値{i+1}", key=f"header_value_{i}")
            if key:
                headers[key] = value
        
        # パラメータ設定
        if method == 'GET':
            st.subheader("クエリパラメータ")
            params = st.text_area(
                "パラメータ（JSON形式）",
                value='{\n  "param1": "value1"\n}'
            )
        else:
            st.subheader("リクエストボディ")
            body = st.text_area(
                "ボディ（JSON形式）",
                value='{\n  "key": "value"\n}'
            )
        
        if st.button("APIリクエスト実行"):
            try:
                if method == 'GET':
                    response = requests.get(
                        endpoint,
                        headers=headers,
                        params=json.loads(params) if params else None
                    )
                else:
                    response = requests.post(
                        endpoint,
                        headers=headers,
                        json=json.loads(body) if body else None
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ データ取得成功")
                    st.json(data)
                    
                    # DataFrameに変換を試みる
                    try:
                        df = pd.json_normalize(data)
                        st.dataframe(df)
                    except:
                        st.info("データをDataFrameに変換できませんでした")
                else:
                    st.error(f"エラー: {response.status_code}")
                    
            except Exception as e:
                st.error(f"リクエストエラー: {str(e)}")
    
    else:
        st.info(f"{api_type}の連携機能は今後実装予定です")

with tab4:
    st.header("🕷️ Webスクレイピング")
    
    url = st.text_input("対象URL")
    
    st.warning("""
    ⚠️ 注意事項:
    - robots.txtを確認し、スクレイピングが許可されているか確認してください
    - サーバーに負荷をかけないよう、適切な間隔を空けてアクセスしてください
    - 利用規約を確認してください
    """)
    
    if url and st.button("スクレイピング実行"):
        st.info("スクレイピング機能は環境に応じて実装してください")
        # BeautifulSoupやSeleniumを使用したスクレイピングコードをここに追加

with tab5:
    st.header("🎲 サンプルデータ生成")
    
    st.markdown("テスト用のサンプルデータを生成します。")
    
    data_type = st.selectbox(
        "データタイプ",
        ['時系列データ', 'ネットワークデータ', '顧客データ', '売上データ']
    )
    
    if data_type == '時系列データ':
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("開始日")
        with col2:
            end_date = st.date_input("終了日")
        with col3:
            freq = st.selectbox("頻度", ['D', 'H', 'M', 'W'])
        
        columns = st.multiselect(
            "生成する列",
            ['売上', '在庫', '顧客数', '気温', 'トレンド'],
            default=['売上', '在庫']
        )
        
        if st.button("時系列データ生成"):
            dates = pd.date_range(start=start_date, end=end_date, freq=freq)
            data = {'date': dates}
            
            for col in columns:
                if col == '売上':
                    data[col] = np.random.normal(10000, 2000, len(dates)) + \
                               np.sin(np.arange(len(dates)) * 0.1) * 1000
                elif col == '在庫':
                    data[col] = np.random.normal(500, 100, len(dates))
                elif col == '顧客数':
                    data[col] = np.random.poisson(50, len(dates))
                elif col == '気温':
                    data[col] = np.random.normal(20, 5, len(dates)) + \
                               np.sin(np.arange(len(dates)) * 0.02) * 10
                else:  # トレンド
                    data[col] = np.arange(len(dates)) * 10 + \
                               np.random.normal(0, 5, len(dates))
            
            df = pd.DataFrame(data)
            st.dataframe(df.head(10))
            
            # グラフ表示
            st.line_chart(df.set_index('date')[columns])
            
            # 保存
            if st.button("このデータを保存"):
                save_path = Path("data/raw") / f"timeseries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(save_path, index=False)
                st.success(f"✅ 保存しました: {save_path}")
    
    elif data_type == 'ネットワークデータ':
        col1, col2 = st.columns(2)
        with col1:
            num_nodes = st.slider("ノード数", 5, 100, 20)
        with col2:
            edge_prob = st.slider("エッジ生成確率", 0.0, 1.0, 0.1)
        
        if st.button("ネットワークデータ生成"):
            import networkx as nx
            
            # ランダムグラフ生成
            G = nx.erdos_renyi_graph(num_nodes, edge_prob)
            
            # エッジリストをDataFrameに変換
            edges = []
            for u, v in G.edges():
                weight = np.random.uniform(0.1, 1.0)
                edges.append({
                    'source': f'Node_{u}',
                    'target': f'Node_{v}',
                    'weight': weight
                })
            
            edges_df = pd.DataFrame(edges)
            
            # ノード属性
            nodes = []
            for i in range(num_nodes):
                nodes.append({
                    'node_id': f'Node_{i}',
                    'degree': G.degree(i),
                    'category': np.random.choice(['A', 'B', 'C']),
                    'value': np.random.uniform(0, 100)
                })
            
            nodes_df = pd.DataFrame(nodes)
            
            st.subheader("エッジデータ")
            st.dataframe(edges_df.head(10))
            
            st.subheader("ノードデータ")
            st.dataframe(nodes_df.head(10))
            
            # 保存
            col1, col2 = st.columns(2)
            with col1:
                if st.button("エッジデータを保存"):
                    save_path = Path("data/raw") / f"edges_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    edges_df.to_csv(save_path, index=False)
                    st.success(f"✅ 保存: {save_path}")
            
            with col2:
                if st.button("ノードデータを保存"):
                    save_path = Path("data/raw") / f"nodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    nodes_df.to_csv(save_path, index=False)
                    st.success(f"✅ 保存: {save_path}")
    
    else:
        st.info(f"{data_type}の生成機能は今後実装予定です")

# サイドバー：データ管理
st.sidebar.header("📂 データ管理")

# 保存済みデータの一覧
data_dir = Path("data/raw")
if data_dir.exists():
    files = list(data_dir.glob("*"))
    if files:
        st.sidebar.subheader("保存済みデータ")
        for file in sorted(files, reverse=True)[:10]:
            file_size = file.stat().st_size / 1024  # KB
            st.sidebar.text(f"📄 {file.name} ({file_size:.1f} KB)")
    else:
        st.sidebar.info("保存済みデータはありません")
else:
    data_dir.mkdir(parents=True, exist_ok=True)
    st.sidebar.info("dataフォルダを作成しました")

# メモリ使用状況
import psutil
memory = psutil.virtual_memory()
st.sidebar.metric(
    "メモリ使用率",
    f"{memory.percent}%",
    f"{memory.used / 1024**3:.1f} / {memory.total / 1024**3:.1f} GB"
)
