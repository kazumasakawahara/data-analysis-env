import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pylab import rcParams

# ページの設定
st.set_page_config(page_title="ネットワーク分析デモ", page_icon="🕸️", layout="wide")

st.title("🕸️ NetworkXを使ったグラフ分析デモ")
st.markdown("このアプリケーションは、NetworkXとStreamlitを使ったネットワーク分析のデモです。")

# サイドバーで設定
st.sidebar.header("グラフの設定")
graph_type = st.sidebar.selectbox(
    "グラフの種類を選択",
    ["ランダムグラフ", "スケールフリーネットワーク", "スモールワールド", "完全グラフ"]
)

num_nodes = st.sidebar.slider("ノード数", 5, 30, 10)

# グラフの生成
if graph_type == "ランダムグラフ":
    G = nx.erdos_renyi_graph(num_nodes, 0.3)
elif graph_type == "スケールフリーネットワーク":
    G = nx.barabasi_albert_graph(num_nodes, 2)
elif graph_type == "スモールワールド":
    G = nx.watts_strogatz_graph(num_nodes, 4, 0.3)
else:  # 完全グラフ
    G = nx.complete_graph(num_nodes)

# メインコンテンツ
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("ネットワークの可視化")
    
    # グラフの描画
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # ノードの次数を計算
    degrees = dict(G.degree())
    node_sizes = [v * 100 + 100 for v in degrees.values()]
    
    # グラフを描画
    nx.draw(G, pos, 
            node_color='lightblue',
            node_size=node_sizes,
            with_labels=True,
            font_size=10,
            font_weight='bold',
            edge_color='gray',
            alpha=0.7,
            ax=ax)
    
    plt.title(f"{graph_type} (ノード数: {num_nodes})")
    st.pyplot(fig)

with col2:
    st.subheader("グラフの統計情報")
    
    # 基本統計
    stats = {
        "ノード数": G.number_of_nodes(),
        "エッジ数": G.number_of_edges(),
        "平均次数": f"{2 * G.number_of_edges() / G.number_of_nodes():.2f}",
        "密度": f"{nx.density(G):.3f}",
    }
    
    # 連結性
    if nx.is_connected(G):
        stats["平均経路長"] = f"{nx.average_shortest_path_length(G):.2f}"
        stats["直径"] = nx.diameter(G)
    
    stats["クラスタリング係数"] = f"{nx.average_clustering(G):.3f}"
    
    # データフレームとして表示
    stats_df = pd.DataFrame.from_dict(stats, orient='index', columns=['値'])
    st.dataframe(stats_df)

# 次数分布
st.subheader("次数分布")
col3, col4 = st.columns(2)

with col3:
    # 次数のヒストグラム
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    ax2.bar(range(len(degree_sequence)), degree_sequence)
    ax2.set_xlabel("ノード")
    ax2.set_ylabel("次数")
    ax2.set_title("ノードごとの次数")
    st.pyplot(fig2)

with col4:
    # 次数分布の表
    degree_counts = {}
    for node, degree in G.degree():
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1
    
    degree_df = pd.DataFrame.from_dict(
        degree_counts, 
        orient='index', 
        columns=['ノード数']
    ).sort_index()
    degree_df.index.name = '次数'
    st.dataframe(degree_df)

# 中心性の計算
st.subheader("ノードの中心性")
centrality_type = st.selectbox(
    "中心性の種類",
    ["次数中心性", "媒介中心性", "近接中心性", "固有ベクトル中心性"]
)

if centrality_type == "次数中心性":
    centrality = nx.degree_centrality(G)
elif centrality_type == "媒介中心性":
    centrality = nx.betweenness_centrality(G)
elif centrality_type == "近接中心性":
    if nx.is_connected(G):
        centrality = nx.closeness_centrality(G)
    else:
        st.warning("グラフが連結でないため、近接中心性を計算できません。")
        centrality = {node: 0 for node in G.nodes()}
else:  # 固有ベクトル中心性
    try:
        centrality = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        st.warning("固有ベクトル中心性の計算に失敗しました。")
        centrality = {node: 0 for node in G.nodes()}

# 中心性でソートして上位を表示
sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
top_nodes = pd.DataFrame(sorted_centrality[:10], columns=['ノード', '中心性スコア'])
st.dataframe(top_nodes)

# フッター
st.markdown("---")
st.markdown("このデモは、NetworkX、Matplotlib、Streamlitを使用して作成されています。")