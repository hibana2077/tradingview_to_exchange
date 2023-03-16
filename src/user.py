
import requests
import streamlit as st
import pandas as pd
import openai
from plotly import graph_objects as go
from plotly import express as px
from ccxt import binance,okex5
from datetime import datetime, timedelta, date

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="TV2EX -- Quantitative Trading Platform",
    page_icon="https://media.discordapp.net/attachments/868759966431973416/1085575299871277116/HEX_Inc..png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

Greetings = {
    "morning": "Good morning",
    "afternoon": "Good afternoon",
    "evening": "Good evening",
    "night": "Good night",
}

emoji_dict = {
    "morning": "🌅",
    "afternoon": "🌇",
    "evening": "🌆",
    "night": "🌃",
}

def best_greeting():
    hour = datetime.now().hour
    if 6>hour>=0:
        return Greetings["night"]
    elif 12>hour>=6:
        return Greetings["morning"]
    elif 18>hour>=12:
        return Greetings["afternoon"]
    elif 24>hour>=18:
        return Greetings["evening"]

def best_emoji():
    hour = datetime.now().hour
    if 6>hour>=0:
        return emoji_dict["night"]
    elif 12>hour>=6:
        return emoji_dict["morning"]
    elif 18>hour>=12:
        return emoji_dict["afternoon"]
    elif 24>hour>=18:
        return emoji_dict["evening"]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df

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
    else:
        return False

def Dashboard():
    if is_login():
        greeting = best_greeting()
        welcom_str = f"""<p style="font-size:320%;">{greeting} <span style="color:#ECD53F">{st.session_state.user_name}</span> ! {best_emoji()}</p>"""
        st.markdown(welcom_str,unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", "20", delta="+1.68%", help="Total orders in the past 24 hours") #connect to database
        col2.metric("Unrealized PnL", "168 USDT", delta="+0.5%", help="Unrealized PnL in the past 24 hours") #connect to database
        col3.metric("Realized PnL", "289 USDT", delta="+0.5%", help="Realized PnL in the past 24 hours") #connect to database
        st.markdown("""## Analytics""") #connect to database
        tab1 , tab2, tab3 = st.tabs(["Portfolio", "Trade History", "Trade Analysis"])
        with tab1:
            st.markdown("""### Portfolio""")
            portfolio_data = {
                "symbol": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "LINKUSDT", "SOLUSDT", "UNIUSDT", "AVAXUSDT", "FILUSDT", "BCHUSDT", "THETAUSDT", "VETUSDT", "XLMUSDT", "TRXUSDT", "ETCUSDT", "ICPUSDT"],
                "quantity": ["0.001", "0.01", "0.1", "10", "1000", "0.01", "1.", "1", "0.1", "0.01", "0.1", "1", "0.1", "0.01", "1", "10", "100", "1000", "10", "1"],
                "price": ["$50000", "$2000", "$400", "$2.50", "$0.30", "$40", "$1.50", "$200", "$40", "$50", "$40", "$60", "$60", "$600", "$10", "$0.20", "$0.50", "$0.10", "$10", "$60"],
                "value": ["$50", "$20", "$40", "$25", "$300", "$400", "$15", "$2000", "$400", "$500", "$400", "$600", "$600", "$6000", "$100", "$2", "$50", "$10", "$100", "$600"],
            }
            portfolio_df = pd.DataFrame(portfolio_data)
            portfolio_df["price"] = portfolio_df["price"].apply(lambda x: x.replace("$",""))
            portfolio_df["value"] = portfolio_df["value"].apply(lambda x: x.replace("$",""))
            portfolio_df["quantity"] = portfolio_df["quantity"].astype(float)
            portfolio_df["price"] = portfolio_df["price"].astype(float)
            portfolio_df["value"] = portfolio_df["value"].astype(float)
            portfolio_df["price"] = portfolio_df["price"].apply(lambda x: f"${x:,.4f}")
            portfolio_df["value"] = portfolio_df["value"].apply(lambda x: f"${x:,.4f}")
            #pie chart
            fig = px.pie(portfolio_df, values='value', names='symbol', title='Portfolio Value')
            # fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)
        st.markdown("""## Orders""") #connect to database
        tab1 , tab2, tab3 = st.tabs(["Open Orders", "Closed Orders", "All Orders"])
        with tab1:
            st.markdown("""### Open Orders""")
            openorder_data = {
                "symbol": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "LINKUSDT", "SOLUSDT"],
                "side": ["Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell"],
                "price": ["$50,000", "$2,000", "$400", "$2.50", "$0.30", "$40", "$1.50", "$200", "$40", "$50"],
                "quantity": ["0.001", "0.01", "0.1", "10", "1000", "10", "100", "1", "10", "1"],
                "Unrealized PnL": ["$14", "$2", "$4", "$0.25", "$0.03", "$4", "$0.15", "$20", "$4", "$5"],
            }#connect to database
            st.table(openorder_data)
        with tab2:
            st.markdown("""### Closed Orders""")
            closedorder_data = {
                "symbol": ["DODOUSDT", "UNIUSDT", "FILUSDT", "AAVEUSDT", "ICPUSDT", "SUSHIUSDT", "AVAXUSDT", "XLMUSDT", "BCHUSDT", "EOSUSDT"],
                "side": ["Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell"],
                "price": ["$5.50", "$30", "$60", "$350", "$50", "$10", "$70", "$0.50", "$600", "$5"],
                "quantity": ["0.1", "0.1", "0.01", "0.1", "0.1", "0.01", "0.1", "100", "0.01", "0.1"],
                "Realized PnL": ["$1.4", "$0.2", "$0.4", "$0.25", "$0.03", "$0.4", "$0.15", "$2.0", "$0.4", "$0.5"],
            }
            st.table(closedorder_data)
        with tab3:
            st.markdown("""### All Orders""")
            allorder_data = {
                "symbol": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "LINKUSDT", "SOLUSDT","DODOUSDT", "UNIUSDT", "FILUSDT", "AAVEUSDT", "ICPUSDT", "SUSHIUSDT", "AVAXUSDT", "XLMUSDT", "BCHUSDT", "EOSUSDT"],
                "side": ["Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell","Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell", "Buy", "Sell"],
                "price": ["$50,000", "$2,000", "$400", "$2.50", "$0.30", "$40", "$1.50", "$200", "$40", "$50","$5.50", "$30", "$60", "$350", "$50", "$10", "$70", "$0.50", "$600", "$5"],
                "quantity": ["0.001", "0.01", "0.1", "10", "1000", "10", "100", "1", "10", "1","0.1", "0.1", "0.01", "0.1", "0.1", "0.01", "0.1", "100", "0.01", "0.1"],
                "status":["Open","Open","Open","Open","Open","Open","Open","Open","Open","Open","Closed","Closed","Closed","Closed","Closed","Closed","Closed","Closed","Closed","Closed"],
            }
            st.table(allorder_data)
        

def Trend():
    st.markdown("""# Trend""")

def Setting():
    st.markdown("""# Setting""")
    st.markdown("""## User Setting""")
    st.markdown("""## API Setting""")
    st.markdown("""## Webhook Setting""")
    st.markdown("""## Tradingview Setting""")
    st.markdown("""## Exchange Setting""")
    

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
    "Trend": Trend,
}

login_user_page = {
    "Dashboard": Dashboard,
    "Trend": Trend,
    "User Manual": User_manual,
    "Setting": Setting,
    "Logout": logout,
}

unlogin_user_page = {
    "Welcome": welcome,
    "Login": login,
}


if __name__ == "__main__":
    # st.sidebar.title("Navigation")
    # col1,_ = st.columns([1,1])
    # selection = st.sidebar.selectbox("Go to", list(login_user_page.keys())) if is_login() else st.sidebar.selectbox("Go to", list(unlogin_user_page.keys()))
    # page = pages[selection]
    # page()
    with st.sidebar:
        col1,_ = st.columns([1,1])
        with col1:
            st.image("https://media.discordapp.net/attachments/868759966431973416/1085575034933874748/HEX_Inc..png",width=200)
        st.title("TV2EX")
        selection = st.selectbox("Go to", list(login_user_page.keys())) if is_login() else st.selectbox("Go to", list(unlogin_user_page.keys()))
        
    page = pages[selection]
    page()