'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2023-03-15 13:26:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2023-03-15 14:42:41
FilePath: /tradingview_to_exchange/src/lab.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# import pymongo

# my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# my_db = my_client["tradingview_to_exchange"]
# my_col = my_db["users"]
# my_col.create_index("user_name", unique=True)
# my_col.insert_one({"user_name": "ET9423", "password": "admin", "token": "080c0d187dcaSUDE"})
# print(my_col.find_one({"user_name": "ET9423"}))
# my_col = my_db["orders"]
# my_col.create_index("order_id", unique=True)
# my_col = my_db["failed_orders"]
# my_col.create_index("order_id", unique=True)
import streamlit as st

with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")