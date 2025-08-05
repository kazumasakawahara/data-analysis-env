import streamlit as st
import graphviz
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Graphviz可視化デモ", page_icon="🎯", layout="wide")

st.title("🎯 Graphvizを使った図表作成デモ")
st.markdown("Graphvizを使って、フローチャートや組織図などを作成できます。")

# タブの作成
tab1, tab2, tab3 = st.tabs(["フローチャート", "組織図", "ネットワーク図"])

with tab1:
    st.header("フローチャートの例")
    
    # Graphvizのコード
    dot = graphviz.Digraph(comment='フローチャート')
    dot.attr(rankdir='TB')
    
    # ノードのスタイル設定
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    
    # フローチャートの作成
    dot.node('start', '開始', shape='ellipse', fillcolor='lightgreen')
    dot.node('input', 'データ入力')
    dot.node('process', 'データ処理')
    dot.node('decision', '条件判定', shape='diamond', fillcolor='lightyellow')
    dot.node('output1', '結果出力A')
    dot.node('output2', '結果出力B')
    dot.node('end', '終了', shape='ellipse', fillcolor='lightcoral')
    
    # エッジ（矢印）の追加
    dot.edge('start', 'input')
    dot.edge('input', 'process')
    dot.edge('process', 'decision')
    dot.edge('decision', 'output1', label='Yes')
    dot.edge('decision', 'output2', label='No')
    dot.edge('output1', 'end')
    dot.edge('output2', 'end')
    
    # 表示
    st.graphviz_chart(dot.source)
    
    # コードの表示
    with st.expander("Graphvizコードを見る"):
        st.code(dot.source, language='dot')

with tab2:
    st.header("組織図の例")
    
    # 組織図の作成
    org = graphviz.Digraph(comment='組織図')
    org.attr(rankdir='TB')
    org.attr('node', shape='box', style='filled', fillcolor='lightgray')
    
    # CEOレベル
    org.node('ceo', '代表取締役\n山田太郎', fillcolor='gold')
    
    # 部門長レベル
    org.node('cto', 'CTO\n技術部長', fillcolor='lightblue')
    org.node('cfo', 'CFO\n財務部長', fillcolor='lightgreen')
    org.node('cmo', 'CMO\nマーケティング部長', fillcolor='lightcoral')
    
    # チームレベル
    org.node('dev1', '開発チーム1')
    org.node('dev2', '開発チーム2')
    org.node('finance', '経理チーム')
    org.node('accounting', '会計チーム')
    org.node('marketing', 'マーケティングチーム')
    org.node('sales', '営業チーム')
    
    # 関係性の定義
    org.edge('ceo', 'cto')
    org.edge('ceo', 'cfo')
    org.edge('ceo', 'cmo')
    org.edge('cto', 'dev1')
    org.edge('cto', 'dev2')
    org.edge('cfo', 'finance')
    org.edge('cfo', 'accounting')
    org.edge('cmo', 'marketing')
    org.edge('cmo', 'sales')
    
    st.graphviz_chart(org.source)

with tab3:
    st.header("インタラクティブなネットワーク図")
    
    # ユーザー入力
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ノードの追加")
        node_name = st.text_input("ノード名")
        node_color = st.color_picker("ノードの色", "#00f900")
        if st.button("ノードを追加"):
            if 'nodes' not in st.session_state:
                st.session_state.nodes = []
            st.session_state.nodes.append({
                'name': node_name,
                'color': node_color
            })
    
    with col2:
        st.subheader("エッジの追加")
        if 'nodes' in st.session_state and len(st.session_state.nodes) > 1:
            node_names = [n['name'] for n in st.session_state.nodes]
            from_node = st.selectbox("開始ノード", node_names)
            to_node = st.selectbox("終了ノード", node_names)
            edge_label = st.text_input("エッジのラベル（オプション）")
            
            if st.button("エッジを追加"):
                if 'edges' not in st.session_state:
                    st.session_state.edges = []
                st.session_state.edges.append({
                    'from': from_node,
                    'to': to_node,
                    'label': edge_label
                })
        else:
            st.info("エッジを追加するには、まず2つ以上のノードを作成してください。")
    
    # グラフの描画
    if 'nodes' in st.session_state and st.session_state.nodes:
        graph = graphviz.Digraph(comment='カスタムグラフ')
        graph.attr('node', shape='circle', style='filled')
        
        # ノードの追加
        for node in st.session_state.nodes:
            graph.node(node['name'], node['name'], fillcolor=node['color'])
        
        # エッジの追加
        if 'edges' in st.session_state:
            for edge in st.session_state.edges:
                if edge['label']:
                    graph.edge(edge['from'], edge['to'], label=edge['label'])
                else:
                    graph.edge(edge['from'], edge['to'])
        
        st.graphviz_chart(graph.source)
        
        # リセットボタン
        if st.button("グラフをリセット"):
            del st.session_state.nodes
            if 'edges' in st.session_state:
                del st.session_state.edges
            st.rerun()
    else:
        st.info("ノードを追加してグラフの作成を開始してください。")

# サイドバーに説明を追加
st.sidebar.header("Graphvizについて")
st.sidebar.markdown("""
Graphvizは、グラフ構造を記述するための言語（DOT言語）を使って、
様々な図表を自動的に美しくレイアウトしてくれるツールです。

### 主な用途
- フローチャート
- 組織図
- ネットワーク図
- 状態遷移図
- データ構造の可視化

### 特徴
- テキストベースで図を定義
- 自動レイアウト
- 多様な出力形式（PNG、SVG、PDFなど）
""")