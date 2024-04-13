'''
Author: hibana2077 hibana2077@gmail.com
Date: 2023-06-10 18:31:13
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-04-13 21:28:21
FilePath: \tradingview_to_exchange\src\web_api\api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)