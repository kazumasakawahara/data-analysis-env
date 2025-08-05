import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

st.set_page_config(page_title="データ前処理アシスタント", page_icon="🧹", layout="wide")

st.title("🧹 データ前処理アシスタント")
st.markdown("データのクレンジング、欠損値補完、変換などの前処理を支援します。")

# データフォルダのパス
DATA_DIR = "data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# サイドバー：ファイル選択
st.sidebar.header("ファイル選択")

# rawフォルダ内のファイルをリスト
try:
    files = os.listdir(RAW_DIR)
    data_files = [f for f in files if f.endswith(('.csv', '.xlsx', '.xls', '.json'))]
    
    if data_files:
        selected_file = st.sidebar.selectbox("分析するファイルを選択", data_files)
        file_path = os.path.join(RAW_DIR, selected_file)
    else:
        st.warning(f"📁 {RAW_DIR} フォルダにデータファイルを配置してください。")
        st.stop()
except:
    st.error(f"❌ {RAW_DIR} フォルダが見つかりません。")
    st.stop()

# ファイルアップロード機能も提供
uploaded_file = st.sidebar.file_uploader(
    "または新しいファイルをアップロード",
    type=['csv', 'xlsx', 'xls', 'json']
)

if uploaded_file:
    # アップロードされたファイルを保存
    save_path = os.path.join(RAW_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"✅ {uploaded_file.name} を保存しました")
    selected_file = uploaded_file.name
    file_path = save_path

# データの読み込み
@st.cache_data
def load_data(path):
    """データファイルを読み込む"""
    try:
        if path.endswith('.csv'):
            # エンコーディングを試行
            encodings = ['utf-8', 'shift-jis', 'cp932', 'latin-1']
            for encoding in encodings:
                try:
                    return pd.read_csv(path, encoding=encoding)
                except:
                    continue
            st.error("CSVファイルの読み込みに失敗しました。")
            return None
        elif path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(path)
        elif path.endswith('.json'):
            return pd.read_json(path)
    except Exception as e:
        st.error(f"ファイル読み込みエラー: {e}")
        return None

# データの読み込みと表示
df = load_data(file_path)

if df is not None:
    st.header("📊 データの概要")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("行数", f"{len(df):,}")
    with col2:
        st.metric("列数", f"{len(df.columns):,}")
    with col3:
        st.metric("欠損値の総数", f"{df.isnull().sum().sum():,}")
    with col4:
        st.metric("メモリ使用量", f"{df.memory_usage().sum() / 1024**2:.2f} MB")
    
    # データプレビュー
    st.subheader("データプレビュー")
    preview_rows = st.slider("表示する行数", 5, 100, 10)
    st.dataframe(df.head(preview_rows))
    
    # タブで異なる前処理を整理
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 データ診断", 
        "🧹 欠損値処理", 
        "🔄 データ型変換",
        "📊 異常値検出",
        "💾 処理済みデータ保存"
    ])
    
    with tab1:
        st.header("データ診断レポート")
        
        # データ型の情報
        st.subheader("列のデータ型")
        dtype_df = pd.DataFrame({
            'データ型': df.dtypes,
            'ユニーク値数': df.nunique(),
            '欠損値数': df.isnull().sum(),
            '欠損率(%)': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(dtype_df)
        
        # 基本統計量
        st.subheader("数値列の基本統計量")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(df[numeric_cols].describe())
        else:
            st.info("数値列がありません。")
        
        # 相関行列
        if len(numeric_cols) > 1:
            st.subheader("相関行列")
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
            st.pyplot(fig)
    
    with tab2:
        st.header("欠損値処理")
        
        # 欠損値の可視化
        missing_df = pd.DataFrame({
            '列名': df.columns,
            '欠損値数': df.isnull().sum().values,
            '欠損率(%)': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        missing_df = missing_df[missing_df['欠損値数'] > 0].sort_values('欠損値数', ascending=False)
        
        if len(missing_df) > 0:
            st.subheader("欠損値のある列")
            st.dataframe(missing_df)
            
            # 欠損値処理方法の選択
            st.subheader("欠損値処理方法")
            
            # 処理対象の列を選択
            selected_cols = st.multiselect(
                "処理する列を選択",
                missing_df['列名'].tolist(),
                default=missing_df['列名'].tolist()
            )
            
            if selected_cols:
                # 処理方法を選択
                method = st.selectbox(
                    "処理方法",
                    [
                        "削除（行を削除）",
                        "削除（列を削除）",
                        "平均値で補完（数値列のみ）",
                        "中央値で補完（数値列のみ）",
                        "最頻値で補完",
                        "前方補完（時系列データ）",
                        "後方補完（時系列データ）",
                        "線形補間（数値列のみ）",
                        "固定値で補完"
                    ]
                )
                
                # 固定値補完の場合は値を入力
                fill_value = None
                if method == "固定値で補完":
                    fill_value = st.text_input("補完する値を入力")
                
                # 処理実行ボタン
                if st.button("欠損値処理を実行"):
                    df_processed = df.copy()
                    
                    try:
                        if method == "削除（行を削除）":
                            df_processed = df_processed.dropna(subset=selected_cols)
                        elif method == "削除（列を削除）":
                            df_processed = df_processed.drop(columns=selected_cols)
                        elif method == "平均値で補完（数値列のみ）":
                            for col in selected_cols:
                                if df_processed[col].dtype in [np.float64, np.int64]:
                                    df_processed[col].fillna(df_processed[col].mean(), inplace=True)
                        elif method == "中央値で補完（数値列のみ）":
                            for col in selected_cols:
                                if df_processed[col].dtype in [np.float64, np.int64]:
                                    df_processed[col].fillna(df_processed[col].median(), inplace=True)
                        elif method == "最頻値で補完":
                            for col in selected_cols:
                                mode_val = df_processed[col].mode()
                                if len(mode_val) > 0:
                                    df_processed[col].fillna(mode_val[0], inplace=True)
                        elif method == "前方補完（時系列データ）":
                            df_processed[selected_cols] = df_processed[selected_cols].fillna(method='ffill')
                        elif method == "後方補完（時系列データ）":
                            df_processed[selected_cols] = df_processed[selected_cols].fillna(method='bfill')
                        elif method == "線形補間（数値列のみ）":
                            for col in selected_cols:
                                if df_processed[col].dtype in [np.float64, np.int64]:
                                    df_processed[col] = df_processed[col].interpolate(method='linear')
                        elif method == "固定値で補完" and fill_value:
                            df_processed[selected_cols] = df_processed[selected_cols].fillna(fill_value)
                        
                        st.success("✅ 欠損値処理が完了しました！")
                        st.session_state['df_processed'] = df_processed
                        
                        # 処理結果の表示
                        st.subheader("処理後のデータ")
                        st.write(f"処理前: {len(df)} 行 → 処理後: {len(df_processed)} 行")
                        st.dataframe(df_processed.head())
                        
                    except Exception as e:
                        st.error(f"処理中にエラーが発生しました: {e}")
        else:
            st.success("✨ 欠損値はありません！")
    
    with tab3:
        st.header("データ型変換")
        
        # 現在のデータ型を表示
        st.subheader("現在のデータ型")
        dtype_info = pd.DataFrame({
            '列名': df.columns,
            '現在の型': df.dtypes
        })
        st.dataframe(dtype_info)
        
        # 型変換の設定
        st.subheader("データ型を変換")
        col_to_convert = st.selectbox("変換する列", df.columns)
        new_type = st.selectbox(
            "新しいデータ型",
            ["int64", "float64", "string", "datetime", "category", "bool"]
        )
        
        # 日付形式の指定（datetime選択時）
        date_format = None
        if new_type == "datetime":
            date_format = st.text_input(
                "日付形式（例: %Y-%m-%d）",
                help="空欄の場合は自動推定します"
            )
        
        if st.button("データ型を変換"):
            try:
                df_converted = df.copy()
                if new_type == "datetime":
                    if date_format:
                        df_converted[col_to_convert] = pd.to_datetime(
                            df_converted[col_to_convert], 
                            format=date_format
                        )
                    else:
                        df_converted[col_to_convert] = pd.to_datetime(
                            df_converted[col_to_convert]
                        )
                elif new_type == "category":
                    df_converted[col_to_convert] = df_converted[col_to_convert].astype('category')
                else:
                    df_converted[col_to_convert] = df_converted[col_to_convert].astype(new_type)
                
                st.success("✅ データ型の変換が完了しました！")
                st.session_state['df_processed'] = df_converted
                
                # 変換結果の確認
                st.write(f"変換後の型: {df_converted[col_to_convert].dtype}")
                st.dataframe(df_converted[[col_to_convert]].head())
                
            except Exception as e:
                st.error(f"変換エラー: {e}")
    
    with tab4:
        st.header("異常値検出")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("分析する列を選択", numeric_cols)
            
            # 基本統計量
            col_stats = df[selected_col].describe()
            st.subheader(f"{selected_col} の統計情報")
            st.dataframe(col_stats)
            
            # ボックスプロット
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # ボックスプロット
            ax1.boxplot(df[selected_col].dropna())
            ax1.set_title(f"{selected_col} のボックスプロット")
            ax1.set_ylabel("値")
            
            # ヒストグラム
            ax2.hist(df[selected_col].dropna(), bins=30, edgecolor='black')
            ax2.set_title(f"{selected_col} のヒストグラム")
            ax2.set_xlabel("値")
            ax2.set_ylabel("頻度")
            
            st.pyplot(fig)
            
            # 異常値検出方法
            st.subheader("異常値の検出方法")
            method = st.selectbox(
                "検出方法",
                ["IQR（四分位範囲）法", "標準偏差法", "パーセンタイル法"]
            )
            
            if method == "IQR（四分位範囲）法":
                Q1 = df[selected_col].quantile(0.25)
                Q3 = df[selected_col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
                
            elif method == "標準偏差法":
                n_std = st.slider("標準偏差の倍数", 1.0, 4.0, 3.0, 0.5)
                mean = df[selected_col].mean()
                std = df[selected_col].std()
                lower_bound = mean - n_std * std
                upper_bound = mean + n_std * std
                
                outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
                
            else:  # パーセンタイル法
                lower_pct = st.slider("下限パーセンタイル", 0, 10, 1)
                upper_pct = st.slider("上限パーセンタイル", 90, 100, 99)
                lower_bound = df[selected_col].quantile(lower_pct / 100)
                upper_bound = df[selected_col].quantile(upper_pct / 100)
                
                outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
            
            st.write(f"**下限値**: {lower_bound:.2f}")
            st.write(f"**上限値**: {upper_bound:.2f}")
            st.write(f"**異常値の数**: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
            
            if len(outliers) > 0:
                st.subheader("異常値のプレビュー")
                st.dataframe(outliers[[selected_col]].head(10))
                
                # 異常値の処理
                if st.checkbox("異常値を処理する"):
                    treatment = st.selectbox(
                        "処理方法",
                        ["削除", "上限・下限でクリップ", "欠損値に変換"]
                    )
                    
                    if st.button("異常値処理を実行"):
                        df_treated = df.copy()
                        
                        if treatment == "削除":
                            df_treated = df_treated[
                                (df_treated[selected_col] >= lower_bound) & 
                                (df_treated[selected_col] <= upper_bound)
                            ]
                        elif treatment == "上限・下限でクリップ":
                            df_treated[selected_col] = df_treated[selected_col].clip(
                                lower=lower_bound, 
                                upper=upper_bound
                            )
                        else:  # 欠損値に変換
                            df_treated.loc[
                                (df_treated[selected_col] < lower_bound) | 
                                (df_treated[selected_col] > upper_bound), 
                                selected_col
                            ] = np.nan
                        
                        st.success("✅ 異常値処理が完了しました！")
                        st.session_state['df_processed'] = df_treated
                        st.write(f"処理前: {len(df)} 行 → 処理後: {len(df_treated)} 行")
        else:
            st.info("数値列がありません。")
    
    with tab5:
        st.header("処理済みデータの保存")
        
        # 処理済みデータの確認
        if 'df_processed' in st.session_state:
            df_to_save = st.session_state['df_processed']
            st.success("✅ 処理済みデータがあります")
        else:
            df_to_save = df
            st.info("ℹ️ 元のデータを保存します（前処理が実行されていません）")
        
        # データのプレビュー
        st.subheader("保存するデータのプレビュー")
        st.dataframe(df_to_save.head())
        
        # ファイル名の設定
        base_name = os.path.splitext(selected_file)[0]
        default_name = f"{base_name}_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        file_name = st.text_input("保存するファイル名（拡張子なし）", default_name)
        file_format = st.selectbox("保存形式", ["CSV", "Excel", "JSON"])
        
        # 保存オプション
        if file_format == "CSV":
            encoding = st.selectbox("エンコーディング", ["utf-8", "shift-jis", "cp932"])
            include_index = st.checkbox("インデックスを含める", value=False)
        
        # 保存実行
        if st.button("💾 データを保存"):
            try:
                if file_format == "CSV":
                    save_path = os.path.join(PROCESSED_DIR, f"{file_name}.csv")
                    df_to_save.to_csv(
                        save_path, 
                        encoding=encoding, 
                        index=include_index
                    )
                elif file_format == "Excel":
                    save_path = os.path.join(PROCESSED_DIR, f"{file_name}.xlsx")
                    df_to_save.to_excel(save_path, index=False)
                else:  # JSON
                    save_path = os.path.join(PROCESSED_DIR, f"{file_name}.json")
                    df_to_save.to_json(save_path, orient='records', force_ascii=False)
                
                st.success(f"✅ ファイルを保存しました: {save_path}")
                
                # 処理レポートの生成
                report = {
                    "処理日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "元ファイル": selected_file,
                    "処理後ファイル": os.path.basename(save_path),
                    "元の行数": len(df),
                    "処理後の行数": len(df_to_save),
                    "元の列数": len(df.columns),
                    "処理後の列数": len(df_to_save.columns),
                    "削除された行数": len(df) - len(df_to_save),
                    "削除された列": list(set(df.columns) - set(df_to_save.columns))
                }
                
                # レポートの保存
                report_path = os.path.join(PROCESSED_DIR, f"{file_name}_report.json")
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                
                st.info(f"📄 処理レポートも保存しました: {report_path}")
                
            except Exception as e:
                st.error(f"保存エラー: {e}")

# サイドバーに使い方を追加
st.sidebar.markdown("---")
st.sidebar.header("💡 使い方のヒント")
st.sidebar.markdown("""
### Claudeに依頼できること：

1. **データの診断**
   - 「このデータの問題点を教えて」
   - 「欠損値の傾向を分析して」

2. **前処理の提案**
   - 「このデータに適した前処理を提案して」
   - 「外れ値をどう処理すべき？」

3. **コード生成**
   - 「特定の前処理のPythonコードを書いて」
   - 「カスタム処理関数を作って」

4. **分析準備**
   - 「ネットワーク分析用にデータを変換して」
   - 「時系列分析の準備をして」
""")

# フッター
st.markdown("---")
st.markdown("このアプリケーションは、データの前処理を支援します。処理済みデータは `data/processed/` フォルダに保存されます。")