from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ccxt import binance,okex5,binanceusdm,bitget,bybit
from datetime import datetime,date,timedelta
from hashlib import md5
import pymongo
import uvicorn
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--mongo', type=str, default='mongodb://localhost:27017/', help='MongoDB connection string')
parser.add_argument('--user_name', type=str, default='admin', help='APP user name')
parser.add_argument('--password', type=str, default='admin', help='APP password')
parser.add_argument('--broker', type=str, default='080c0d187dcaSUDE', help='Broker ID')

args = parser.parse_args()

# 记录失败的订单
def record_failed_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["failed_orders"]
    res = mycol.insert_one(order)
    print(f"订单 {res.inserted_id} 已记录。")
    myclient.close()
    return res.inserted_id

# 记录订单
def record_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["orders"]
    res = mycol.insert_one(order)
    print(f"订单 {res.inserted_id} 已记录。")
    myclient.close()
    return res.inserted_id

#更新profile
def update_profile(user_name:str,update_data:dict):
    '''
    更新用户的profile。
    
    参数:
        user_name (str): 用户名。
        update_data (dict): 更新的数据。
            - profit_history (float): 收益历史记录。
            - balance (float): 余额。
            - open_orders_num (int): 持仓数量。
            - win_or_lose (int): 勝負。(1:win,0:lose)

    '''
    try:
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["profiles"]
        q_data = mycol.find_one({'user_name': user_name})
        if q_data is not None:
            profit_history = q_data['profit_history']
            profit_history.append(update_data['profit_history'])
            balance = q_data['balance']
            balance.append(update_data['balance'])
            open_orders_num = q_data['open_orders_num']
            open_orders_num.append(update_data['open_orders_num'])
            win_or_lose = q_data['win_or_lose']
            win_or_lose.append(update_data['win_or_lose'])
            if update_data['win_or_lose']:
                win_num = q_data['win_num']
                win_num += 1
            else:
                lose_num = q_data['lose_num']
                lose_num += 1

        #not complete
    except Exception as e:
        print("在尝试更新用户记录时发生错误：")
        print(e)

# 用户记录
def user_record(user):
    '''
    将用户信息记录到数据库。

    参数:
        user (dict): 用户信息字典，预期包含'user_name'键。
    '''
    try:
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        mycol.update_one({'user_name': user['user_name']}, {'$set': user}, upsert=True)
        print(f"用户 {user['user_name']} 的记录已成功更新。")
    except Exception as e:
        print("在尝试更新用户记录时发生错误：")
        print(e)

# 获取用户记录
def get_user_record(user_name:str, mongo_connection_string:str):
    '''
    从数据库中获取用户记录。

    参数:
        user_name (str): 用户名。
        mongo_connection_string (str): MongoDB连接字符串。
    '''
    try:
        myclient = pymongo.MongoClient(mongo_connection_string)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        data = mycol.find_one({'user_name': user_name})
        myclient.close()
        if data is not None:
            print(f"成功获取到 {user_name} 的记录。")
        else:
            print(f"未找到 {user_name} 的记录。")
        return data
    except Exception as e:
        print("在尝试获取用户记录时发生错误：")
        print(e)

# 生成令牌
def generate_Token(user_name:str):
    '''
    根据用户名和当前日期时间生成MD5令牌。

    参数:
        user_name (str): 用户名。

    返回:
        Token (str): 生成的MD5令牌。
        expire_date (str): 令牌的到期日期（从当前时间开始计算的5天后）。
    '''
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Token = md5((user_name + date).encode()).hexdigest()
    expire_date = datetime.now() + timedelta(days=5)
    return (Token, expire_date.strftime("%Y-%m-%d %H:%M:%S"))

def token_2_user_name(Token:str):
    '''
    根据令牌获取用户名。

    参数:
        Token (str): 令牌。

    返回:
        user_name (str): 用户名。
    '''
    try:
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        data = mycol.find_one({'Token': Token})
        myclient.close()
        if data is not None:
            print(f"成功取得 {Token} 的紀錄。")
            return data['user_name']
        else:
            print(f"未找到 {Token} 的紀錄。")
            return None
    except Exception as e:
        print("在嘗試獲取用户資料時發生錯誤：")
        print(e)

def check_token(Token:str):
    '''
    检查令牌是否有效。
    
    参数:
        Token (str): 令牌。
        
    返回:
        bool: 令牌是否有效。
    '''
    try:
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        result = mycol.find_one({'Token': Token})
        myclient.close()
        if result is not None:
            if datetime.strptime(result['expire_date'], "%Y-%m-%d %H:%M:%S") > datetime.now():
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print("在嘗試檢查令牌時發生錯誤：")
        print(e)

# 定义数据模型
class Order(BaseModel):
    username: str # 下单用户的用户名，用于查询api_key和secret_key
    symbol: str # 购买的币种符号
    exchange: str # 购买币种的交易所
    side: str # 买入或卖出  
    type: str # 市价或限价
    quantity: float # 购买的币种数量
    leverage: Optional[int] = None # 购买币种的杠杆
    price: Optional[float] = None # 购买币种的价格
    class_SF: Optional[str] = None # 现货或期货
    webhook: Optional[str] = None # 发送订单状态的webhook
    note: Optional[str] = None # 订单备注

class Fast_Order(BaseModel):
    api_key: str # 下单用户的api_key
    secret_key: str # 下单用户的secret_key
    phrase: Optional[str] = None # 下单用户的phrase
    symbol: str # 购买的币种符号
    exchange: str # 购买币种的交易所
    side: str # 买入或卖出  
    type: str # 市价或限价
    quantity: float # 购买的币种数量
    leverage: Optional[int] = None # 购买币种的杠杆
    price: Optional[float] = None # 购买币种的价格
    class_SF: Optional[str] = None # 现货或期货
    webhook: Optional[str] = None # 发送订单状态的webhook
    note: Optional[str] = None # 订单备注

class front_Query(BaseModel):
    token: str # 用户令牌
    symbol: Optional[str] = None
    date: Optional[str] = None # 购买的币种日期，格式：YYYY-MM-DD
    side: Optional[str] = None # 买入或卖出

class User(BaseModel):
    user_name: str
    password: str

class binance_api_setting(BaseModel):
    user_name: str
    api_key: str
    secret_key: str

class okex5_api_setting(BaseModel):
    user_name: str
    api_key: str
    secret_key: str
    passphrase: str

# 创建FastAPI应用实例
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(user: User):
    if user.user_name == args.user_name and user.password == args.password:
        Token,expire_date = generate_Token(user.user_name)
        user_record({'user_name': user.user_name, 'Token': Token, 'expire_date': expire_date})
        return {'Token': Token, 'expire_date': expire_date, 'status': 'success'}
    else:
        data = get_user_record(user.user_name)
        if data is None:
            return {'status': 'error', 'error': 'user not found'}
        elif data['password'] != user.password:
            return {'status': 'error', 'error': 'password error'}
        else:
            Token,expire_date = generate_Token(user.user_name)
            user_record({'user_name': user.user_name, 'Token': Token, 'expire_date': expire_date})
            return {'Token': Token, 'expire_date': expire_date, 'status': 'success'}
    
@app.get("/query/profile")
async def query_profile(token: str):
    if check_token(token):
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        user_name = mycol.find_one({'Token': token})['user_name']
        mycol = mydb["profiles"]
        profile_data = mycol.find_one({'user_name': user_name})
        myclient.close()
        return profile_data
    else:return {'status': 'error', 'error': 'token error'}

@app.post("/exchange/binance")#it should be place spot order
async def binance_order(order: Order):
    db_client = pymongo.MongoClient(args.mongo)
    db = db_client["tradingview_to_exchange"]
    col = db["api_setting"]
    data = col.find_one({'user_name': order.username , 'exchange': order.exchange})
    api_key,api_sec = data['api_key'],data['secret_key']
    db_client.close()
    binance_ex = binance({
        'apiKey': api_key,
        'secret': api_sec,
        'options': {
            'defaultType': order.class_SF,
        },
        'timeout': 30000,
    })
    if order.type == 'market':
        if order.side == 'buy':
            result = binance_ex.create_market_buy_order(order.symbol,order.quantity)
        elif order.side == 'sell':
            result = binance_ex.create_market_sell_order(order.symbol,order.quantity)
    elif order.type == 'limit':
        if order.side == 'buy':
            result = binance_ex.create_limit_buy_order(order.symbol,order.quantity,order.price)
        elif order.side == 'sell':
            result = binance_ex.create_limit_sell_order(order.symbol,order.quantity,order.price)
    if result['info']['status'] == 'FILLED':#need to change error status
        record_failed_order(order)
        return {'status': 'success', 'order_id': result['id']}
    else:
        record_order(order)
        return {'status': 'error', 'error': result['info']['status']}
    
@app.post("/exchange/okex5")
async def okex5_order(order: Order):
    db_client = pymongo.MongoClient(args.mongo)
    db = db_client["tradingview_to_exchange"]
    col = db["api_setting"]
    data = col.find_one({'user_name': order.username , 'exchange': order.exchange})
    api_key,api_sec,passphrase = data['api_key'],data['secret_key'],data['passphrase']
    db_client.close()
    okex5_ex = okex5({
        'apiKey': api_key,
        'secret': api_sec,
        'password': passphrase,
        'timeout': 30000,
        'options': {
            'defaultType': order.class_SF,
        },
    })
    if order.type == 'market':
        result = okex5_ex.create_order(
            order.symbol,
            order.type,
            order.side,
            order.quantity,
            None,
            params={
                "tag": args.broker
            }
        )
    elif order.type == 'limit':
        result = okex5_ex.create_order(
            order.symbol,
            order.type,
            order.side,
            order.quantity,
            order.price,
            params={
                "tag": args.broker#broker code
            }
        )
    return result

if __name__ == "__main__":
    # 設定資料庫
    my_client = pymongo.MongoClient(args.mongo)
    my_db = my_client["tradingview_to_exchange"]
    my_col = my_db["users"]
    my_col.create_index("user_name", unique=True)
    token,expire_date = generate_Token(args.user_name)
    my_col.insert_one({
        "user_name": args.user_name,
        "password": args.password,
        "Token": token,
        "expire_date": expire_date,
    })
    my_col = my_db["orders"]
    my_col.create_index("order_id", unique=True)
    my_col = my_db["failed_orders"]
    my_col.create_index("order_id", unique=True)
    my_col = my_db["profiles"]
    my_col.create_index("user_name", unique=True)
    my_col = my_db["api_setting"]
    my_col.create_index("user_name", unique=True)
    # 啟動API
    uvicorn.run(app, host="0.0.0.0",port=80)
