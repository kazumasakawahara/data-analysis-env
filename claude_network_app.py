import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
import networkx as nx
import matplotlib.pyplot as plt
import json

# 環境変数の読み込み
load_dotenv()

st.set_page_config(page_title="Claude連携ネットワーク分析", page_icon="🤖", layout="wide")

st.title("🤖 Claude連携ネットワーク分析アプリ")
st.markdown("Claudeと対話しながらネットワーク分析を行うアプリです。")

# APIキーの設定
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv('ANTHROPIC_API_KEY', '')

with st.sidebar:
    st.header("設定")
    api_key = st.text_input(
        "Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        help="https://console.anthropic.com/ から取得できます"
    )
    if api_key:
        st.session_state.api_key = api_key

# メインコンテンツ
if not st.session_state.api_key:
    st.warning("⚠️ APIキーを設定してください。")
    st.info("""
    ### APIキーの取得方法：
    1. [Anthropic Console](https://console.anthropic.com/) にアクセス
    2. アカウントを作成またはログイン
    3. API Keysセクションで新しいキーを生成
    4. 左のサイドバーにキーを貼り付け
    """)
else:
    # Claudeクライアントの初期化
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    
    # チャット履歴の初期化
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.graph_data = None
    
    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("graph_data"):
                # グラフの再描画
                G = nx.node_link_graph(message["graph_data"])
                fig, ax = plt.subplots(figsize=(8, 6))
                pos = nx.spring_layout(G)
                nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                       node_size=1000, font_size=10, ax=ax)
                st.pyplot(fig)
    
    # ユーザー入力
    if prompt := st.chat_input("ネットワーク分析について質問してください（例：「5つのノードを持つランダムグラフを作成して」）"):
        # ユーザーメッセージの追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Claudeへのリクエスト
        with st.chat_message("assistant"):
            with st.spinner("考えています..."):
                try:
                    # システムプロンプト
                    system_prompt = """
あなたはネットワーク分析の専門家です。ユーザーの質問に対して、NetworkXを使ったPythonコードを生成し、実行可能な形で提供します。

回答する際は以下の形式に従ってください：

1. まず質問への説明を日本語で行う
2. 必要に応じて、以下の形式でNetworkXコードを生成する：

```python
# グラフの作成コード
import networkx as nx
G = nx.Graph()  # または他のグラフタイプ
# ... グラフ構築のコード ...

# グラフのJSONデータを生成（これは必須）
graph_json = nx.node_link_data(G)
```

3. コードブロックには必ず `graph_json = nx.node_link_data(G)` を含める

重要：生成するコードは実際に実行可能で、エラーが出ないようにしてください。
"""
                    
                    # Claudeに質問
                    response = client.messages.create(
                        model="claude-3-sonnet-20241022",
                        max_tokens=2000,
                        system=system_prompt,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # レスポンスの取得
                    claude_response = response.content[0].text
                    st.markdown(claude_response)
                    
                    # コードブロックの抽出と実行
                    if "```python" in claude_response:
                        # コードの抽出
                        code_start = claude_response.find("```python") + 9
                        code_end = claude_response.find("```", code_start)
                        code = claude_response[code_start:code_end].strip()
                        
                        try:
                            # コードの実行
                            exec_globals = {}
                            exec(code, exec_globals)
                            
                            # グラフデータの取得
                            if 'graph_json' in exec_globals:
                                graph_data = exec_globals['graph_json']
                                
                                # グラフの可視化
                                G = nx.node_link_graph(graph_data)
                                fig, ax = plt.subplots(figsize=(8, 6))
                                pos = nx.spring_layout(G)
                                nx.draw(G, pos, with_labels=True, 
                                       node_color='lightblue', node_size=1000, 
                                       font_size=10, ax=ax)
                                st.pyplot(fig)
                                
                                # グラフの統計情報
                                with st.expander("グラフの詳細情報"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.metric("ノード数", G.number_of_nodes())
                                        st.metric("エッジ数", G.number_of_edges())
                                    with col2:
                                        st.metric("密度", f"{nx.density(G):.3f}")
                                        if G.number_of_nodes() > 0:
                                            st.metric("平均次数", 
                                                    f"{2*G.number_of_edges()/G.number_of_nodes():.2f}")
                                
                                # メッセージに保存
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": claude_response,
                                    "graph_data": graph_data
                                })
                            else:
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": claude_response
                                })
                        
                        except Exception as e:
                            st.error(f"コードの実行中にエラーが発生しました: {str(e)}")
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": claude_response
                            })
                    else:
                        # コードブロックがない場合
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": claude_response
                        })
                
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

# サンプル質問
with st.sidebar:
    st.header("サンプル質問")
    sample_questions = [
        "10個のノードを持つスケールフリーネットワークを作成して",
        "完全グラフK5を作成して、各ノードの次数を教えて",
        "ランダムグラフを作成して、最短経路を計算して",
        "二部グラフを作成して可視化して",
        "有向グラフでPageRankを計算する例を見せて"
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()