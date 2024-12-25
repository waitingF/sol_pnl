import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.config import *
import json
from datetime import datetime
from termcolor import colored
from tqdm import tqdm
import time


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    # options.add_argument("--headless")
    
    # Explicitly set the Chrome version (update this to match your Chrome version)
    uc.TARGET_VERSION = 131

    driver = uc.Chrome(options=options, version_main=131, use_subprocess=False)
    return driver


def fetch_wallet_data(driver, wallet_address):
    url = f'{API_URL}{wallet_address}'
    try:
        driver.get(url)
        time.sleep(0.1)  # Wait for 5 seconds to allow the page to load
        
        # Wait for the pre tag to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        
        # Get the page source and find the pre tag
        page_source = driver.page_source
        start_index = page_source.find("<pre>") + 5
        end_index = page_source.find("</pre>")
        json_data = page_source[start_index:end_index]
        
        return json.loads(json_data)
    except Exception as e:
        print(f'Error fetching data for wallet {wallet_address}: {e}')
        return None

def process_data(data, wallet_address, period):
    if data:
        print(f'processing data {json.dumps(data)}')
        try:
            sol_balance = data['data']['sol_balance'] if data['data']['sol_balance'] is not None else 0
            pnl_key = 'pnl_30d' if period == '30d' else 'pnl_7d'
            pnl = data['data'][pnl_key] if data['data'][pnl_key] is not None else 0
            pnl_7d = data['data']['pnl_7d'] if data['data']['pnl_7d'] is not None else 0
            pnl_30d = data['data']['pnl_30d'] if data['data']['pnl_30d'] is not None else 0
            winrate = data['data']['winrate'] if data['data']['winrate'] is not None else 0
            realized_profit_key = 'realized_profit_30d' if period == '30d' else 'realized_profit_7d'
            realized_profit = data['data'][realized_profit_key] if data['data'][realized_profit_key] is not None else 0
            last_active_timestamp = data['data'].get('last_active_timestamp') if data['data'].get('last_active_timestamp') is not None else 0
            last_pnl = pnl_7d * 100
            last_winrate = winrate * 100

            winrate_str = f'{round(last_winrate, 2)}%'
            if last_winrate > 60:
                winrate_str = colored(winrate_str, 'green')

            result = {
                'Wallet Address': wallet_address,
                'SOL Balance': f'{float(sol_balance):.2f}',
                f'PnL 7d': f'{round(pnl_7d, 2)}%',
                f'PnL 30d': f'{round(pnl_30d, 2)}%',
                'Winrate': winrate_str,
                f'Realized Profit {period}': f'{realized_profit:.2f}$',
                'Last Active Timestamp': datetime.fromtimestamp(last_active_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'Winrate Value': last_winrate,
            }
            return result
        except KeyError as e:
            print(f'ERROR: Make sure your list is correct.')
    return None


def gmgn_scrape(date_str: str, is_monitor_list: bool):
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    start_time = datetime.now()
    print(f'process date: {datetime.now()}')
    wallet_list_path = get_wallet_list_path(date_str, is_monitor_list=is_monitor_list)
    print(f'wallet_list: {wallet_list_path}')

    raw_data_file_path = get_raw_data_file_path(date_str, is_monitor_list=is_monitor_list)
    print(f'output file: {raw_data_file_path}')

    driver = setup_driver()

    try:
        with open(wallet_list_path, 'r') as file:
            wallet_addresses = file.read().strip().split('\n')
            wallet_addresses = set(wallet_addresses)
            wallet_addresses = list(wallet_addresses)
            print(f'wallet count {len(wallet_addresses)}')

        with open(raw_data_file_path, 'a') as file:
            print(f'processing {len(wallet_addresses)} wallet address at {datetime.now()}')
            for wallet_address in tqdm(wallet_addresses, desc="wallet pnl scrape progress"):
                if wallet_address.strip():
                    raw_data = fetch_wallet_data(driver, wallet_address)
                    if raw_data and raw_data['data']:
                        actual_data = raw_data['data']
                        actual_data['wallet'] = wallet_address
                        file.write(json.dumps(actual_data) + '\n')
    except FileNotFoundError:
        print("The file 'list.txt' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}', e.with_traceback())
    finally:
        driver.quit()

    end_time = datetime.now()
    print(f'total process time: {end_time - start_time}')


if __name__ == "__main__":
    gmgn_scrape(None)
