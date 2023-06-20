
import requests
import streamlit as st
import pandas as pd
import json
from random import randint
from plotly import graph_objects as go
from plotly import express as px
from ccxt import okex5,bitget,bybit,binanceusdm,Exchange,binance
from datetime import datetime, timedelta, date

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

binance_f_ex = binanceusdm({
    'option': {
        "defaultType": "swap",
        "fetchMarkets": ["swap"]
    },
})

binance_s_ex = binance({
    "options": {
        "defaultType": "spot",
        "fetchMarkets": ["spot"]
    },
})

exchange_dict = {
    "OKEx": okex5({}),
    "Bitget": bitget({}),
    "Bybit": bybit({}),
}

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

def best_risk_color(risk:int):
    if risk < 25:
        return "#67E82E"
    elif risk < 50:
        return "#FFE940"
    else:
        return "#FF5340"
    
def best_win_rate_color(win_rate:int):
    if win_rate < 25:
        return "#FF5340"
    elif win_rate < 50:
        return "#FFE940"
    else:
        return "#67E82E"

def fliter_symbols_list(symbols_list:list,type:str,exchange:Exchange):
    '''
    This function is used to filter symbols list by type(swap,spot)
    '''
    filtered_symbols_list = []
    for symbol in symbols_list:
        if exchange.markets[symbol]['type'] == type:
            filtered_symbols_list.append(symbol)
    return filtered_symbols_list

def Caculate_Unrealized_Pnl(open_orders_data:dict,exchange:Exchange):
    for symbol in open_orders_data.keys():
        symbol_history_df = pd.DataFrame(exchange.fetch_ohlcv(symbol, '1m', limit=10))
        most_recent_price_index = symbol_history_df[4].idxmax()
        most_recent_price = symbol_history_df[4][most_recent_price_index]
        if open_orders_data[symbol]['side'] == 'buy':
            open_orders_data[symbol]['Unrealized'] = round((most_recent_price - open_orders_data[symbol]['entry_price'])*open_orders_data[symbol]['entry_quantity'],2)
        else:
            open_orders_data[symbol]['Unrealized'] = round((open_orders_data[symbol]['entry_price'] - most_recent_price)*open_orders_data[symbol]['entry_quantity'],2)
    return open_orders_data

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
    
#init session state
if "is_login" not in st.session_state:
    st.session_state.binance_api_key = ""
    st.session_state.binance_secret_key = ""
    st.session_state.okex_api_key = ""
    st.session_state.okex_secret_key = ""
    st.session_state.okex_passphrase = ""
    set_login_satae("clear",{})
    

def is_login():
    if st.session_state.is_login:
        #check token expire date
        if st.session_state.expire_date > datetime.now():
            return True
        else:
            set_login_satae("clear", {})
    else:
        return False

def Analysis():
    st.markdown("""## Analysis""") #connect to database
    tab1, tab2 = st.tabs(["Trading Data", "Performance"])
    with tab1:
        col1,col2 = st.columns([1,2])
        with col1:
            st.markdown("""### Data Overview""") #connect to database
            col_tiny_1 , col_tiny_2 = st.columns([1,1])
            col_tiny_1.metric("30 Days ROI", "+99.19 %", delta="+45.5 %", help="30 Days ROI") #connect to database
            col_tiny_2.metric("30 Days PnL", "1680 USDT", delta="+560", help="30 Days PnL") #connect to database
            st.markdown("""---""")
            account_assets = 1000 #connect to database
            risk_score = 45 #connect to database
            win_rate = 80 #connect to database
            total_trades = 1258 #connect to database
            profit_trades = 1000 #connect to database
            loss_trades = 258 #connect to database
            average_profit = 1.68 #connect to database
            average_loss = -0.65 #connect to database
            profit_loss_ratio = 2.6 #connect to database
            average_trade_duration = 1.5 #connect to database
            trading_frequency = 19 #connect to database
            last_trade_date = "2023-03-16" #connect to database
            st.markdown(f"""<p style="font-size:155%;"> Account Asset: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{account_assets} </span>USDT</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Account Risk: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:{best_risk_color(risk=risk_score)}">{risk_score} </span>%</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Win Rate: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:{best_win_rate_color(win_rate=win_rate)}">{win_rate} </span>%</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Total Trades: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{total_trades}</span></p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Profit Trades: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{profit_trades}</span></p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Loss Trades: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">{loss_trades}</span></p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Average Profit: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{average_profit} </span>USDT</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Average Loss: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">{average_loss} </span>USDT</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Profit/Loss Ratio: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{profit_loss_ratio}</span></p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Average Trade Duration: &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{average_trade_duration} </span>days</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Trading Frequency: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{trading_frequency} </span>trades/day</p>""",unsafe_allow_html=True)
            st.markdown(f"""<p style="font-size:155%;"> Last Trade Date: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:green">{last_trade_date}</span></p>""",unsafe_allow_html=True)
        with col2:
            st.markdown("""### ROI""")#connect to database
            ROI_data = {
                "date": [i for i in range(1, 34)],
                "ROI": [i for i in range(1,100,3)]
            }
            ROI_df = pd.DataFrame(ROI_data)
            fig = px.line(ROI_df, x="date", y="ROI")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="ROI",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="RebeccaPurple"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            col_tiny_1 , col_tiny_2 = st.columns([1,1])
            with col_tiny_1:
                st.markdown("""### Every week income""")#connect to database
                weekly_income_data = {
                    "date": [date(2021, 1, 1) + timedelta(days=i) for i in range(1, 180,7)],
                    "income": [randint(1, 100) for i in range(26)]
                }
                weekly_income_df = pd.DataFrame(weekly_income_data)
                fig = px.bar(weekly_income_df, x="date", y="income")
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Income",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="RebeccaPurple"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            with col_tiny_2:
                st.markdown("""### Risk """)#connect to database
                risk_data = {
                    "date": [date(2021, 1, 1) + timedelta(days=i) for i in range(1, 180,7)],
                    "risk": [randint(1, 3) for i in range(26)]
                }
                risk_df = pd.DataFrame(risk_data)
                fig = px.bar(risk_df, x="date", y="risk")
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Risk",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="RebeccaPurple"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("""### Trade Symbol""")#connect to database
        trade_symbol_data = {
            "Symbol": ["LINK","BTC","ETH","ADA","DOGE","XRP","DOT","LTC","BCH","UNI","SOL","BNB"],
            "Total Trades": [randint(2, 100) for i in range(12)],
            "Profit": [randint(2, 100) for i in range(12)],
        }
        trade_symbol_df = pd.DataFrame(trade_symbol_data)
        fig = px.pie(trade_symbol_df, values='Total Trades', names='Symbol', title='Total Trades', hover_data=['Profit'], labels={'Profit':'Profit'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            xaxis_title="Symbol",
            yaxis_title="Total Trades",
            font=dict(
                family="Helvetica, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        st.markdown("""### Performance""")# compare with S&P500 and other index roi , index roi need to scrape from yahoo finance.

def Dashboard():
    if is_login():
        greeting = best_greeting()
        welcom_str = f"""<p style="font-size:320%;">{greeting} <span style="color:#ECD53F">{st.session_state.user_name}</span> ! {best_emoji()}</p>"""
        st.markdown(welcom_str,unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", "20", delta="+1.68%", help="Total orders in the past 24 hours") #connect to database
        col2.metric("Unrealized PnL", "168 USDT", delta="+0.5%", help="Unrealized PnL in the past 24 hours") #connect to database
        col3.metric("Realized PnL", "289 USDT", delta="+0.5%", help="Realized PnL in the past 24 hours") #connect to database
        daily_roi_data = {
            "date": ["2023-01-"+str(date_it) for date_it in range(1, 31)],
            "ROI": [randint(1, 100) for i in range(30)],
        }
        daily_roi_df = pd.DataFrame(daily_roi_data)
        daily_roi_df["date"] = pd.to_datetime(daily_roi_df["date"])
        fig_daily_roi = px.line(daily_roi_df, x="date", y="ROI", title="Daily ROI")
        st.plotly_chart(fig_daily_roi, use_container_width=True)
        st.markdown("""## Orders""") #connect to database
        tab1 , tab2 = st.tabs(["Open Orders", "Closed Orders"])
        with open('src/sample_data.json') as f: #this can change to connect api server
            openorder_data = json.load(f)
        with st.spinner("Loading Data..."):
            openorder_df = pd.DataFrame(Caculate_Unrealized_Pnl(openorder_data["open_orders"],binance_f_ex)).T
        with tab1:
            st.markdown("""### Open Orders""")
            st.dataframe(filter_dataframe(openorder_df))
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
        

def Trend():
    st.markdown("""# Trend""")

def Setting():
    st.markdown("""# Setting""")
    st.markdown("""## User Setting""")
    user_setting_form = st.form(key="user_setting_form")
    user_name = user_setting_form.text_input("User Name")
    pass_word = user_setting_form.text_input("Password", type="password")


    if user_setting_form.form_submit_button("Save"):
        st.session_state.user_name = user_name
        st.session_state.pass_word = pass_word
        #send request to backend
        data = {
            "user_name": user_name if user_name != "" else st.session_state.user_name,
            "pass_word": pass_word if pass_word != "" else st.session_state.pass_word,
        }
        url = st.session_state.host_location + "/api/user_setting"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success("User Setting Saved!")
        else:
            st.error("User Setting Failed!")
    st.markdown("""## API Setting""")
    binance_tab , okex_tab = st.tabs(["Binance", "OKEx"])
    with binance_tab:
        binance_api_setting_form = st.form(key="binance_api_setting_form")
        binance_api_key = binance_api_setting_form.text_input("API Key")
        binance_secret_key = binance_api_setting_form.text_input("Secret Key")
        if binance_api_setting_form.form_submit_button("Save"):
            st.session_state.binance_api_key = binance_api_key
            st.session_state.binance_secret_key = binance_secret_key
            #send request to backend
            data = {
                "user_name": st.session_state.user_name,
                "api_key": binance_api_key if binance_api_key != "" else st.session_state.binance_api_key,
                "secret_key": binance_secret_key if binance_secret_key != "" else st.session_state.binance_secret_key,
            }
            url = st.session_state.host_location + "/api/binance_api_setting"
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.success("Binance API Setting Saved!")
            else:
                st.error("Binance API Setting Failed!")
    with okex_tab:
        okex_api_setting_form = st.form(key="okex_api_setting_form")
        okex_api_key = okex_api_setting_form.text_input("API Key")
        okex_api_secret = okex_api_setting_form.text_input("Secret Key")
        okex_passphrase = okex_api_setting_form.text_input("Passphrase")
        if okex_api_setting_form.form_submit_button("Save"):
            st.session_state.okex_api_key = okex_api_key
            #send request to backend
            data = {
                "user_name": st.session_state.user_name,
                "api_key": okex_api_key if okex_api_key != "" else st.session_state.okex_api_key,
                "api_secret": okex_api_secret if okex_api_secret != "" else st.session_state.okex_api_secret,
                "passphrase": okex_passphrase if okex_passphrase != "" else st.session_state.okex_passphrase,
            }
            url = st.session_state.host_location + "/api/okex_api_setting"
            response = requests.post(url, json=data)
            if response.status_code == 200:
                st.success("OKEx API Setting Saved!")
            else:
                st.error("OKEx API Setting Failed!")
    st.markdown("""## Webhook Setting""")
    exchange = st.selectbox("Exchange", ["Binance", "OKEx","Bitget","Bybit"])
    class_SF = st.selectbox("Class", ["spot", "swap"])
    if exchange == "Binance":
        exchange_ex = binance_f_ex if class_SF == "swap" else binance_s_ex
        exchange_ex.load_markets()
        symbol_list = list(exchange_ex.symbols)
    else:
        exchange_ex = exchange_dict[exchange]
        symbol_list = fliter_symbols_list(exchange_ex, class_SF)
    exchange_ex.load_markets()
    symbol = st.selectbox("Symbol", symbol_list)
    webhook_setting_form = st.form(key="webhook_setting_form")
    order_type = webhook_setting_form.selectbox("Order Type", ["Limit", "Market"])
    quantity_rule = exchange_ex.markets[symbol]['limits']['amount']
    leverage_rule = exchange_ex.markets[symbol]['limits']['leverage']
    quantity = webhook_setting_form.number_input("Quantity", min_value=quantity_rule['min'], max_value=quantity_rule['max'],help=f"Min: {quantity_rule['min']}, Max: {quantity_rule['max']}")
    
    if webhook_setting_form.form_submit_button("Generate Tradingview alert"):
        st.success("Tradingview alert generated!")
        

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
    "Analysis": Analysis,
}

login_user_page = {
    "Dashboard": Dashboard,
    "Analysis": Analysis,
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
