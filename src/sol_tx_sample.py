from solana.rpc.api import Client


if __name__ == '__main__':

    # 初始化 Solana RPC 客户端
    rpc_url = "https://api.mainnet-beta.solana.com"
    client = Client(rpc_url)


    # 获取某个交易的详细信息
    def get_transaction_details(tx_signature):
        tx_data = client.get_transaction(tx_signature, encoding="jsonParsed")
        return tx_data['result']


    # 分析交易中地址关系
    def analyze_transaction(tx_signature):
        tx = get_transaction_details(tx_signature)
        message = tx['transaction']['message']

        print("Account Keys Involved:")
        for account in message['accountKeys']:
            print(f"- {account}")

        print("\nInstructions:")
        for instr in message['instructions']:
            program_id = instr['programId']
            accounts = instr['accounts']
            print(f"Program ID: {program_id}")
            print(f"Related Accounts: {accounts}")


    # 示例交易签名
    analyze_transaction(tx_signature)
