from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,date,timedelta
from hashlib import md5
import uvicorn
import json
import os
import requests
import ccxt.binanceusdm as binanceusdm
import ccxt.binance as binance

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)