import os

WEBHOOK_TOPIC = "wallet-monitor-webhook"
BOOTSTRAP_SERVER = "54.169.129.35:9092"
CONSUMER_GROUP = "txn-consumer-01"

#### scrape url
API_URL = 'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/'

#### data path
RAW_DATA_DIR = '../gmgnai_scraper/data'
ALL_WALLET_LIST_FILE_NAME = 'all_wallet_list.txt'
ALL_RESULT_BASE_FILE_NAME = 'all_wallet_pnl_data.txt'
ALL_RESULT_CSV_FILE_NAME = 'all_wallet_pnl_data.csv'
MONITOR_WALLET_LIST_FILE_NAME = 'monitor_wallet_list.txt'
MONITOR_RESULT_BASE_FILE_NAME = 'monitor_wallet_pnl_data.txt'
MONITOR_RESULT_CSV_FILE_NAME = 'monitor_wallet_pnl_data.csv'


def get_wallet_list_path(date_str: str, is_monitor_list: bool) -> str:
    date_dir = os.path.join(RAW_DATA_DIR, date_str)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    if is_monitor_list:
        output_raw_data_path = os.path.join(date_dir, MONITOR_WALLET_LIST_FILE_NAME)
    else:
        output_raw_data_path = os.path.join(date_dir, ALL_WALLET_LIST_FILE_NAME)
    return output_raw_data_path


def get_raw_data_file_path(date_str: str, is_monitor_list: bool) -> str:
    date_dir = os.path.join(RAW_DATA_DIR, date_str)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    if is_monitor_list:
        output_raw_data_path = os.path.join(date_dir, MONITOR_RESULT_BASE_FILE_NAME)
    else:
        output_raw_data_path = os.path.join(date_dir, ALL_RESULT_BASE_FILE_NAME)
    return output_raw_data_path


def get_csv_data_file_path(date_str: str, is_monitor_list: bool) -> str:
    date_dir = os.path.join(RAW_DATA_DIR, date_str)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    if is_monitor_list:
        output_raw_data_path = os.path.join(date_dir, MONITOR_RESULT_CSV_FILE_NAME)
    else:
        output_raw_data_path = os.path.join(date_dir, ALL_RESULT_CSV_FILE_NAME)
    return output_raw_data_path


PGHOST='xxxx'
PGDATABASE='neondb'
PGUSER='neondb_owner'
PGPASSWORD='xxxx'
