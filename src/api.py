from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ccxt import binance,okex5
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
    mycol.insert_one(order)

# 记录订单
def record_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["orders"]
    mycol.insert_one(order)

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
        if data is not None:
            print(f"成功取得 {Token} 的紀錄。")
            return data['user_name']
        else:
            print(f"未找到 {Token} 的紀錄。")
            return None
    except Exception as e:
        print("在嘗試獲取用户資料時發生錯誤：")
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
    # 啟動API
    uvicorn.run(app, host="0.0.0.0",port=80)
