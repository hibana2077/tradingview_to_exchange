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
    selection = st.sidebar.selectbox("Go to", list(pages.keys())) if (st.session_state.get("host_location") is not None) and (date(*map(int, st.session_state.expire_date.split(" ")[0].split("-"))) >= date.today()) else "Login"
    page = pages[selection]
    page()