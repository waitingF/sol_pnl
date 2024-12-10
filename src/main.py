import argparse
from datetime import datetime
import os
from config import HELIUS_API_KEY, HELIUS_API_URL, DEFAULT_ADDRESS, DEFAULT_DAYS
from data_fetcher import SolanaDataFetcher
from analyzer import TransactionAnalyzer
from visualizer import PnLVisualizer
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description='Solana PnL Analyzer')
    parser.add_argument('--address', type=str, default=DEFAULT_ADDRESS,
                      help='Solana wallet address to analyze')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS,
                      choices=[7, 30],
                      help='Number of days to analyze (7 or 30)')
    parser.add_argument('--output', type=str, default='data',
                      help='Output directory for reports and visualizations')
    return parser.parse_args()


def main():
    base_dir = '/Users/kongwei/CascadeProjects/sol_pnl'
    os.chdir(base_dir)

    # 解析命令行参数
    args = parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)
    txs_result_path = args.output + "/txs"
    os.makedirs(txs_result_path, exist_ok=True)

    # 初始化组件
    fetcher = SolanaDataFetcher()
    visualizer = PnLVisualizer(args.output)
    
    print(f"开始分析地址: {args.address}")
    print(f"分析周期: {args.days} 天")
    
    try:
        address_txs_result_path = txs_result_path + "/" + args.address + ".json"
        if os.path.exists(address_txs_result_path):
            transactions_df = pd.read_json(address_txs_result_path)
        else:
            # 获取交易数据
            transactions_df = fetcher.fetch_transactions(args.address, args.days)
            if transactions_df is None or transactions_df.empty:
                print("未找到交易数据")
                return
            # 保存transaction数据
            transactions_df.to_json(address_txs_result_path, index=False)
        # return
        # 分析数据
        analyzer = TransactionAnalyzer(transactions_df, args.address)
        analysis_results = analyzer.calculate_pnl()
        daily_summary = analyzer.get_daily_summary()
        
        if analysis_results:
            print("\n=== 分析结果 ===")
            print(f"总交易次数: {analysis_results['total_transactions']}")
            print(f"成功交易次数: {analysis_results['successful_transactions']}")
            print(f"总流入SOL: {analysis_results['total_sol_in']:.4f}")
            print(f"总流出SOL: {analysis_results['total_sol_out']:.4f}")
            print(f"总手续费: {analysis_results['total_fees']:.4f}")
            print(f"净盈亏: {analysis_results['net_pnl']:.4f}")
            print("\n交易类型统计:")
            for tx_type, count in analysis_results['transaction_types'].items():
                print(f"- {tx_type}: {count}")
            
        # 生成可视化
        if daily_summary is not None:
            visualizer.plot_daily_pnl(daily_summary, args.address)
            visualizer.plot_transaction_volume(daily_summary, args.address)
            print(f"\n可视化报告已保存至: {args.output}")
            
    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")


if __name__ == "__main__":
    main()
