import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

class TransactionAnalyzer:
    def __init__(self, transactions_df: pd.DataFrame, wallet_address: str):
        self.df = transactions_df
        self.wallet_address = wallet_address.lower()
        
    def _process_transaction(self, transaction: Dict) -> Dict:
        """
        处理单个交易，计算SOL的流入流出
        
        Args:
            transaction (Dict): 单个交易数据
            
        Returns:
            Dict: 包含处理后的交易信息
        """
        result = {
            'timestamp': transaction['timestamp'],
            'signature': transaction['signature'],
            'success': transaction.get('success', True),
            'fee': float(transaction.get('fee', 0)) / 1e9 if transaction.get('feePayer').lower() == self.wallet_address else 0,  # 转换为SOL单位
            'sol_in': 0.0,
            'sol_out': 0.0,
            'net_change': 0.0,
            'type': 'unknown'
        }
        
        # 处理预算账户变化
        if 'accountData' in transaction:
            for account in transaction['accountData']:
                if account['account'].lower() == self.wallet_address:
                    # 计算SOL余额变化
                    # pre_balance = float(account.get('preBalance', 0)) / 1e9
                    # post_balance = float(account.get('postBalance', 0)) / 1e9
                    # balance_change = post_balance - pre_balance
                    balance_change = float(account.get('nativeBalanceChange', 0)) / 1e9
                    
                    if balance_change > 0:
                        result['sol_in'] += balance_change
                    else:
                        result['sol_out'] += abs(balance_change)
        
        # 计算净变化（包含手续费）
        result['net_change'] = result['sol_in'] - result['sol_out'] - result['fee']
        
        # 确定交易类型
        if result['sol_in'] > 0 and result['sol_out'] == 0:
            result['type'] = 'receive'
        elif result['sol_out'] > 0 and result['sol_in'] == 0:
            result['type'] = 'send'
        elif result['sol_in'] > 0 and result['sol_out'] > 0:
            result['type'] = 'swap'
        elif result['sol_in'] == 0 and result['sol_out'] == 0 and result['fee'] > 0:
            result['type'] = 'fee_only'
            
        return result
        
    def calculate_pnl(self) -> Dict:
        """
        计算总体盈亏情况
        
        Returns:
            Dict: 包含各种分析指标的字典
        """
        if self.df is None or self.df.empty:
            return None
            
        # 处理每笔交易
        processed_transactions = []
        for _, tx in self.df.iterrows():
            processed_tx = self._process_transaction(tx)
            processed_transactions.append(processed_tx)
            
        # 转换为DataFrame便于分析
        analysis_df = pd.DataFrame(processed_transactions)
        
        # 计算各项指标
        successful_txs = analysis_df[analysis_df['success'] == True]
        
        analysis = {
            'total_transactions': len(analysis_df),
            'successful_transactions': len(successful_txs),
            'first_transaction_time': analysis_df['timestamp'].min(),
            'last_transaction_time': analysis_df['timestamp'].max(),
            'total_sol_in': successful_txs['sol_in'].sum(),
            'total_sol_out': successful_txs['sol_out'].sum(),
            'total_fees': successful_txs['fee'].sum(),
            'net_pnl': successful_txs['net_change'].sum(),
            'largest_inflow': successful_txs['sol_in'].max(),
            'largest_outflow': successful_txs['sol_out'].max(),
            'transaction_types': {
                'receive': len(successful_txs[successful_txs['type'] == 'receive']),
                'send': len(successful_txs[successful_txs['type'] == 'send']),
                'swap': len(successful_txs[successful_txs['type'] == 'swap']),
                'fee_only': len(successful_txs[successful_txs['type'] == 'fee_only'])
            }
        }
        
        return analysis
        
    def get_daily_summary(self) -> pd.DataFrame:
        """
        获取每日交易汇总
        
        Returns:
            pd.DataFrame: 每日交易统计数据
        """
        if self.df is None or self.df.empty:
            return None
            
        # 处理所有交易
        processed_transactions = [self._process_transaction(tx) for _, tx in self.df.iterrows()]
        daily_df = pd.DataFrame(processed_transactions)
        
        # 转换时间戳为日期
        daily_df['date'] = pd.to_datetime(daily_df['timestamp']).dt.date
        
        # 按日期分组统计
        daily_summary = daily_df.groupby('date').agg({
            'net_change': 'sum',
            'sol_in': 'sum',
            'sol_out': 'sum',
            'fee': 'sum',
            'signature': 'count'  # 计算交易数量
        }).rename(columns={'signature': 'transaction_count'})
        
        # 计算累计盈亏
        daily_summary['cumulative_pnl'] = daily_summary['net_change'].cumsum()
        
        return daily_summary
