import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
HELIUS_API_KEY = os.getenv('HELIUS_API_KEY')
HELIUS_API_URL = "https://api.helius.xyz/v0"

# 默认配置
DEFAULT_ADDRESS = "9WiFm4KzEbMvn1HQBVMb4W49S9rNfqhqjK9sjXJqiCbQ"
DEFAULT_DAYS = 7

# 数据存储路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../data')
