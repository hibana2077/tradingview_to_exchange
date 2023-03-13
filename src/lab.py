import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["tradingview_to_exchange"]
my_col = my_db["users"]
my_col.create_index("user_name", unique=True)
my_col.insert_one({"user_name": "ET9423", "password": "admin", "token": "080c0d187dcaSUDE"})
print(my_col.find_one({"user_name": "ET9423"}))
my_col = my_db["orders"]
my_col.create_index("order_id", unique=True)
my_col = my_db["failed_orders"]
my_col.create_index("order_id", unique=True)