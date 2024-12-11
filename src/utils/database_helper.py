import datetime
import json

from tqdm import tqdm

from config import *
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Double, Date, TIMESTAMP, Boolean, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sol_pnl.src.utils.config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD

# Do not expose your Neon credentials to the browser

# 数据库连接参数
db_config = {
    'dbname': PGDATABASE,
    'user': PGUSER,
    'password': PGPASSWORD,
    'host': PGHOST,
    'port': 5432
}

# 数据库连接配置
DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:5432/{PGDATABASE}"


# 定义基类
Base = declarative_base()


class WalletTransaction(Base):
    __tablename__ = 'wallet_txn_events'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    signature = Column(String(128), nullable=False)
    wallet_address = Column(String(128), nullable=False)
    txn_type = Column(String(32))
    timestamp = Column(BigInteger)
    fee = Column(Double)
    fee_payer = Column(String(128))
    token_fees = Column(JSON)
    token_inputs = Column(JSON)
    token_outputs = Column(JSON)
    native_fees = Column(JSON)
    native_input = Column(JSON)
    native_output = Column(JSON)


# 定义模型类（映射数据库表）
class WalletPnL(Base):
    __tablename__ = 'wallet_pnl'  # 数据库中的表名
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(1024), nullable=False)
    name = Column(String(256))
    total_profit = Column(Double)
    total_profit_pnl = Column(Double)
    unrealized_profit = Column(Double)
    unrealized_pnl = Column(Double)
    realized_profit = Column(Double)
    realized_profit_7d = Column(Double)
    realized_profit_30d = Column(Double)
    all_pnl = Column(Double)
    pnl_7d = Column(Double)
    pnl_30d = Column(Double)
    winrate = Column(Double)
    sol_balance = Column(Double)
    token_num = Column(Integer)
    buy_30d = Column(BigInteger)
    sell_30d = Column(BigInteger)
    buy_7d = Column(BigInteger)
    sell_7d = Column(BigInteger)
    update_date = Column(Date)
    tags = Column(String(1024))


class WalletTopProfit(Base):
    __tablename__ = 'wallet_top_profits'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(1024), nullable=False)
    name = Column(String(256))
    total_profit = Column(Double)
    total_profit_pnl = Column(Double)
    unrealized_profit = Column(Double)
    unrealized_pnl = Column(Double)
    realized_profit = Column(Double)
    realized_profit_7d = Column(Double)
    realized_profit_30d = Column(Double)
    all_pnl = Column(Double)
    pnl_7d = Column(Double)
    pnl_30d = Column(Double)
    winrate = Column(Double)
    sol_balance = Column(Double)
    token_num = Column(Integer)
    buy_30d = Column(BigInteger)
    sell_30d = Column(BigInteger)
    buy_7d = Column(BigInteger)
    sell_7d = Column(BigInteger)
    update_date = Column(Date)
    tags = Column(String(1024))
    first_degree = Column(JSON)


class WalletTopUnrealizedProfit(Base):
    __tablename__ = 'wallet_top_unrealized_profits'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(1024), nullable=False)
    name = Column(String(256))
    total_profit = Column(Double)
    total_profit_pnl = Column(Double)
    unrealized_profit = Column(Double)
    unrealized_pnl = Column(Double)
    realized_profit = Column(Double)
    realized_profit_7d = Column(Double)
    realized_profit_30d = Column(Double)
    all_pnl = Column(Double)
    pnl_7d = Column(Double)
    pnl_30d = Column(Double)
    winrate = Column(Double)
    sol_balance = Column(Double)
    token_num = Column(Integer)
    buy_30d = Column(BigInteger)
    sell_30d = Column(BigInteger)
    buy_7d = Column(BigInteger)
    sell_7d = Column(BigInteger)
    update_date = Column(Date)
    tags = Column(String(1024))
    first_degree = Column(JSON)


class AccountInfo(Base):
    __tablename__ = 'account_info'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(60), nullable=False)
    owner = Column(String(60))
    is_owner_system_program = Column(Boolean)
    is_on_curve = Column(Boolean)
    executable = Column(Boolean)
    is_bot_txs = Column(Boolean)
    is_blocked = Column(Boolean)


class Holder(Base):
    __tablename__ = 'holders'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(60), nullable=False)
    token_address = Column(String(60))
    parent_wallet_address = Column(String(60))  # first degree
    updated_transfer_signature = Column(String(100))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    recent_tx_at = Column(TIMESTAMP)
    in_degree = Column(Integer)
    token_count = Column(Integer)
    blocked_at = Column(TIMESTAMP)
    first_degree_updated_at = Column(TIMESTAMP)
    owner = Column(String(60))
    is_owner_system_program = Column(Boolean)
    is_on_curve = Column(Boolean)
    executable = Column(Boolean)


class FirstDegree(Base):
    __tablename__ = "first_degree"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    wallet_address = Column(String(60), nullable=False)
    first_degree_address = Column(String(60))


class TokenHolder(Base):
    __tablename__ = 'token_holders'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date)
    token_address = Column(String(60))
    holder_address = Column(String(60))
    balance = Column(BigInteger)
    percentage_held = Column(Double)


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def get_date_before(date_str: str) -> str:
    cur_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return cur_date.__sub__(datetime.timedelta(days=1)).strftime('%Y-%m-%d')


def get_blocked_wallet_addresses():
    all_addresses = session.query(AccountInfo).where(AccountInfo.is_blocked.__eq__(True)).all()
    blocked_addresses = set()
    for addr in all_addresses:
        blocked_addresses.add(addr.wallet_address)
    return blocked_addresses


def get_all_wallet_addresses(date_str: str):
    try:
        wallet_list_path = get_wallet_list_path(date_str, is_monitor_list=False)
        if os.path.exists(wallet_list_path):
            print(f'wallet list path[{wallet_list_path}] already exist, just return')
            return open(wallet_list_path, 'r').readlines()

        one_day_before = get_date_before(date_str)
        all_holders = session.query(Holder.wallet_address).distinct().all()
        blocked_addresses = get_blocked_wallet_addresses()
        valid_wallet_addresses = list()
        for holder in all_holders:
            if blocked_addresses.__contains__(holder.wallet_address): continue
            valid_wallet_addresses.append(holder.wallet_address)

        with open(wallet_list_path, 'w') as file:
            for addr in valid_wallet_addresses:
                file.write(addr + '\n')
        return open(wallet_list_path, 'r').readlines()
    except Exception as e:
        print(f'get all wallet addresses error', e)


def write_wallet_pnl_to_postgresql(date_str: str, is_monitor_list: bool):
    session = Session()
    raw_data_file_path = get_raw_data_file_path(date_str, is_monitor_list=is_monitor_list)
    raw_data = open(raw_data_file_path, 'r').readlines()

    '''
    'wallet',
     'total_profit', 'total_profit_pnl',
     'unrealized_profit', 'unrealized_pnl',
     'realized_profit', 'realized_profit_7d', 'realized_profit_30d',
     'all_pnl', 'pnl_7d', 'pnl_30d',
     'winrate',
     'sol_balance',
     'token_num', # realized_profit_7d / token_num 为7天平均每token盈利
     'buy_30d', 'sell_30d', 'buy_7d', 'sell_7d',
     'updated_at', # date
     'refresh_requested_at',
    '''

    try:
        batch_count = 0
        for line in raw_data:
            data = json.loads(line)
            wallet_address = data['wallet']
            total_profit = data['total_profit']
            total_profit_pnl = data['total_profit_pnl']
            unrealized_profit = data['unrealized_profit']
            unrealized_pnl = data['unrealized_pnl']
            realized_profit = data['realized_profit']
            realized_profit_7d = data['realized_profit_7d']
            realized_profit_30d = data['realized_profit_30d']
            all_pnl = data['all_pnl']
            pnl_7d = data['pnl_7d']
            pnl_30d = data['pnl_30d']
            winrate = data['winrate']
            sol_balance = data['sol_balance']
            token_num = data['token_num']
            name = data['name'] if 'name' in data.keys() else None
            buy_30d = data['buy_30d'] if 'buy_30d' in data.keys() else None
            sell_30d = data['sell_30d'] if 'sell_30d' in data.keys() else None
            buy_7d = data['buy_7d'] if 'buy_7d' in data.keys() else None
            sell_7d = data['sell_7d'] if 'sell_7d' in data.keys() else None
            tags = ','.join(data['tags']) if 'tags' in data.keys() else ''

            wallet_pnl_info = WalletPnL(
                wallet_address=wallet_address, name=name,
                total_profit=total_profit, total_profit_pnl=total_profit_pnl,
                unrealized_profit=unrealized_profit, unrealized_pnl=unrealized_pnl,
                realized_profit=realized_profit, realized_profit_7d=realized_profit_7d, realized_profit_30d=realized_profit_30d,
                all_pnl=all_pnl, pnl_7d=pnl_7d, pnl_30d=pnl_30d,
                winrate=winrate,
                sol_balance=sol_balance,
                token_num=token_num,
                buy_30d=buy_30d, sell_30d=sell_30d, buy_7d=buy_7d, sell_7d=sell_7d,
                update_date=date_str, tags=tags
            )
            session.add(wallet_pnl_info)  # 将对象加入会话

            batch_count += 1
            if batch_count == 1000:
                session.commit()  # 提交事务
                batch_count = 0

        if batch_count != 0:
            session.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pass


def get_all_wallet_first_degrees():
    session = Session()
    first_degrees = session.query(FirstDegree).all()
    first_degree_map = {}
    for degree_pair in first_degrees:
        if degree_pair.wallet_address is None:
            continue
        if degree_pair.wallet_address not in first_degree_map.keys():
            first_degree_map[degree_pair.wallet_address] = set()
        first_degree_map[degree_pair.wallet_address].add(degree_pair.first_degree_address)
    return first_degree_map


def get_monitor_wallet_addresses(date_str: str):
    try:
        wallet_list_path = get_wallet_list_path(date_str, is_monitor_list=True)
        if os.path.exists(wallet_list_path):
            print(f'wallet list path[{wallet_list_path}] already exist, just return')
            return open(wallet_list_path, 'r').readlines()

        stmt = text("""
        select 
          a.wallet_address
          ,a.token_count
          ,d.token_count as parent_token_count
        from holders a 
          join account_info b on a.wallet_address=b.wallet_address
          left join holders d on a.parent_wallet_address=d.wallet_address
        where (b.is_blocked=false OR b.is_blocked IS NULL)
          and (a.token_count > 2 or d.token_count > 2)
        order by a.token_count desc
        """)
        result = session.execute(stmt).all()
        refined_addresses = []
        with open(wallet_list_path, 'w') as file:
            for row in result:
                refined_addresses.append(row.wallet_address)
                file.write(row.wallet_address + '\n')
        return refined_addresses
    except Exception as e:
        print("get monitor wallet addresses error", e)


top_profit_threshold = 100000
top_unrealized_profit_threshold = 100000
def write_top_profit_wallet_pnl_to_postgresql(date_str: str, realized: bool, holders_map: dict, is_monitor_list: bool):
    raw_data_file_path = get_raw_data_file_path(date_str, is_monitor_list=is_monitor_list)
    raw_data = open(raw_data_file_path, 'r').readlines()

    '''
    'wallet',
     'total_profit', 'total_profit_pnl',
     'unrealized_profit', 'unrealized_pnl',
     'realized_profit', 'realized_profit_7d', 'realized_profit_30d',
     'all_pnl', 'pnl_7d', 'pnl_30d',
     'winrate',
     'sol_balance',
     'token_num', # realized_profit_7d / token_num 为7天平均每token盈利
     'buy_30d', 'sell_30d', 'buy_7d', 'sell_7d',
     'updated_at', # date
     'refresh_requested_at',
    '''

    session = Session()

    try:
        batch_count = 0
        for line in tqdm(raw_data):
            data = json.loads(line)
            wallet_address = data['wallet']
            total_profit = data['total_profit']
            total_profit_pnl = data['total_profit_pnl']
            unrealized_profit = data['unrealized_profit']
            unrealized_pnl = data['unrealized_pnl']
            realized_profit = data['realized_profit']
            realized_profit_7d = data['realized_profit_7d']
            realized_profit_30d = data['realized_profit_30d']
            all_pnl = data['all_pnl']
            pnl_7d = data['pnl_7d']
            pnl_30d = data['pnl_30d']
            winrate = data['winrate']
            sol_balance = data['sol_balance']
            token_num = data['token_num']
            name = data['name'] if 'name' in data.keys() else None
            buy_30d = data['buy_30d'] if 'buy_30d' in data.keys() else None
            sell_30d = data['sell_30d'] if 'sell_30d' in data.keys() else None
            buy_7d = data['buy_7d'] if 'buy_7d' in data.keys() else None
            sell_7d = data['sell_7d'] if 'sell_7d' in data.keys() else None
            tags = ','.join(data['tags']) if 'tags' in data.keys() else ''
            first_degrees = list(holders_map.get(wallet_address)) if wallet_address in holders_map.keys() else None

            if realized:
                if total_profit is None:
                    continue
                if total_profit < top_profit_threshold:
                    continue
                wallet_top_pnl_info = WalletTopProfit(
                    wallet_address=wallet_address, name=name,
                    total_profit=total_profit, total_profit_pnl=total_profit_pnl,
                    unrealized_profit=unrealized_profit, unrealized_pnl=unrealized_pnl,
                    realized_profit=realized_profit, realized_profit_7d=realized_profit_7d,
                    realized_profit_30d=realized_profit_30d,
                    all_pnl=all_pnl, pnl_7d=pnl_7d, pnl_30d=pnl_30d,
                    winrate=winrate,
                    sol_balance=sol_balance,
                    token_num=token_num,
                    buy_30d=buy_30d, sell_30d=sell_30d, buy_7d=buy_7d, sell_7d=sell_7d,
                    update_date=date_str, tags=tags,
                    first_degree=first_degrees
                )
            else:
                if unrealized_profit is None:
                    continue
                if unrealized_profit < top_unrealized_profit_threshold:
                    continue
                wallet_top_pnl_info = WalletTopUnrealizedProfit(
                    wallet_address=wallet_address, name=name,
                    total_profit=total_profit, total_profit_pnl=total_profit_pnl,
                    unrealized_profit=unrealized_profit, unrealized_pnl=unrealized_pnl,
                    realized_profit=realized_profit, realized_profit_7d=realized_profit_7d,
                    realized_profit_30d=realized_profit_30d,
                    all_pnl=all_pnl, pnl_7d=pnl_7d, pnl_30d=pnl_30d,
                    winrate=winrate,
                    sol_balance=sol_balance,
                    token_num=token_num,
                    buy_30d=buy_30d, sell_30d=sell_30d, buy_7d=buy_7d, sell_7d=sell_7d,
                    update_date=date_str, tags=tags,
                    first_degree=first_degrees
                )

            session.add(wallet_top_pnl_info)  # 将对象加入会话

            batch_count += 1
            if batch_count == 1000:
                session.commit()  # 提交事务
                batch_count = 0

        if batch_count != 0:
            session.commit()

        print(f'delete data of yesterday: ' + get_date_before(date_str))
        if realized:
            stmt = text("delete from " + WalletTopProfit.__tablename__ + " where update_date<='" + get_date_before(date_str) + "'")

        else:
            stmt = text("delete from " + WalletTopUnrealizedProfit.__tablename__ + " where update_date<='" + get_date_before(date_str) + "'")
        print(stmt)
        session.execute(stmt)
        session.commit()


    except Exception as e:
        print(f"Error: {e}")
    finally:
        pass


if __name__ == '__main__':

    refine_list_3 = get_monitor_wallet_addresses()
    exit()

    # print(f'{get_date_before("2024-12-15")}')
    wallet_addresses = get_wallet_addresses('2024-12-19')
    exit()
    # print(f'wallet_addresses count {len(wallet_addresses)}')
    # write_all_wallet_pnl_to_postgresql('2024-12-17')
    holders_map = get_all_wallet_first_degrees()
    print(holders_map)
    write_top_profit_wallet_pnl_to_postgresql('2024-12-17', realized=True, holders_map=holders_map)
    write_top_profit_wallet_pnl_to_postgresql('2024-12-17', realized=False, holders_map=holders_map)

