import requests
from datetime import datetime, timedelta
import pandas as pd
import config

class SolanaDataFetcher:
    def __init__(self):
        self.api_key = config.HELIUS_API_KEY
        if not self.api_key:
            raise ValueError("HELIUS_API_KEY not found in environment variables")
        self.base_url = config.HELIUS_API_URL

    def fetch_transactions(self, address: str, days: int = 7):
        """
        获取指定地址的交易历史
        
        Args:
            address (str): Solana钱包地址
            days (int): 获取天数（7或30）
            
        Returns:
            pd.DataFrame: 包含交易数据的DataFrame
        """
        if days not in [7, 30]:
            raise ValueError("days must be either 7 or 30")

        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        url = f"{self.base_url}/addresses/{address}/transactions"
        
        params = {
            "api-key": self.api_key,
            # "before": end_time.isoformat(),
            # "after": start_time.isoformat(),
            # "type": "ALL"
        }

        try:
            print(f"Fetching transactions for address: {address} from {start_time} to {end_time}")  # Debug info
            response = requests.get(url, params=params)
            response.raise_for_status()
            transactions = response.json()
            return pd.DataFrame(transactions)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transactions: {e}")
            return None
