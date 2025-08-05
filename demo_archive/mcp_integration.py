import streamlit as st
import json
import subprocess
import os

st.set_page_config(page_title="Claude MCP連携", page_icon="🔌", layout="wide")

st.title("🔌 Claude Desktop MCP連携")
st.markdown("""
このアプリは、Claude Desktop のMCP（Model Context Protocol）と連携して、
データ分析環境の情報をClaudeに提供します。
""")

# MCP設定の説明
st.header("MCPサーバーの設定方法")

st.markdown("""
### 1. MCP設定ファイルの場所

Windowsの場合：
```
%APPDATA%\\Claude\\claude_desktop_config.json
```

### 2. 設定ファイルに追加する内容

以下のJSON設定を追加してください：
""")

mcp_config = {
    "mcpServers": {
        "data-analysis-env": {
            "command": "python",
            "args": [
                f"C:\\Users\\kazum\\data-analysis-env\\mcp_server.py"
            ],
            "env": {
                "PYTHONPATH": "C:\\Users\\kazum\\data-analysis-env"
            }
        }
    }
}

st.code(json.dumps(mcp_config, indent=2), language="json")

# 現在の環境情報
st.header("現在の環境情報")

col1, col2 = st.columns(2)

with col1:
    st.subheader("インストール済みパッケージ")
    try:
        result = subprocess.run(
            ["pip", "list", "--format=json"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            # 主要パッケージのみ表示
            main_packages = [
                p for p in packages 
                if p['name'] in ['networkx', 'graphviz', 'streamlit', 
                               'pandas', 'numpy', 'matplotlib']
            ]
            for pkg in main_packages:
                st.text(f"{pkg['name']} == {pkg['version']}")
    except Exception as e:
        st.error(f"パッケージ情報の取得に失敗: {e}")

with col2:
    st.subheader("プロジェクトファイル")
    try:
        files = os.listdir("C:\\Users\\kazum\\data-analysis-env")
        py_files = [f for f in files if f.endswith('.py')]
        for f in py_files:
            st.text(f"📄 {f}")
    except Exception as e:
        st.error(f"ファイル一覧の取得に失敗: {e}")

# 使用例
st.header("Claude Desktopでの使用例")

st.markdown("""
### 設定後、Claude Desktopで以下のように質問できます：

1. **環境情報の確認**
   - 「data-analysis-envにインストールされているパッケージを教えて」
   - 「NetworkXのバージョンは？」

2. **コードの実行依頼**
   - 「data-analysis-envでグラフを作成して」
   - 「Streamlitアプリを起動して」

3. **ファイルの操作**
   - 「新しい分析スクリプトを作成して」
   - 「既存のデモアプリを修正して」
""")

# トラブルシューティング
with st.expander("トラブルシューティング"):
    st.markdown("""
    ### よくある問題：
    
    1. **MCPサーバーが起動しない**
       - パスが正しいか確認
       - Pythonがインストールされているか確認
    
    2. **Claudeが認識しない**
       - Claude Desktopを再起動
       - 設定ファイルのJSON形式を確認
    
    3. **コマンドが実行できない**
       - DevContainer内でのみ動作する機能もあります
    """)

# フッター
st.markdown("---")
st.info("💡 ヒント: Claude Desktop アプリと連携することで、より自然な対話形式でデータ分析を行えます。")