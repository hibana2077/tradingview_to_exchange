'''
Author: hibana2077 hibana2077@gmail.com
Date: 2023-03-11 23:14:36
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2023-03-12 02:18:12
FilePath: \tradingview_to_exchange\src\api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from ccxt import binance
import pymongo
import uvicorn
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--mongo', type=str, default='mongodb://localhost:27017/', help='MongoDB connection string')
parser.add_argument('--user_name', type=str, default='admin', help='APP user name')
parser.add_argument('--password', type=str, default='admin', help='APP password')

args = parser.parse_args()

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
    if order.class_SF == "Spot":
        binance_spot = binance({
            'apiKey': order.api_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            },
        })
        if order.type == "Market":
            order = binance_spot.create_order(
                symbol=order.symbol,
                type="market",
                side=order.side,
                amount=order.quantity
            )
        elif order.type == "Limit":
            order = binance_spot.create_order(
                symbol=order.symbol,
                type="limit",
                side=order.side,
                amount=order.quantity,
                price=order.price
            )
        else:
            my_client = pymongo.MongoClient(args.mongo)
            my_db = my_client["tradingview_to_exchange"]
            my_col = my_db["orders"]
            my_dict = {
                "api_key": order.api_key,
                "symbol": order.symbol,
                "side": order.side,
                "type": order.type,
                "quantity": order.quantity,
                "price": order.price,
                "class_SF": order.class_SF,
                "webhook": order.webhook,
                "status": "Error: Invalid order type"
            }
            my_col.insert_one(my_dict)
            return {"status": "Error: Invalid order type"}
    elif order.class_SF == "Future":
        binance_future = binance({
            'apiKey': order.api_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            },
        })
        if order.type == "Market":
            order = binance_future.create_order(
                symbol=order.symbol,
                type="market",
                side=order.side,
                amount=order.quantity
            )
        elif order.type == "Limit":
            order = binance_future.create_order(
                symbol=order.symbol,
                type="limit",
                side=order.side,
                amount=order.quantity,
                price=order.price
            )

while True:
    try:
        if __name__ == "__main__":
    
            uvicorn.run(app, host="0.0.0.0", port=80)
    except Exception as e:
        print(e)
        pass