from fastapi import FastAPI
from fastapi import HTTPException, status
from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import Optional
from ccxt import binance,okex5,binanceusdm,bitget,bybit
from datetime import datetime,date,timedelta
from hashlib import md5
import pymongo
import uvicorn
import argparse

# 定义数据模型
class Order(BaseModel):
    user_id: str # 下單用戶的ID，用於查詢api_key和secret_key
    symbol: str # 購買的幣種符號
    exchange: str # 購買幣種的交易所
    side: str # 買入或賣出  
    type: str # 市價或限價
    quantity: float # 購買的幣種數量
    leverage: Optional[int] = None # 購買幣種的杠桿
    price: Optional[float] = None # 購買幣種的價格
    class_SF: Optional[str] = None # 現貨或期貨
    webhook: Optional[str] = None # 發送訂單狀態的webhook
    note: Optional[str] = None # 訂單備注
    order_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 訂單時間

class Fast_Order(BaseModel):
    api_key: str # 下單用戶的api_key
    secret_key: str # 下單用戶的secret_key
    phrase: Optional[str] = None # 下單用戶的phrase
    symbol: str # 購買的幣種符號
    exchange: str # 購買幣種的交易所
    side: str # 買入或賣出  
    type: str # 市價或限價
    quantity: float # 購買的幣種數量
    leverage: Optional[int] = None # 購買幣種的杠桿
    price: Optional[float] = None # 購買幣種的價格
    class_SF: Optional[str] = None # 現貨或期貨
    webhook: Optional[str] = None # 發送訂單狀態的webhook
    note: Optional[str] = None # 訂單備注
    order_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 訂單時間

class front_Query(BaseModel):
    token: str # 用户令牌
    symbol: Optional[str] = None
    date: Optional[str] = None # 购买的币种日期，格式：YYYY-MM-DD
    side: Optional[str] = None # 买入或卖出

class User(BaseModel):
    user_name: str
    password: str

class RegisterUser(BaseModel):
    id: str
    name: str
    email: str
    password: str

class Api_settings(BaseModel):
    token: str
    api_key: str
    secret_key: str
    phrase: Optional[str] = None
    exchange: str

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

def recordOrder(order: Order, status: str):
    '''
    紀錄訂單。

    參數:
        order (Order): 訂單詳情。
        status (str): 訂單的狀態，可以是 'success' 或 'failed'。
    '''
    with pymongo.MongoClient(args.mongo) as myclient:
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["orders"]
        rec_data = {
            "user_id": order.user_id, 
            "order_id": md5((order.user_id + order.order_time).encode()).hexdigest(), #primary key
            "order_time": order.order_time, 
            "order_status": status,
            "order_detail": order.dict()
        }
        res = mycol.insert_one(rec_data)
        print(f"訂單 {res.inserted_id} 已記錄。")
        return res.inserted_id


def getOrder(order_id: str):
    '''
    獲取特定訂單的詳情。

    參數:
        order_id (str): 訂單的ID。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["orders"]
            data = mycol.find_one({'order_id': order_id})

        if data is not None:
            print(f"成功獲取到 {order_id} 的訂單記錄。")
        else:
            print(f"未找到 {order_id} 的訂單記錄。")
            
        return data
    except Exception as e:
        print("在嘗試獲取訂單記錄時發生錯誤：")
        print(e)
        return None


def getUserOrders(user_id: str):
    '''
    獲取特定用戶的所有訂單。

    參數:
        user_id (str): 用戶的ID。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["orders"]
            data = mycol.find({'user_id': user_id})

        if data is not None:
            print(f"成功獲取到 {user_id} 的所有訂單記錄。")
        else:
            print(f"未找到 {user_id} 的任何訂單記錄。")
            
        return list(data)
    except Exception as e:
        print("在嘗試獲取訂單記錄時發生錯誤：")
        print(e)
        return None


def updateProfile(user_name: str, update_data: dict):
    '''
    更新用戶的profile。

    參數:
        user_name (str): 用戶名。
        update_data (dict): 更新的數據。
            - profit_history (float): 收益歷史記錄。
            - balance (float): 余額。
            - open_orders_num (int): 持倉數量。
            - win_or_lose (int): 勝負。(1:win,0:lose)
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["profiles"]

            win_or_lose = update_data['win_or_lose']
            win_num_inc = 1 if win_or_lose else 0
            lose_num_inc = 1 if not win_or_lose else 0

            update = {
                "$push": {
                    "profile_details.profit_history": update_data['profit_history'],
                    "profile_details.balance": update_data['balance'],
                    "profile_details.open_orders_num": update_data['open_orders_num'],
                },
                "$inc": {
                    "profile_details.win_num": win_num_inc,
                    "profile_details.lose_num": lose_num_inc
                }
            }

            res = mycol.update_one({"user_name": user_name}, update)

            if res.matched_count > 0:
                print(f"用戶 {user_name} 的記錄已更新。")
            else:
                print(f"未找到 {user_name} 的記錄。")
    except Exception as e:
        print("在嘗試更新用戶記錄時發生錯誤：")
        print(e)


def getProfile(user_name:str):
    '''
    获取指定用户的个人资料。

    参数:
        user_name (str): 用户名。

    返回:
        dict: 用户的个人资料，如果找不到该用户则返回 None。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["profiles"]
            profile = mycol.find_one({'user_name': user_name})

            if profile is not None:
                print(f"成功取得用户 {user_name} 的资料。")
            else:
                print(f"未找到用户 {user_name} 的资料。")
                
            return profile

    except Exception as e:
        print("在尝试获取用户资料时发生错误：")
        print(e)
        return None

def createProfile(user_name:str, profile_details:dict):
    '''
    為用戶創建一個個人資料。

    參數:
        user_name (str): 用戶名。
        profile_details (dict): 用戶資料詳細信息。

    返回:
        bool: 成功創建返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["profiles"]
            
            profile_details['user_name'] = user_name
            mycol.insert_one(profile_details)

            print(f"用戶 {user_name} 的個人資料已成功創建。")
            return True

    except Exception as e:
        print("在嘗試創建用戶個人資料時發生錯誤：")
        print(e)
        return False


def deleteProfile(user_name:str):
    '''
    刪除用戶的個人資料。

    參數:
        user_name (str): 用戶名。

    返回:
        bool: 成功刪除返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["profiles"]
            
            mycol.delete_one({'user_name': user_name})

            print(f"用戶 {user_name} 的個人資料已成功刪除。")
            return True

    except Exception as e:
        print("在嘗試刪除用戶個人資料時發生錯誤：")
        print(e)
        return False

def getAssets(user_id: str):
    '''
    獲取用戶的資產詳情。

    參數:
        user_id (str): 用戶ID。

    返回:
        dict: 用戶的資產詳情，如果找不到用戶則返回 None。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["assets"]

            user_assets = mycol.find_one({'user_id': user_id})
            if user_assets:
                return user_assets['asset_details']
            else:
                return None
    except Exception as e:
        print(f"在嘗試獲取用戶資產詳情時發生錯誤： {e}")
        return None


def updateAssets(user_id: str, increase_dict: dict, decrease_dict: dict):
    '''
    更新用戶的資產。

    參數:
        user_id (str): 用戶ID。
        increase_dict (dict): 資產增加的量。
        decrease_dict (dict): 資產減少的量。

    返回:
        bool: 更新成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["assets"]

            user_assets = mycol.find_one({'user_id': user_id})
            if user_assets is not None:
                for asset, increase in increase_dict.items():
                    mycol.update_one({'user_id': user_id}, {'$inc': {f'asset_details.{asset}': increase}})

                for asset, decrease in decrease_dict.items():
                    mycol.update_one({'user_id': user_id}, {'$inc': {f'asset_details.{asset}': -decrease}})
                
                return True
            else:
                print(f"找不到用戶 {user_id} 的資產記錄。")
                return False

    except Exception as e:
        print(f"在嘗試更新用戶資產時發生錯誤： {e}")
        return False


def createAssets(user_id: str, asset_details: dict):
    '''
    創建用戶的資產。

    參數:
        user_id (str): 用戶ID。
        asset_details (dict): 資產詳情。

    返回:
        bool: 創建成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["assets"]

            mycol.insert_one({'user_id': user_id, 'asset_details': asset_details})
            return True
    except Exception as e:
        print(f"在嘗試創建用戶資產時發生錯誤： {e}")
        return False


def deleteAssets(user_id: str):
    '''
    刪除用戶的資產。

    參數:
        user_id (str): 用戶ID。

    返回:
        bool: 刪除成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["assets"]

            mycol.delete_one({'user_id': user_id})
            return True
    except Exception as e:
        print(f"在嘗試刪除用戶資產時發生錯誤： {e}")
        return False


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

def token_2_user_name(Token:str)->str:
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
            return ""
    except Exception as e:
        print("在嘗試獲取用户資料時發生錯誤：")
        print(e)
        return ""

def check_token(Token:str):
    '''
    檢查令牌是否有效。

    參數:
        Token (str): 令牌。

    返回:
        bool: 令牌是否有效。
    '''
    try:
        myclient = pymongo.MongoClient(args.mongo)
        mydb = myclient["tradingview_to_exchange"]
        mycol = mydb["users"]
        result = mycol.find_one({'user_detail.token': Token})
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
        return False

def getAccountDetails(user_id: str):
    '''
    獲取用戶的API設置。

    參數:
        user_id (str): 用戶ID。

    返回:
        dict: 用戶的API設置。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["account"]
            account_details = mycol.find_one({'user_id': user_id})
            if account_details:
                return account_details['account_details']
            else:
                print(f"找不到用戶 {user_id} 的API設置。")
                return None
    except Exception as e:
        print(f"在嘗試獲取用戶API設置時發生錯誤： {e}")
        return None


def updateAccountDetails(user_id: str, account_details: dict):
    '''
    更新用戶的API設置。

    參數:
        user_id (str): 用戶ID。
        account_details (dict): API設置。

    返回:
        bool: 更新成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["account"]
            mycol.update_one({'user_id': user_id}, {'$set': {'account_details': account_details}})
            return True
    except Exception as e:
        print(f"在嘗試更新用戶API設置時發生錯誤： {e}")
        return False


def createAccountDetails(user_id: str, account_details: dict):
    '''
    為用戶創建API設置。

    參數:
        user_id (str): 用戶ID。
        account_details (dict): API設置。

    返回:
        bool: 創建成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["account"]
            mycol.insert_one({'user_id': user_id, 'account_details': account_details})
            return True
    except Exception as e:
        print(f"在嘗試創建用戶API設置時發生錯誤： {e}")
        return False


def deleteAccountDetails(user_id: str):
    '''
    刪除用戶的API設置。

    參數:
        user_id (str): 用戶ID。

    返回:
        bool: 刪除成功返回 True，否則返回 False。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["account"]
            delete_result = mycol.delete_one({'user_id': user_id})
            if delete_result.deleted_count > 0:
                return True
            else:
                print(f"找不到用戶 {user_id} 的API設置。")
                return False
    except Exception as e:
        print(f"在嘗試刪除用戶API設置時發生錯誤： {e}")
        return False

def createLog(user_id: str, log_details: dict):
    '''
    紀錄特定事件。

    參數:
        user_id (str): 用戶ID。
        log_details (dict): 日誌詳情。

    返回:
        log_id (str): 成功創建的日誌ID。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["logs"]
            log_data = {
                "user_id": user_id,
                "log_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "log_details": log_details
            }
            res = mycol.insert_one(log_data)
            return str(res.inserted_id)
    except Exception as e:
        print(f"在嘗試創建日誌時發生錯誤： {e}")
        return None

def getLog(log_id: str):
    '''
    獲取特定日誌的詳情。

    參數:
        log_id (str): 日誌ID。

    返回:
        dict: 日誌詳情。若未找到，返回None。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["logs"]
            res = mycol.find_one({"_id": ObjectId(log_id)})
            return res
    except Exception as e:
        print(f"在嘗試獲取日誌詳情時發生錯誤： {e}")
        return None

def getUserLogs(user_id: str):
    '''
    獲取特定用戶的所有日誌。

    參數:
        user_id (str): 用戶ID。

    返回:
        list: 包含所有日誌的列表。若未找到，返回空列表。
    '''
    try:
        with pymongo.MongoClient(args.mongo) as myclient:
            mydb = myclient["tradingview_to_exchange"]
            mycol = mydb["logs"]
            res = mycol.find({"user_id": user_id})
            return [log for log in res]
    except Exception as e:
        print(f"在嘗試獲取用戶日誌時發生錯誤： {e}")
        return []


# 创建FastAPI应用实例
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
async def login(user: User):
    data = getUser(user_name=user.user_name, mongo_connection_string=args.mongo)
    if data is None:
        return {'status': 'error', 'error': 'user not found'}
    elif data['password'] != user.password:
        return {'status': 'error', 'error': 'password incorrect'}
    else:
        token, expire_date = generate_Token(user_name=user.user_name)
        update_dict = {
            "user_detail": {
                "token": token,
                "expire_date": expire_date.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        updateUser(username=user.user_name, user=update_dict)
        return {'token': token, 'expire_date': expire_date.strftime("%Y-%m-%d %H:%M:%S"), 'status': 'success'}
    
@app.post("/register")
async def register(user: RegisterUser):
    existing_user = getUser(user_name=user.name,mongo_connection_string=args.mongo)
    if existing_user is not None:
        return {'status': 'error', 'error': 'username already exists'}
    else:
        createUser(username=user.name, password=user.password,userid=user.id,email=user.email)
        return {'status': 'success'}

@app.post("/api/setting")
async def api_setting(setting: Api_settings):
    if not check_token(Token=setting.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='token incorrect or expired')

    user_id = token_2_user_name(Token=setting.token)
    update_data = {
        setting.exchange: {
            "api_key": setting.api_key,
            "secret_key": setting.secret_key,
            "phrase": setting.phrase
        }
    }
    updateUser(username=user_id, user=update_data)
    return {'status': 'success'}

def create_collection_and_index(db, collection_name, index_field):
    collection = db[collection_name]
    collection.create_index(index_field, unique=True)
    return collection

if __name__ == "__main__":
    # Initialize database
    my_client = pymongo.MongoClient(args.mongo)
    my_db = my_client["tradingview_to_exchange"]

    # Users
    token,expire_date = generate_Token(args.user_name)
    my_col = create_collection_and_index(my_db, "users", "user_name")
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
    orders_col = create_collection_and_index(my_db, "orders", "order_id")

    # Profile
    profile_col = create_collection_and_index(my_db, "profiles", "user_id")

    # Account (API Settings)
    account_col = create_collection_and_index(my_db, "account", "user_id")

    # Logs
    logs_col = create_collection_and_index(my_db, "logs", "log_id")

    # Assets
    assets_col = create_collection_and_index(my_db, "assets", "user_id")

    #exit database
    my_client.close()

    # Start API
    uvicorn.run(app, host="0.0.0.0", port=443)

