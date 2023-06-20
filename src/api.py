from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ccxt import binance,okex5,binanceusdm,bitget,bybit
from datetime import datetime,date,timedelta
from hashlib import md5
import pymongo
import uvicorn
import argparse

#constants
ALLOWED_FIELDS = ['user_name', 'user_email', 'user_password', 'user_detail']

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--mongo', type=str, default='mongodb://localhost:27017/', help='MongoDB connection string')
parser.add_argument('--user_name', type=str, default='admin', help='APP user name')
parser.add_argument('--password', type=str, default='admin', help='APP password')
parser.add_argument('--user_email', type=str,default="", help='APP user email')
parser.add_argument('--broker', type=str, default='080c0d187dcaSUDE', help='Broker ID')

args = parser.parse_args()

# 记录失败的订单
def record_failed_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["orders"]
    rec_data = {
        "owner": order["username"],#primary key
        "id": md5((order["username"] + order["time"]).encode()).hexdigest(),
        "time": order["time"], 
        "status": "failed",
        "detail": {
            "symbol": order["symbol"],
            "side": order["side"],
            "type": order["type"],
            "quantity": order["quantity"],
            "price": order["price"],
            "leverage": order["leverage"],
            "class": order["class_SF"],
            "note": order["note"]
        }
    }
    res = mycol.insert_one(rec_data)
    print(f"订单 {res.inserted_id} 已记录。")
    myclient.close()
    return res.inserted_id

# 记录订单
def record_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["orders"]
    rec_data = {
        "owner": order["username"],#primary key
        "id": md5((order["username"] + order["time"]).encode()).hexdigest(),
        "time": order["time"], 
        "status": "success",
        "detail": {
            "symbol": order["symbol"],
            "side": order["side"],
            "type": order["type"],
            "quantity": order["quantity"],
            "price": order["price"],
            "leverage": order["leverage"],
            "class": order["class_SF"],
            "note": order["note"]
        }
    }
    res = mycol.insert_one(rec_data)
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

def createUser(username: str, email: str, password: str, userid: str):
    '''
    在資料庫中創建一個新的用戶。

    參數:
        username (str): 用戶名
        email (str): 用戶的電子郵件
        password (str): 用戶的密碼
        userid (str): 用戶的ID
    '''
    try:
        # 創建並編碼JWT令牌
        token, expiry_time = generate_Token(username)

        # 創建用戶詳細信息字典
        user_details = {
            'token': token,
            'expire_date': expiry_time
        }

        # 創建用戶字典
        user = {
            'user_id': userid,
            'user_name': username,
            'user_email': email,
            'user_password': password,
            'user_detail': user_details
        }

        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["users"]

            # 檢查用戶名，電子郵件和用戶 ID 是否已經存在於數據庫中
            if mycol.find_one({'user_name': username}):
                print(f"用戶名 {username} 已存在。")
                return False
            if mycol.find_one({'user_email': email}):
                print(f"電子郵件 {email} 已存在。")
                return False
            if mycol.find_one({'user_id': userid}):
                print(f"用戶 ID {userid} 已存在。")
                return False

            # 插入用戶資訊到資料庫
            mycol.insert_one(user)

        print(f"用戶 {username} 的記錄已成功創建。")
        return True
    except Exception as e:
        print("在嘗試創建用戶記錄時發生錯誤：")
        print(e)
        return False

def getUser(user_name: str, mongo_connection_string: str):
    '''
    從數據庫中獲取用戶記錄。

    參數:
        user_name (str): 用戶名。
        mongo_connection_string (str): MongoDB連接字符串。
    '''
    try:
        with pymongo.MongoClient(mongo_connection_string) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["users"]
            data = mycol.find_one({'user_name': user_name})

        if data is not None:
            print(f"成功獲取到 {user_name} 的記錄。")
        else:
            print(f"未找到 {user_name} 的記錄。")
            
        return data
    except Exception as e:
        print("在嘗試獲取用戶記錄時發生錯誤：")
        print(e)
        return None

def updateUser(username:str, user:dict):
    '''
    將用戶信息記錄到數據庫。

    參數:
        username (str): 用戶名
        user (dict): 用戶信息字典，預期包含允許的字段鍵。

    DB中的用戶信息字典包含以下字段鍵：
        - user_name (str): 用戶名
        - user_email (str): 用戶的電子郵件
        - user_password (str): 用戶的密碼
        - user_detail (dict): 用戶詳細信息字典，包含以下字段鍵：
            - token (str): JWT令牌
            - expire_date (str): JWT令牌的到期日期
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["users"]
            
            temp = mycol.find_one({'user_name': username})
            if not temp:
                print(f"找不到用戶名為 {username} 的用戶。")
                return False
            
            update_data = {field: user.get(field) for field in ALLOWED_FIELDS if field in user}
            mycol.update_one({'user_name': username}, {'$set': update_data}, upsert=True)
            
        print(f"用戶 {username} 的記錄已成功更新。")
        return True
    except Exception as e:
        print("在嘗試更新用戶記錄時發生錯誤：")
        print(e)
        return False
    
def deleteUser(username: str):
    '''
    從數據庫中刪除用戶記錄。

    參數:
        username (str): 用戶名。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["users"]

            # Check if user exists
            if mycol.count_documents({'user_name': username}) == 0:
                print(f"未找到 {username} 的記錄，因此無法刪除。")
                return False

            mycol.delete_one({'user_name': username})

        print(f"用戶 {username} 的記錄已成功刪除。")
        return True
    except Exception as e:
        print("在嘗試刪除用戶記錄時發生錯誤：")
        print(e)
        return False

# 生成令牌
def generate_Token(user_name: str)->dict:
    '''
    根據用戶名和當前日期時間生成MD5令牌。

    參數:
        user_name (str): 用戶名。

    返回:
        token_expire_info (dict): 包含生成的MD5令牌和到期日期的字典。
    '''
    try:
        # Generate token using MD5 hashing
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Token = md5((user_name + date).encode()).hexdigest()

        # Set token expiry date to 5 days from now
        expire_date = datetime.now() + timedelta(days=5)

        token_expire_info = {
            'Token': Token,
            'Expire_Date': expire_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        return token_expire_info
    except Exception as e:
        print("在嘗試生成令牌時發生錯誤：")
        print(e)
        return {'Token': None, 'Expire_Date': None}

def token_2_user_name(Token:str):
    '''
    根据令牌获取用户名。

    参数:
        Token (str): 令牌。

    返回:
        user_name (str): 用户名。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["users"]
            data = mycol.find_one({'user_detail.token': Token})

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
            if datetime.strptime(result['user_detail']['expire_date'], "%Y-%m-%d %H:%M:%S") > datetime.now():
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
    token: str
    api_key: str
    secret_key: str

class okex5_api_setting(BaseModel):
    token: str
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
    data = getUser(user.user_name, args.mongo)
    if data is None:
        return {'status': 'error', 'error': 'user not found'}
    elif data['password'] != user.password:
        return {'status': 'error', 'error': 'password error'}
    else:
        Token,expire_date = generate_Token(user.user_name)
        update_dict = {
            "user_detail": {
                "Token": Token,
                "expire_date": expire_date
            }
        }
        updateUser(username=user.user_name, user=update_dict)
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

@app.post("/exchange/test")#this using for demo
async def test_order(order: Order):
    record_order(order.dict())

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
    side = 'buy' if order.side == 'buy' else 'sell'
    if order.type == 'market':
        result = okex5_ex.create_order(
            order.symbol,
            'market',
            side,
            order.quantity,
            None,
            params={
                "tag": args.broker
            }
        )
    elif order.type == 'limit':
        result = okex5_ex.create_order(
            order.symbol,
            'limit',
            side,
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
        "user_id": args.user_name,
        "user_name": args.user_name,
        "user_password": args.password,
        "user_email": args.email,
        "user_detail": {
            "token": token,
            "expire_date": expire_date
        }
    })

    # Orders
    orders_col = my_db['orders']
    orders_col.create_index('order_id', unique=True)

    # Profile
    profile_col = my_db['profile']
    profile_col.create_index('user_id', unique=True)

    # Account (API Settings)
    account_col = my_db['account']
    account_col.create_index('user_id', unique=True)

    # Logs
    logs_col = my_db['logs']
    logs_col.create_index('log_id', unique=True)

    # Trade
    trade_col = my_db['trade']
    trade_col.create_index('trade_id', unique=True)

    # Assets
    assets_col = my_db['assets']
    assets_col.create_index('user_id', unique=True)

    # 啟動API
    uvicorn.run(app, host="0.0.0.0",port=80)
