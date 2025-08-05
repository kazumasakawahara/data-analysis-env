import streamlit as st
import pandas as pd
import numpy as np
import anthropic
import os
from dotenv import load_dotenv
import json
import io
import matplotlib.pyplot as plt
import seaborn as sns

# 環境変数の読み込み
load_dotenv()

st.set_page_config(page_title="Claude データ分析アシスタント", page_icon="🤖", layout="wide")

st.title("🤖 Claude データ分析アシスタント")
st.markdown("Claudeと対話しながらデータの前処理や分析を行います。")

# データフォルダのパス
DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

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

# データファイルの選択
st.sidebar.header("データファイル")
try:
    files = os.listdir(RAW_DIR)
    data_files = [f for f in files if f.endswith(('.csv', '.xlsx', '.xls', '.json'))]
    
    if data_files:
        selected_file = st.sidebar.selectbox("分析するファイルを選択", data_files)
        file_path = os.path.join(RAW_DIR, selected_file)
        
        # データの読み込み
        @st.cache_data
        def load_data(path):
            try:
                if path.endswith('.csv'):
                    encodings = ['utf-8', 'shift-jis', 'cp932', 'latin-1']
                    for encoding in encodings:
                        try:
                            return pd.read_csv(path, encoding=encoding)
                        except:
                            continue
                elif path.endswith(('.xlsx', '.xls')):
                    return pd.read_excel(path)
                elif path.endswith('.json'):
                    return pd.read_json(path)
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {e}")
                return None
        
        df = load_data(file_path)
        
        if df is not None:
            st.sidebar.success(f"✅ {selected_file} を読み込みました")
            st.sidebar.write(f"サイズ: {df.shape[0]} 行 × {df.shape[1]} 列")
    else:
        st.sidebar.warning(f"📁 {RAW_DIR} フォルダにデータファイルを配置してください。")
        df = None
except:
    st.sidebar.error(f"❌ {RAW_DIR} フォルダが見つかりません。")
    df = None

# メインコンテンツ
if not st.session_state.api_key:
    st.warning("⚠️ APIキーを設定してください。")
    st.stop()

if df is None:
    st.info("データファイルを選択するか、アップロードしてください。")
    
    # ファイルアップロード
    uploaded_file = st.file_uploader(
        "データファイルをアップロード",
        type=['csv', 'xlsx', 'xls', 'json']
    )
    
    if uploaded_file:
        # ディレクトリの作成（存在しない場合）
        os.makedirs(RAW_DIR, exist_ok=True)
        
        # アップロードされたファイルを保存
        save_path = os.path.join(RAW_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ {uploaded_file.name} を保存しました。ページを更新してください。")
        st.rerun()
else:
    # Claudeクライアントの初期化
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    
    # チャット履歴の初期化
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.analysis_results = []
    
    # データのプレビュー
    with st.expander("📊 データのプレビュー", expanded=True):
        st.dataframe(df.head(10))
        
        # 基本情報
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("行数", f"{len(df):,}")
        with col2:
            st.metric("列数", f"{len(df.columns):,}")
        with col3:
            st.metric("欠損値の総数", f"{df.isnull().sum().sum():,}")
        with col4:
            st.metric("データ型の種類", f"{df.dtypes.nunique()}")
    
    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # 分析結果の再表示
            if message.get("analysis_result"):
                result = message["analysis_result"]
                if result["type"] == "dataframe":
                    st.dataframe(pd.DataFrame(result["data"]))
                elif result["type"] == "plot":
                    st.pyplot(result["figure"])
                elif result["type"] == "code":
                    st.code(result["code"], language="python")
    
    # ユーザー入力
    if prompt := st.chat_input("データについて質問してください（例：「欠損値の状況を教えて」「外れ値を検出して」）"):
        # ユーザーメッセージの追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Claudeへのリクエスト
        with st.chat_message("assistant"):
            with st.spinner("分析中..."):
                try:
                    # データの要約情報を準備
                    data_info = {
                        "shape": df.shape,
                        "columns": df.columns.tolist(),
                        "dtypes": df.dtypes.to_dict(),
                        "missing_values": df.isnull().sum().to_dict(),
                        "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
                        "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
                        "head": df.head().to_dict(),
                        "describe": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
                    }
                    
                    # システムプロンプト
                    system_prompt = f"""
あなたはデータ分析の専門家です。以下のデータについて質問に答えてください。

データ情報:
- ファイル名: {selected_file}
- サイズ: {data_info['shape'][0]} 行 × {data_info['shape'][1]} 列
- 列名: {', '.join(data_info['columns'][:10])}{'...' if len(data_info['columns']) > 10 else ''}
- データ型: {json.dumps({k: str(v) for k, v in list(data_info['dtypes'].items())[:5]}, ensure_ascii=False)}

回答する際は：
1. まず質問に対する説明を日本語で行う
2. 必要に応じて、実行可能なPythonコードを生成する
3. コードは以下の形式で記述する：

```python
# 必要なインポート
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# データ処理のコード
# df という変数名でDataFrameが利用可能です

# 結果を result 変数に格納
result = ...  # DataFrame、図、または処理済みデータ
```

4. 前処理の提案をする場合は、具体的な手順とコードを提供する
5. 可視化を行う場合は、matplotlib/seabornを使用する

重要：
- dfという変数でデータフレームにアクセスできます
- 結果は必ずresult変数に格納してください
- エラーが出ないよう、実行可能なコードを生成してください
"""
                    
                    # Claudeに質問
                    response = client.messages.create(
                        model="claude-3-sonnet-20241022",
                        max_tokens=3000,
                        system=system_prompt,
                        messages=[
                            {
                                "role": "user", 
                                "content": f"データの詳細情報:\n{json.dumps(data_info, ensure_ascii=False, indent=2)}\n\n質問: {prompt}"
                            }
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
                            exec_globals = {
                                'pd': pd,
                                'np': np,
                                'plt': plt,
                                'sns': sns,
                                'df': df.copy()  # データフレームのコピーを提供
                            }
                            
                            # matplotlib の設定
                            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
                            plt.rcParams['axes.unicode_minus'] = False
                            
                            exec(code, exec_globals)
                            
                            # 結果の処理
                            if 'result' in exec_globals:
                                result = exec_globals['result']
                                
                                if isinstance(result, pd.DataFrame):
                                    st.subheader("処理結果")
                                    st.dataframe(result)
                                    
                                    # データフレームを保存可能にする
                                    csv = result.to_csv(index=False, encoding='utf-8-sig')
                                    st.download_button(
                                        label="CSVダウンロード",
                                        data=csv,
                                        file_name=f"processed_{selected_file}",
                                        mime="text/csv"
                                    )
                                    
                                    # セッションに保存
                                    st.session_state['last_result'] = result
                                    
                                    # メッセージに保存
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": claude_response,
                                        "analysis_result": {
                                            "type": "dataframe",
                                            "data": result.to_dict()
                                        }
                                    })
                                
                                elif isinstance(result, plt.Figure):
                                    st.pyplot(result)
                                    plt.close()
                                    
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": claude_response,
                                        "analysis_result": {
                                            "type": "plot",
                                            "figure": result
                                        }
                                    })
                                
                                else:
                                    st.write("実行結果:", result)
                                    st.session_state.messages.append({
                                        "role": "assistant",
                                        "content": claude_response
                                    })
                            
                            # 現在の図があれば表示
                            if plt.get_fignums():
                                st.pyplot(plt.gcf())
                                plt.close('all')
                        
                        except Exception as e:
                            st.error(f"コードの実行中にエラーが発生しました: {str(e)}")
                            st.code(code, language="python")
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": claude_response,
                                "analysis_result": {
                                    "type": "code",
                                    "code": code
                                }
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
    st.header("💡 サンプル質問")
    
    sample_questions = [
        "データの基本的な統計情報を教えて",
        "欠損値の状況を詳しく分析して",
        "各列の分布を可視化して",
        "相関行列を作成して高い相関を持つ列を教えて",
        "外れ値を検出して可視化して",
        "カテゴリカル変数の頻度を分析して",
        "時系列データとして扱える列があるか確認して",
        "データクレンジングの提案をして",
        "ネットワーク分析用にデータを変換する方法を教えて"
    ]
    
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# 処理済みデータの保存
if st.sidebar.button("💾 最後の結果を保存"):
    if 'last_result' in st.session_state:
        result_df = st.session_state['last_result']
        file_name = st.sidebar.text_input("ファイル名", f"processed_{selected_file}")
        
        if file_name:
            save_path = os.path.join(PROCESSED_DIR, file_name)
            if file_name.endswith('.csv'):
                result_df.to_csv(save_path, index=False, encoding='utf-8-sig')
            else:
                result_df.to_csv(f"{save_path}.csv", index=False, encoding='utf-8-sig')
            
            st.sidebar.success(f"✅ {save_path} に保存しました")
    else:
        st.sidebar.warning("保存する結果がありません")

# フッター
st.markdown("---")
st.info("💡 ヒント: Claudeは自然な日本語で質問を理解し、適切なデータ分析コードを生成します。")