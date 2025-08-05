"""
統合データ分析ワークフロー
データの取り込みから分析、可視化、レポート作成まで一貫して行えるシステム
"""

import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json

st.set_page_config(
    page_title="統合データ分析ワークフロー",
    page_icon="📊",
    layout="wide"
)

st.title("📊 統合データ分析ワークフロー")
st.markdown("""
このアプリケーションでは、データの取り込みから分析、可視化、レポート作成まで
一貫したワークフローで実行できます。
""")

# セッション状態の初期化
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# サイドバー：ワークフロー管理
st.sidebar.header("🔄 ワークフロー")

workflow_step = st.sidebar.radio(
    "ステップを選択",
    ["1. データ読み込み", "2. データ探索", "3. データ分析", "4. 可視化", "5. レポート作成"]
)

# ステップ1: データ読み込み
if workflow_step == "1. データ読み込み":
    st.header("📁 ステップ1: データ読み込み")
    
    # 既存ファイルから選択
    data_dir = Path("data/raw")
    files = list(data_dir.glob("*.csv")) + list(data_dir.glob("*.xlsx"))
    
    if files:
        selected_file = st.selectbox(
            "既存のファイルから選択",
            ["新規アップロード"] + [f.name for f in files]
        )
        
        if selected_file != "新規アップロード":
            file_path = data_dir / selected_file
            try:
                if selected_file.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                
                st.session_state.data = df
                st.success(f"✅ データを読み込みました: {selected_file}")
                st.dataframe(df.head())
                
                # 基本情報
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("行数", f"{len(df):,}")
                with col2:
                    st.metric("列数", f"{len(df.columns):,}")
                with col3:
                    st.metric("メモリ使用量", f"{df.memory_usage().sum() / 1024**2:.2f} MB")
                    
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {str(e)}")
    
    # 新規アップロード
    if selected_file == "新規アップロード" or not files:
        uploaded_file = st.file_uploader(
            "ファイルをアップロード",
            type=['csv', 'xlsx']
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.data = df
                st.success("✅ データを読み込みました")
                st.dataframe(df.head())
                
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {str(e)}")

# ステップ2: データ探索
elif workflow_step == "2. データ探索":
    st.header("🔍 ステップ2: データ探索")
    
    if st.session_state.data is None:
        st.warning("先にデータを読み込んでください")
    else:
        df = st.session_state.data
        
        # タブで整理
        tab1, tab2, tab3, tab4 = st.tabs(["基本統計", "データ型", "欠損値", "相関分析"])
        
        with tab1:
            st.subheader("基本統計量")
            st.dataframe(df.describe())
            
            # 数値列のヒストグラム
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.subheader("数値列の分布")
                col = st.selectbox("列を選択", numeric_cols)
                
                fig = px.histogram(df, x=col, nbins=30, title=f"{col}の分布")
                st.plotly_chart(fig)
        
        with tab2:
            st.subheader("データ型情報")
            dtype_df = pd.DataFrame({
                '列名': df.columns,
                'データ型': df.dtypes.astype(str),
                'ユニーク値数': [df[col].nunique() for col in df.columns],
                'null値数': df.isnull().sum().values,
                'null割合(%)': (df.isnull().sum() / len(df) * 100).round(2).values
            })
            st.dataframe(dtype_df)
        
        with tab3:
            st.subheader("欠損値の可視化")
            
            # 欠損値のヒートマップ
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
            plt.title("欠損値のパターン")
            st.pyplot(fig)
            
            # 欠損値の処理オプション
            st.subheader("欠損値の処理")
            col_with_null = df.columns[df.isnull().any()].tolist()
            
            if col_with_null:
                selected_col = st.selectbox("処理する列", col_with_null)
                method = st.selectbox(
                    "処理方法",
                    ["削除", "平均値で補完", "中央値で補完", "最頻値で補完", "前方補完", "後方補完"]
                )
                
                if st.button("欠損値を処理"):
                    if method == "削除":
                        df = df.dropna(subset=[selected_col])
                    elif method == "平均値で補完":
                        df[selected_col].fillna(df[selected_col].mean(), inplace=True)
                    elif method == "中央値で補完":
                        df[selected_col].fillna(df[selected_col].median(), inplace=True)
                    elif method == "最頻値で補完":
                        df[selected_col].fillna(df[selected_col].mode()[0], inplace=True)
                    elif method == "前方補完":
                        df[selected_col].fillna(method='ffill', inplace=True)
                    else:  # 後方補完
                        df[selected_col].fillna(method='bfill', inplace=True)
                    
                    st.session_state.data = df
                    st.success("✅ 欠損値を処理しました")
                    st.experimental_rerun()
        
        with tab4:
            st.subheader("相関分析")
            
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                # 相関行列のヒートマップ
                corr = numeric_df.corr()
                
                fig = px.imshow(
                    corr,
                    labels=dict(x="変数", y="変数", color="相関係数"),
                    x=corr.columns,
                    y=corr.columns,
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1
                )
                fig.update_layout(title="相関行列ヒートマップ")
                st.plotly_chart(fig)
                
                # 高相関ペアの抽出
                st.subheader("高相関ペア（|r| > 0.5）")
                high_corr = []
                for i in range(len(corr.columns)):
                    for j in range(i+1, len(corr.columns)):
                        if abs(corr.iloc[i, j]) > 0.5:
                            high_corr.append({
                                '変数1': corr.columns[i],
                                '変数2': corr.columns[j],
                                '相関係数': round(corr.iloc[i, j], 3)
                            })
                
                if high_corr:
                    st.dataframe(pd.DataFrame(high_corr))
                else:
                    st.info("高相関のペアは見つかりませんでした")

# ステップ3: データ分析
elif workflow_step == "3. データ分析":
    st.header("📈 ステップ3: データ分析")
    
    if st.session_state.data is None:
        st.warning("先にデータを読み込んでください")
    else:
        df = st.session_state.data
        
        analysis_type = st.selectbox(
            "分析タイプを選択",
            ["統計分析", "時系列分析", "グループ分析", "ネットワーク分析"]
        )
        
        if analysis_type == "統計分析":
            st.subheader("統計分析")
            
            # t検定、ANOVA、回帰分析など
            test_type = st.selectbox(
                "検定手法",
                ["記述統計", "t検定", "相関検定", "回帰分析"]
            )
            
            if test_type == "記述統計":
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                selected_col = st.selectbox("分析する列", numeric_cols)
                
                if selected_col:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("平均", f"{df[selected_col].mean():.2f}")
                    with col2:
                        st.metric("中央値", f"{df[selected_col].median():.2f}")
                    with col3:
                        st.metric("標準偏差", f"{df[selected_col].std():.2f}")
                    with col4:
                        st.metric("変動係数", f"{(df[selected_col].std() / df[selected_col].mean()):.2f}")
                    
                    # 正規性の検定
                    from scipy import stats
                    statistic, p_value = stats.shapiro(df[selected_col].dropna())
                    st.write(f"Shapiro-Wilk検定: 統計量={statistic:.4f}, p値={p_value:.4f}")
                    if p_value > 0.05:
                        st.success("正規分布に従う可能性があります（p > 0.05）")
                    else:
                        st.warning("正規分布に従わない可能性があります（p < 0.05）")
        
        elif analysis_type == "時系列分析":
            st.subheader("時系列分析")
            
            # 日付列の選択
            date_cols = df.select_dtypes(include=['datetime64', 'object']).columns
            if len(date_cols) > 0:
                date_col = st.selectbox("日付列", date_cols)
                
                # 日付型に変換を試みる
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    df = df.sort_values(date_col)
                    
                    # 分析対象の数値列
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    value_col = st.selectbox("値の列", numeric_cols)
                    
                    if value_col:
                        # 時系列プロット
                        fig = px.line(df, x=date_col, y=value_col, title=f"{value_col}の時系列推移")
                        st.plotly_chart(fig)
                        
                        # 移動平均
                        window = st.slider("移動平均の期間", 2, 30, 7)
                        df[f'MA_{window}'] = df[value_col].rolling(window=window).mean()
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=df[date_col], y=df[value_col], name="実測値"))
                        fig.add_trace(go.Scatter(x=df[date_col], y=df[f'MA_{window}'], name=f"{window}期間移動平均"))
                        fig.update_layout(title="移動平均との比較")
                        st.plotly_chart(fig)
                        
                except Exception as e:
                    st.error(f"日付変換エラー: {str(e)}")
            else:
                st.warning("日付列が見つかりません")
        
        elif analysis_type == "グループ分析":
            st.subheader("グループ分析")
            
            # カテゴリ列の選択
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(cat_cols) > 0:
                group_col = st.selectbox("グループ化する列", cat_cols)
                
                # 集計対象の数値列
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    agg_col = st.selectbox("集計する列", numeric_cols)
                    agg_func = st.selectbox("集計方法", ["mean", "sum", "count", "min", "max"])
                    
                    # グループ集計
                    grouped = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
                    grouped = grouped.sort_values(agg_col, ascending=False)
                    
                    # 結果表示
                    st.dataframe(grouped)
                    
                    # 可視化
                    fig = px.bar(grouped, x=group_col, y=agg_col, 
                                title=f"{group_col}別の{agg_col}（{agg_func}）")
                    st.plotly_chart(fig)
                    
                    # 結果を保存
                    st.session_state.analysis_results['group_analysis'] = grouped
        
        elif analysis_type == "ネットワーク分析":
            st.subheader("ネットワーク分析")
            
            st.info("エッジリスト形式のデータ（source, target, weight）が必要です")
            
            # 列の選択
            cols = df.columns.tolist()
            col1, col2, col3 = st.columns(3)
            with col1:
                source_col = st.selectbox("Source列", cols)
            with col2:
                target_col = st.selectbox("Target列", cols)
            with col3:
                weight_col = st.selectbox("Weight列（オプション）", ["なし"] + cols)
            
            if source_col and target_col and source_col != target_col:
                # NetworkXグラフの作成
                G = nx.Graph()
                
                for idx, row in df.iterrows():
                    if weight_col != "なし":
                        G.add_edge(row[source_col], row[target_col], weight=row[weight_col])
                    else:
                        G.add_edge(row[source_col], row[target_col])
                
                # 基本統計
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("ノード数", G.number_of_nodes())
                with col2:
                    st.metric("エッジ数", G.number_of_edges())
                with col3:
                    st.metric("密度", f"{nx.density(G):.3f}")
                with col4:
                    if nx.is_connected(G):
                        st.metric("平均パス長", f"{nx.average_shortest_path_length(G):.2f}")
                    else:
                        st.metric("連結成分数", nx.number_connected_components(G))
                
                # 中心性分析
                st.subheader("中心性分析")
                centrality_type = st.selectbox(
                    "中心性指標",
                    ["次数中心性", "媒介中心性", "近接中心性", "固有ベクトル中心性"]
                )
                
                if centrality_type == "次数中心性":
                    centrality = nx.degree_centrality(G)
                elif centrality_type == "媒介中心性":
                    centrality = nx.betweenness_centrality(G)
                elif centrality_type == "近接中心性":
                    centrality = nx.closeness_centrality(G)
                else:
                    centrality = nx.eigenvector_centrality(G, max_iter=1000)
                
                # 上位ノードの表示
                centrality_df = pd.DataFrame([
                    {"ノード": k, "中心性": v} 
                    for k, v in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
                ])
                st.dataframe(centrality_df)
                
                # ネットワーク可視化
                st.subheader("ネットワーク可視化")
                
                # レイアウトの選択
                layout_type = st.selectbox(
                    "レイアウト",
                    ["spring", "circular", "kamada_kawai", "shell"]
                )
                
                # 可視化
                plt.figure(figsize=(10, 8))
                
                if layout_type == "spring":
                    pos = nx.spring_layout(G)
                elif layout_type == "circular":
                    pos = nx.circular_layout(G)
                elif layout_type == "kamada_kawai":
                    pos = nx.kamada_kawai_layout(G)
                else:
                    pos = nx.shell_layout(G)
                
                # ノードサイズを中心性に基づいて設定
                node_sizes = [centrality.get(node, 0) * 3000 for node in G.nodes()]
                
                nx.draw(G, pos, node_size=node_sizes, with_labels=True,
                       node_color='lightblue', edge_color='gray', alpha=0.7)
                
                plt.title(f"ネットワーク図（{layout_type}レイアウト）")
                st.pyplot(plt)
                
                # 結果を保存
                st.session_state.analysis_results['network_analysis'] = {
                    'graph': G,
                    'centrality': centrality_df
                }

# ステップ4: 可視化
elif workflow_step == "4. 可視化":
    st.header("📊 ステップ4: 可視化")
    
    if st.session_state.data is None:
        st.warning("先にデータを読み込んでください")
    else:
        df = st.session_state.data
        
        viz_type = st.selectbox(
            "可視化タイプ",
            ["散布図", "折れ線グラフ", "棒グラフ", "ヒートマップ", "箱ひげ図", "3D散布図"]
        )
        
        if viz_type == "散布図":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X軸", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y軸", numeric_cols)
                
                # カラーオプション
                color_col = st.selectbox(
                    "色分け（オプション）",
                    ["なし"] + df.columns.tolist()
                )
                
                if color_col == "なし":
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                else:
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                   title=f"{x_col} vs {y_col} (色: {color_col})")
                
                st.plotly_chart(fig)
        
        elif viz_type == "折れ線グラフ":
            cols = df.columns.tolist()
            x_col = st.selectbox("X軸", cols)
            y_cols = st.multiselect("Y軸（複数選択可）", cols)
            
            if y_cols:
                fig = px.line(df, x=x_col, y=y_cols, title="折れ線グラフ")
                st.plotly_chart(fig)
        
        elif viz_type == "棒グラフ":
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(cat_cols) > 0 and len(numeric_cols) > 0:
                x_col = st.selectbox("カテゴリ", cat_cols)
                y_col = st.selectbox("値", numeric_cols)
                
                # 集計
                agg_df = df.groupby(x_col)[y_col].mean().reset_index()
                agg_df = agg_df.sort_values(y_col, ascending=False)
                
                fig = px.bar(agg_df, x=x_col, y=y_col, title=f"{x_col}別の{y_col}平均")
                st.plotly_chart(fig)
        
        elif viz_type == "ヒートマップ":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr = numeric_df.corr()
                
                fig = px.imshow(corr, 
                              labels=dict(x="変数", y="変数", color="相関係数"),
                              x=corr.columns,
                              y=corr.columns,
                              color_continuous_scale='RdBu_r',
                              zmin=-1, zmax=1)
                fig.update_layout(title="相関ヒートマップ")
                st.plotly_chart(fig)
        
        elif viz_type == "箱ひげ図":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            
            if len(numeric_cols) > 0:
                y_col = st.selectbox("値", numeric_cols)
                
                if len(cat_cols) > 0:
                    x_col = st.selectbox("グループ（オプション）", ["なし"] + cat_cols.tolist())
                    
                    if x_col == "なし":
                        fig = px.box(df, y=y_col, title=f"{y_col}の分布")
                    else:
                        fig = px.box(df, x=x_col, y=y_col, title=f"{x_col}別の{y_col}分布")
                else:
                    fig = px.box(df, y=y_col, title=f"{y_col}の分布")
                
                st.plotly_chart(fig)
        
        elif viz_type == "3D散布図":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 3:
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X軸", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y軸", numeric_cols)
                with col3:
                    z_col = st.selectbox("Z軸", numeric_cols)
                
                fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col,
                                  title=f"3D散布図: {x_col} x {y_col} x {z_col}")
                st.plotly_chart(fig)

# ステップ5: レポート作成
elif workflow_step == "5. レポート作成":
    st.header("📄 ステップ5: レポート作成")
    
    st.markdown("""
    これまでの分析結果をレポートとしてまとめます。
    """)
    
    # レポートタイトル
    report_title = st.text_input("レポートタイトル", value="データ分析レポート")
    
    # レポート内容の選択
    st.subheader("レポートに含める内容")
    
    include_data_info = st.checkbox("データ基本情報", value=True)
    include_stats = st.checkbox("基本統計量", value=True)
    include_analysis = st.checkbox("分析結果", value=True)
    include_viz = st.checkbox("可視化", value=True)
    
    # レポート生成
    if st.button("レポート生成", type="primary"):
        report = f"# {report_title}\n\n"
        report += f"作成日: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n\n"
        
        if st.session_state.data is not None:
            df = st.session_state.data
            
            if include_data_info:
                report += "## データ基本情報\n\n"
                report += f"- データサイズ: {len(df):,}行 × {len(df.columns)}列\n"
                report += f"- メモリ使用量: {df.memory_usage().sum() / 1024**2:.2f} MB\n\n"
                report += "### 列情報\n\n"
                report += "| 列名 | データ型 | 非null数 | ユニーク値数 |\n"
                report += "|------|----------|----------|------------|\n"
                for col in df.columns:
                    report += f"| {col} | {df[col].dtype} | {df[col].notna().sum()} | {df[col].nunique()} |\n"
                report += "\n"
            
            if include_stats:
                report += "## 基本統計量\n\n"
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 0:
                    stats = numeric_df.describe()
                    report += stats.to_markdown() + "\n\n"
            
            if include_analysis and st.session_state.analysis_results:
                report += "## 分析結果\n\n"
                for key, value in st.session_state.analysis_results.items():
                    report += f"### {key}\n\n"
                    if isinstance(value, pd.DataFrame):
                        report += value.to_markdown() + "\n\n"
                    elif isinstance(value, dict):
                        report += f"{json.dumps(value, indent=2, ensure_ascii=False)}\n\n"
            
            # レポート表示
            st.markdown("### レポートプレビュー")
            st.markdown(report)
            
            # ダウンロード
            st.download_button(
                label="レポートをダウンロード（Markdown）",
                data=report,
                file_name=f"{report_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            
            # 処理済みデータの保存オプション
            if st.checkbox("処理済みデータも保存"):
                col1, col2 = st.columns(2)
                with col1:
                    save_name = st.text_input(
                        "ファイル名",
                        value=f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                with col2:
                    save_format = st.selectbox("保存形式", ["csv", "xlsx", "parquet"])
                
                if st.button("データ保存"):
                    save_path = Path("data/processed") / f"{save_name}.{save_format}"
                    
                    if save_format == "csv":
                        df.to_csv(save_path, index=False)
                    elif save_format == "xlsx":
                        df.to_excel(save_path, index=False)
                    else:
                        df.to_parquet(save_path, index=False)
                    
                    st.success(f"✅ データを保存しました: {save_path}")
        else:
            st.warning("分析するデータがありません")

# フッター
st.markdown("---")
st.caption("統合データ分析ワークフロー v1.0")
