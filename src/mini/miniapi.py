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
        else:
            return JSONResponse(status_code=400, content={"message": "DCA type incorrect"})