from kafka import KafkaConsumer
from sol_pnl.src.utils.database_helper import *
import json

consumer = KafkaConsumer("wallet-monitor-webhook",
                         bootstrap_servers="localhost:9092",
                         group_id="txn-consumer-01")

if __name__ == '__main__':
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
        token_inputs = swap_event['tokenInputs']
        token_outputs = swap_event['tokenOutputs']
        token_fees = swap_event['tokenFees']
        native_input = swap_event['nativeInput']
        native_output = swap_event['nativeOutput']
        native_fees = swap_event['nativeFees']
        # break
        wallet_txn = WalletTransaction(
            signature=signature, wallet_address=wallet_address,
            txn_type=txn_type, timestamp=timestamp, fee=fee, fee_payer=fee_payer,
            token_fees=token_fees, token_inputs=token_inputs, token_outputs=token_outputs,
            native_fees=native_fees, native_input=native_input, native_output=native_output
        )
        txns.append(wallet_txn)
        txn_count += 1
        if txn_count % 20 == 0:
            session = Session()
            session.add_all(txns)
            session.commit()
            txn_count = 0
            txns = []
    # print(consumer.next_v1())