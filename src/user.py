'''
Author: hibana2077 hibana2077@gmail.com
Date: 2023-03-12 10:22:06
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2023-03-13 12:50:44
FilePath: \tradingview_to_exchange\src\user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
import streamlit as st
import openai
from datetime import datetime, timedelta, date



def welcome():
    st.title("Welcome")
    st.markdown()

def login():
    st.title("Login")
    host_location = st.text_input("Host Location(IP Address)")
    user_name = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.host_location = host_location
        st.session_state.user_name = user_name
        st.session_state.password = password
        response = requests.post(f"http://{host_location}:80/login", json={"user_name": user_name, "password": password})
        if response.status_code == 200:
            if response.json()["status"] == "Success":
                st.session_state.token = response.json()["token"]
                st.session_state.user_id = response.json()["user_id"]
                st.session_state.user_name = response.json()["user_name"]
                st.session_state.expire_date = response.json()["expire_date"]
            elif response.json()["status"] == "Failure":
                st.error(response.json()["message"])
        else:
            st.error("Login Failed - Please check your host location and credentials")
        


pages = {
    "Welcome": welcome,
    "Login": login,
}

if __name__ == "__main__":
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Go to", list(pages.keys())) if (date(*map(int, st.session_state.expire_date.split(" ")[0].split("-"))) >= date.today()) else "Login"
    page = pages[selection]
    page()