import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from kafka import KafkaConsumer
from src.utils.database_helper import *
import json

from src.utils.tg_helper import send_tg_msg


consumer = KafkaConsumer(WEBHOOK_TOPIC,
                         bootstrap_servers=BOOTSTRAP_SERVER,
                         group_id=CONSUMER_GROUP)


def commit_txn(txn_list):
    with Session() as sess:
        sess.add_all(txn_list)
        sess.commit()


if __name__ == '__main__':
    token_set = get_all_tokens_set()
    print(f'tokens in databases: {token_set}')
    print(consumer)
    print(consumer.subscription())
    print(consumer.bootstrap_connected())
    print(consumer.partitions_for_topic("wallet-monitor-webhook"))
    print(consumer.topics())
    txn_count = 0
    txns = []
    for msg in consumer:

        data = json.loads(msg.value.decode("utf-8"))[0]
        description = data['description']
        timestamp = data['timestamp']
        fee = data['fee']
        fee_payer = data['feePayer']
        txn_type = data['type']
        signature = data['signature']
        wallet_address = fee_payer
        swap_event = data['events']['swap']
        token_inputs = swap_event['tokenInputs']    # 对于swap, input是卖出, output是买入
        token_outputs = swap_event['tokenOutputs']
        token_fees = swap_event['tokenFees']
        native_input = swap_event['nativeInput']
        native_output = swap_event['nativeOutput']
        native_fees = swap_event['nativeFees']
        # break
        wallet_txn = WalletTransaction(
            signature=signature, wallet_address=wallet_address, description=description,
            txn_type=txn_type, timestamp=timestamp, fee=fee, fee_payer=fee_payer,
            token_fees=token_fees, token_inputs=token_inputs, token_outputs=token_outputs,
            native_fees=native_fees, native_input=native_input, native_output=native_output
        )
        txns.append(wallet_txn)

        # 只处理不在token列表内部的新token

        is_about_new_token = False
        # 卖出token
        if token_inputs is not None and len(token_inputs) > 0:
            token_input = token_inputs[0]
            token = token_input['mint']
            if token_set.__contains__(token):
                continue
            is_about_new_token = True
        # 买入token
        if token_outputs is not None and len(token_outputs) > 0:
            token_output = token_outputs[0]
            token = token_output['mint']
            if token_set.__contains__(token):
                continue
            is_about_new_token = True

        if is_about_new_token:
            # TODO send in a queue
            send_tg_msg(description)

        txn_count += 1
        if txn_count % 200 == 0:
            commit_txn(txns)
            txn_count = 0
            txns = []
    # print(consumer.next_v1())