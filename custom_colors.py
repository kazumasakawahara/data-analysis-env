"""
カスタムカラーパレット設定
グラフの色分けを改善するための設定
"""

# カテゴリ別のカラーマップ
CATEGORY_COLORS = {
    # 性別
    '男性': '#1f77b4',  # 青
    '女性': '#ff7f0e',  # オレンジ
    'Male': '#1f77b4',
    'Female': '#ff7f0e',
    
    # 地域（日本の主要都市）
    '東京': '#2ca02c',     # 緑
    '大阪': '#d62728',     # 赤
    '名古屋': '#9467bd',   # 紫
    '福岡': '#8c564b',     # 茶
    '札幌': '#e377c2',     # ピンク
    '仙台': '#7f7f7f',     # 灰
    '広島': '#bcbd22',     # 黄緑
    '京都': '#17becf',     # シアン
    
    # 商品カテゴリ
    '商品A': '#1f77b4',
    '商品B': '#ff7f0e', 
    '商品C': '#2ca02c',
    '商品D': '#d62728',
    '商品E': '#9467bd',
    
    # グループ分類
    'A': '#e74c3c',  # 赤
    'B': '#3498db',  # 青
    'C': '#2ecc71',  # 緑
    'D': '#f39c12',  # オレンジ
    'E': '#9b59b6',  # 紫
    
    # Yes/No, True/False
    'Yes': '#2ecc71',
    'No': '#e74c3c',
    'True': '#2ecc71',
    'False': '#e74c3c',
    'はい': '#2ecc71',
    'いいえ': '#e74c3c',
}

# 連続値用のカラーマップ
SEQUENTIAL_COLORSCALES = {
    'default': 'Viridis',
    'temperature': 'RdBu_r',  # 温度（青→赤）
    'diverging': 'RdBu',      # 発散型（赤→青）
    'sequential': 'Blues',     # 連続（薄青→濃青）
    'heatmap': 'YlOrRd',      # ヒートマップ（黄→赤）
}

# アクセシビリティを考慮した配色（色覚多様性対応）
ACCESSIBLE_COLORS = [
    '#0173B2',  # 青
    '#DE8F05',  # オレンジ
    '#029E73',  # 緑
    '#CC78BC',  # 薄紫
    '#CA9161',  # 茶
    '#FBAFE4',  # ピンク
    '#949494',  # 灰
    '#ECE133',  # 黄
    '#56B4E9',  # 水色
]

def get_color_mapping(series):
    """
    データシリーズに基づいて適切なカラーマップを返す
    
    Parameters:
    -----------
    series : pd.Series
        カテゴリカルデータのシリーズ
        
    Returns:
    --------
    dict : カテゴリとカラーのマッピング
    """
    unique_values = series.unique()
    color_map = {}
    
    # 既定のカテゴリカラーを確認
    for value in unique_values:
        if str(value) in CATEGORY_COLORS:
            color_map[value] = CATEGORY_COLORS[str(value)]
    
    # 未定義のカテゴリにはアクセシブルカラーを割り当て
    unassigned_values = [v for v in unique_values if v not in color_map]
    for i, value in enumerate(unassigned_values):
        if i < len(ACCESSIBLE_COLORS):
            color_map[value] = ACCESSIBLE_COLORS[i]
        else:
            # アクセシブルカラーが足りない場合は、デフォルトのPlotlyカラーを使用
            color_map[value] = None
    
    return color_map

def apply_custom_colors(fig, color_column=None, data=None):
    """
    Plotlyのfigureにカスタムカラーを適用
    
    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        Plotlyのfigureオブジェクト
    color_column : str
        色分けに使用した列名
    data : pd.DataFrame
        元のデータフレーム
        
    Returns:
    --------
    fig : 更新されたfigure
    """
    if color_column and data is not None and color_column in data.columns:
        color_map = get_color_mapping(data[color_column])
        
        # color_discrete_mapを更新
        fig.update_traces(marker=dict(
            size=10,  # マーカーサイズを大きくして見やすく
            line=dict(width=1, color='DarkSlateGrey')  # 境界線を追加
        ))
        
    return fig

# Plotlyのデフォルト設定を更新
import plotly.io as pio

# カスタムテンプレートの作成
pio.templates["custom"] = pio.templates["plotly_white"]
pio.templates["custom"].layout.colorway = ACCESSIBLE_COLORS

# デフォルトテンプレートとして設定
pio.templates.default = "custom"
