import json

import requests


if __name__ == "__main__":

    # response = requests.get("https://api.raydium.io/v2/auto/raydium/mainnet/price")
    # prices = response.json()
    # print(f"USDC/SOL Price: {prices['SOL-USDC']}")

    # response = requests.get("https://api.coingecko.com/api/v3/simple/price")
    # all = response.json()
    # print(F"all: {all}")

    # response = requests.get("https://api.orca.so/allPools")
    # pools = response.json()
    # print(f"all pools: {pools}")

    response = requests.get("https://api.raydium.io/v2/main/pairs")
    pools = response.json()
    output = open('../data/pools.json', 'w')
    output.write(json.dumps(pools))
    output.close()
    # print(f'pools: {pools}')