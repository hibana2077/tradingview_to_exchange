'''
Author: hibana2077 hibana2077@gmaill.com
Date: 2023-03-15 13:26:23
LastEditors: hibana2077 hibana2077@gmaill.com
LastEditTime: 2023-03-15 16:48:13
FilePath: /tradingview_to_exchange/src/user.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import requests
import streamlit as st
import openai
from datetime import datetime, timedelta, date

#init session state
if "is_login" not in st.session_state:
    st.session_state.is_login = False
    
def set_login_satae(state_in:str,data:dict):
    if state_in=="clear":
        st.session_state.host_location = ""
        st.session_state.user_name = ""
        st.session_state.password = ""
        st.session_state.token = ""
        st.session_state.user_id = ""
        st.session_state.user_name = ""
        st.session_state.expire_date = ""
        st.session_state.is_login = False
    elif state_in=="set":
        st.session_state.host_location = data["host_location"]
        st.session_state.user_name = data["user_name"]
        st.session_state.password = data["password"]
        st.session_state.token = data["token"]
        st.session_state.user_id = data["user_id"]
        st.session_state.user_name = data["user_name"]
        st.session_state.expire_date = data["expire_date"]
        st.session_state.is_login = True
    else:
        raise ValueError("state must be 'clear' or 'set'")
    return st.experimental_rerun()
    

def is_login():
    if st.session_state.is_login:
        #check token expire date
        if st.session_state.expire_date > datetime.now():
            return True
        else:
            set_login_satae("clear", {})
            return False
    else:
        return False

def Dashboard():
    if is_login():
        welcom_str = f"""<p style="font-size:200%;">Welcome back <span style="color:#ECD53F">{st.session_state.user_name}</span>.</p>"""
        st.markdown(welcom_str,unsafe_allow_html=True)

def Setting():
    st.markdown("""# Setting""")

def welcome():
    st.markdown("""# Welcome to the Tradingview to Exchange App""")

def User_manual():
    st.markdown("""# User Manual""")

def logout():
    set_login_satae("clear", {})

def login():
    st.title("Login")
    host_location = st.text_input("Host Location(IP Address)")
    user_name = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.host_location = host_location
        st.session_state.user_name = user_name
        st.session_state.password = password
        if user_name == "" or password == "":
            st.error("Please enter your user name and password")
        if user_name == "test" and password == "test":
            st.success("Login Success")
            exprie_date = datetime.now() + timedelta(days=1)
            set_login_satae("set", {"host_location":host_location,"user_name":user_name,"password":password,"token":"test","user_id":"test","user_name":"test","expire_date":exprie_date})
            
        else:
            response = requests.post(f"http://{host_location}:80/login", json={"user_name": user_name, "password": password})
            if response.status_code == 200:
                if response.json()["status"] == "Success":
                    st.success(response.json()["message"])
                    set_login_satae("set", response.json()["data"])
                elif response.json()["status"] == "Failure":
                    st.error(response.json()["message"])
            else:
                st.error("Login Failed - Please check your host location and credentials")
        


pages = {
    "Dashboard": Dashboard,
    "Welcome": welcome,
    "Login": login,
    "Setting": Setting,
    "Logout": logout,
    "User Manual": User_manual,
}

login_user_page = {
    "Dashboard": Dashboard,
    "User Manual": User_manual,
    "Setting": Setting,
    "Logout": logout,
}

unlogin_user_page = {
    "Welcome": welcome,
    "Login": login,
}


if __name__ == "__main__":
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Go to", list(login_user_page.keys())) if is_login() else st.sidebar.selectbox("Go to", list(unlogin_user_page.keys()))
    page = pages[selection]
    page()