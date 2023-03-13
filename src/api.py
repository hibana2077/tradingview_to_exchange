
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

def record_failed_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["failed_orders"]
    mycol.insert_one(order)

def record_order(order):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["orders"]
    mycol.insert_one(order)

def user_record(user):
    myclient = pymongo.MongoClient(args.mongo)
    mydb = myclient["tradingview_to_exchange"]
    mycol = mydb["users"]
    #覆盖原有记录
    mycol.update_one({'user_name': user['user_name']}, {'$set': user}, upsert=True)

def get_user_record(user_name:str):
    my_client = pymongo.MongoClient(args.mongo)
    my_db = my_client["tradingview_to_exchange"]
    my_col = my_db["users"]
    data = my_col.find_one({'user_name': user_name})
    return data

def generate_Token(user_name:str):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #MD5加密
    Token = md5(user_name.encode()+date.encode()).hexdigest()
    #過期日期
    expire_date = datetime.now()+timedelta(days=5)
    return (Token,expire_date.strftime("%Y-%m-%d %H:%M:%S"))


class Order(BaseModel):
    api_key: str # API key for the exchange
    symbol: str # Symbol of the coin to buy
    side: str # Buy or sell   
    type: str # Market or limit
    quantity: float # Quantity of the coin to buy
    leverage: Optional[int] = None # Leverage of the coin to buy
    price: Optional[float] = None # Price of the coin to buy
    class_SF: Optional[str] = None # Spot or future
    webhook: Optional[str] = None # Webhook to send the order status
    note: Optional[str] = None # Note for the order

class front_Query(BaseModel):
    symbol: Optional[str] = None
    date: Optional[str] = None # Date of the coin to buy , format: YYYY-MM-DD
    side: Optional[str] = None # Buy or sell

class User(BaseModel):
    user_name: str
    password: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(user: User):
    if user.user_name == args.user_name and user.password == args.password:
        Token,expire_date = generate_Token(user.user_name)
        user_record({'user_name': user.user_name, 'Token': Token, 'expire_date': expire_date})
        return {'Token': Token, 'expire_date': expire_date}
    

if __name__ == "__main__":
    #set up the database
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
    #run the server
    uvicorn.run(app, host="0.0.0.0",port=80)