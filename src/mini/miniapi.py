from ccxt import mexc3
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,date,timedelta
from hashlib import md5
import uvicorn
import json
import os
import requests

app = FastAPI()

PASSWORD = os.environ.get('PASSWORD')
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK')
DATA_LOC = "DATA.json"
ORIGINAL_DATA = {
    "orders": {},
    "trades": {},
    "profits": {},
    "open": {},
}

class Order(BaseModel):
    password: str
    symbol: str
    side: str   # buy or sell
    quantity: float
    price: float
    act: str    # newpos or add or exit
"""
{
    "password": "PASSWORD",
    "symbol": "BTCUSDT",
    "side": "{{strategy.order.action}}",
    "quantity": "{{strategy.order.contracts}}",
}
"""
coin_img_dataset = {
    "BTC" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
    "LTC" : "https://s2.coinmarketcap.com/static/img/coins/64x64/2.png",
    "DOGE" : "https://s2.coinmarketcap.com/static/img/coins/64x64/74.png",
    "ETH" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
    "XRP" : "https://s2.coinmarketcap.com/static/img/coins/64x64/52.png",
    "ADA" : "https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png",
    "DOT" : "https://s2.coinmarketcap.com/static/img/coins/64x64/6636.png",
    "UNI" : "https://s2.coinmarketcap.com/static/img/coins/64x64/7083.png",
    "BCH" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1831.png",
    "LINK" : "https://s2.coinmarketcap.com/static/img/coins/64x64/1975.png",
}
crypto_img_url = "https://blog.mexc.com/wp-content/uploads/2021/12/MX_Voting_MEXC_Token-768x527.png"

order_recive_embed_template = {
    "title": "Order Recived",
    "description": "Sample Description",
    "color": 0x00ff00,
    "thumbnail": {
        "url": coin_img_dataset["BTC"]
    },
    "footer": {
        "text": "MEXC Global"
    },
    "fields": [
        {
            "name": "Symbol",
            "value": "BTCUSDT",
            "inline": True
        },
        {
            "name": "Side",
            "value": "Buy",
            "inline": True
        },
        {
            "name": "Quantity",
            "value": "0.001",
            "inline": True
        },
        {
            "name": "Price",
            "value": "10000",
            "inline": True
        },
        {
            "name": "Order Type",
            "value": "Limit",
            "inline": True
        },
        {
            "name": "Order ID",
            "value": "123456789",
            "inline": True
        },
        {
            "name": "Order Time",
            "value": "2021-01-01 00:00:00",
            "inline": True
        },
        {
            "name": "Order Status",
            "value": "Filled",
            "inline": True
        }
    ]
}

def send_discord_webhook_with_embed(embed:dict,url:str)->bool:
    """
    Sends an embed to a Discord webhook.

    Args:
        embed (dict): The embed to send. Must be a dictionary containing the following keys:
            - title (str): The title of the embed.
            - description (str): The description of the embed.
            - color (int): The color of the embed in hexadecimal format.
        
        url (str): The Discord webhook URL to send the embed to.

    Returns:
        bool: True if the embed was sent successfully, False otherwise.
    """
    requests.post(url, json={"embeds": [embed],"avatar_url":"https://i.pinimg.com/564x/94/8d/38/948d38262a9cd80fbd7acad5ff43c56f.jpg","username":"Trading Bot"})
    return True

def rec_order(order: Order):
    with open(DATA_LOC, 'r') as f:
        data = json.load(f)
    data.orders[order.symbol].append(order)
    with open(DATA_LOC, 'w') as f:
        json.dump(data, f, indent=4,sort_keys=True)
    return True

def rec_trade(trade: dict):
    with open(DATA_LOC, 'r') as f:
        data = json.load(f)
    data.trades[trade["symbol"]].append(trade)
    with open(DATA_LOC, 'w') as f:
        json.dump(data, f, indent=4,sort_keys=True)
    return True

def rec_profit(profit: dict):
    with open(DATA_LOC, 'r') as f:
        data = json.load(f)
    data.profits[profit["symbol"]].append(profit)
    with open(DATA_LOC, 'w') as f:
        json.dump(data, f, indent=4,sort_keys=True)
    return True

def rec_open(open: dict):
    with open(DATA_LOC, 'r') as f: # type: ignore
        data = json.load(f)
    temp_data = data.open[open["symbol"]]
    new_data = {
        "side": open["side"],
        "quantity": open["quantity"]+temp_data["quantity"] if open["act"] == "add" else open["quantity"] if open["act"] == "newpos" else temp_data["quantity"]-open["quantity"],
        "avg_price": (open["price"]*open["quantity"]+temp_data["avg_price"]*temp_data["quantity"])/(open["quantity"]+temp_data["quantity"]) if open["act"] == "add" else open["price"] if open["act"] == "newpos" else temp_data["avg_price"],
    }
    data.open[open["symbol"]] = new_data
    with open(DATA_LOC, 'w') as f: # type: ignore
        json.dump(data, f, indent=4,sort_keys=True)
    return True

def clear_open(symbol: str):
    with open(DATA_LOC, 'r') as f: # type: ignore
        data = json.load(f)
    data.open[symbol] = []
    with open(DATA_LOC, 'w') as f: # type: ignore
        json.dump(data, f, indent=4,sort_keys=True)

def cacu_profit(indata:dict):
    with open(DATA_LOC, 'r') as f: # type: ignore
        data = json.load(f)
    open_data = data.open[indata["symbol"]]
    if indata["side"] == "buy":
        profit = (indata["price"]-open_data["avg_price"])*indata["quantity"]
        percent = (indata["price"]-open_data["avg_price"])/open_data["avg_price"]
    else:
        profit = (open_data["avg_price"]-indata["price"])*indata["quantity"]
        percent = (open_data["avg_price"]-indata["price"])/open_data["avg_price"]
    rec_profit({"symbol": indata["symbol"], "profit": profit, "percent": percent})
    return True

@app.get("/")
async def root():
    return {"message": "This is a mini api for trading test"}

@app.post("/order")
async def order(order: Order):
    if order.password != PASSWORD:
        return JSONResponse(status_code=400, content={"message": "Password incorrect"})
    else:
        if order.act == "newpos":
            rec_order(order)
            rec_open({"symbol": order.symbol, "side": order.side, "quantity": order.quantity, "price": order.price, "act": order.act})
        if order.act == "add":
            rec_order(order)
            rec_open({"symbol": order.symbol, "side": order.side, "quantity": order.quantity, "price": order.price, "act": order.act})
        if order.act == "exit":
            """
            1. rec_order
            2. cacu_profit
            3. rec_trade
            4. rec_profit
            5. clear_open if quantity == 0
            """
            rec_order(order)
            cacu_profit({"symbol": order.symbol, "side": order.side, "quantity": order.quantity, "price": order.price})
            rec_trade({"symbol": order.symbol, "side": order.side, "quantity": order.quantity, "price": order.price})
            #clear_open(order.symbol)
            clear_open(order.symbol)
        else:
            return JSONResponse(status_code=400, content={"message": "DCA type incorrect"})
        
        return {"message": "Order received"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)