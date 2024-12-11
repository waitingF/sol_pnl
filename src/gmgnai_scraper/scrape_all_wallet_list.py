from datetime import datetime

from gmgn_scraper import gmgn_scrape
from database_helper import get_all_wallet_addresses, write_wallet_pnl_to_postgresql, get_all_wallet_first_degrees, \
    write_top_profit_wallet_pnl_to_postgresql

if __name__ == '__main__':
    start_time = datetime.now()
    date_str = datetime.now().strftime('%Y-%m-%d')
    date_str = '2024-12-19'
    is_monitor = False
    # get_all_wallet_addresses(date_str)
    # gmgn_scrape(date_str, is_monitor_list=is_monitor)
    write_wallet_pnl_to_postgresql(date_str, is_monitor_list=False)

    print(f'total time cost:{datetime.now() - start_time}')
