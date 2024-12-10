import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import os
import config

class PnLVisualizer:
    def __init__(self, save_dir=None):
        self.save_dir = save_dir or config.DATA_DIR
        os.makedirs(self.save_dir, exist_ok=True)

    def plot_daily_pnl(self, daily_data: pd.DataFrame, address: str):
        """
        绘制每日盈亏趋势图
        
        Args:
            daily_data (pd.DataFrame): 包含每日盈亏数据的DataFrame
            address (str): 钱包地址
        """
        fig = go.Figure()
        
        # 添加盈亏曲线
        fig.add_trace(go.Scatter(
            x=daily_data.index,
            y=daily_data['net_change'],
            mode='lines+markers',
            name='Daily PnL',
            line=dict(color='blue')
        ))

        # 设置图表布局
        fig.update_layout(
            title=f'Daily PnL Analysis for {address[:8]}...{address[-4:]}',
            xaxis_title='Date',
            yaxis_title='PnL (SOL)',
            hovermode='x unified'
        )

        # 保存图表
        fig.write_html(os.path.join(self.save_dir, f'daily_pnl_{datetime.now().strftime("%Y%m%d")}.html'))

    def plot_transaction_volume(self, daily_data: pd.DataFrame, address: str):
        """
        绘制交易量分析图
        
        Args:
            daily_data (pd.DataFrame): 包含每日交易数据的DataFrame
            address (str): 钱包地址
        """
        fig = go.Figure()

        # 添加交易量柱状图
        fig.add_trace(go.Bar(
            x=daily_data.index,
            y=daily_data['transaction_count'],
            name='Transaction Volume'
        ))

        # 设置图表布局
        fig.update_layout(
            title=f'Daily Transaction Volume for {address[:8]}...{address[-4:]}',
            xaxis_title='Date',
            yaxis_title='Number of Transactions',
            bargap=0.2
        )

        # 保存图表
        fig.write_html(os.path.join(self.save_dir, f'transaction_volume_{datetime.now().strftime("%Y%m%d")}.html'))
