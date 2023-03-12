'''
Author: hibana2077 hibana2077@gmail.com
Date: 2023-03-11 23:14:36
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2023-03-12 11:40:47
FilePath: \tradingview_to_exchange\src\api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ccxt import binance,okex5
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

class Order(BaseModel):
    api_key: str # API key for the exchange
    symbol: str # Symbol of the coin to buy
    side: str # Buy or sell   
    type: str # Market or limit
    quantity: float # Quantity of the coin to buy
    price: Optional[float] = None # Price of the coin to buy
    class_SF: Optional[str] = None # Spot or future
    webhook: Optional[str] = None # Webhook to send the order status

class front_Query(BaseModel):
    symbol: Optional[str] = None
    date: Optional[str] = None # Date of the coin to buy , format: YYYY-MM-DD
    side: Optional[str] = None # Buy or sell

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/order")
def create_order(order: Order):
    

while True:
    try:
        if __name__ == "__main__":
    
            uvicorn.run(app, host="0.0.0.0", port=80)
    except Exception as e:
        print(e)
        pass