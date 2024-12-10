from borsh_construct import CStruct, U8, U64, String
import base64


if __name__ == '__main__':

    # 定义 data 的结构（根据智能合约的逻辑）
    InstructionData = CStruct(
        "method" / U8,           # 方法标识符（1 字节）
        "amount" / U64,          # 64 位无符号整数
        "memo" / String          # 可选的字符串字段
    )

    # 示例 data 字节流
    data = ("3Bxs4HanWsHUZCbH")

    # 解码 data
    # decoded = InstructionData.parse("3Bxs4HanWsHUZCbH")
    # print(f"Method: {decoded.method}, Amount: {decoded.amount}, Memo: {decoded.memo}")

    print(f'decode {base64.b64decode("3Bxs4HanWsHUZCbH")}')
