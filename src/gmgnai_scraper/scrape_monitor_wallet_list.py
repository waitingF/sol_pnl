import sys
import os
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime

from src.utils.database_helper import write_wallet_pnl_to_postgresql, get_all_wallet_first_degrees, \
    write_top_profit_wallet_pnl_to_postgresql, get_monitor_wallet_addresses
from gmgn_scraper import gmgn_scrape

if __name__ == '__main__':
    start_time = datetime.now()
    date_str = datetime.now().strftime('%Y-%m-%d')
    is_monitor = True
    get_monitor_wallet_addresses(date_str)
    gmgn_scrape(date_str, is_monitor_list=is_monitor)
    write_wallet_pnl_to_postgresql(date_str, is_monitor_list=is_monitor)

    holders_map = get_all_wallet_first_degrees()
    write_top_profit_wallet_pnl_to_postgresql(date_str, realized=True, holders_map=holders_map, is_monitor_list=is_monitor)
    write_top_profit_wallet_pnl_to_postgresql(date_str, realized=False, holders_map=holders_map, is_monitor_list=is_monitor)
    print(f'total time cost:{datetime.now() - start_time}')
