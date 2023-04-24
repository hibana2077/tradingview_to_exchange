from ccxt import binanceusdm,binancecoinm,okex5,Exchange,bybit
from random import randint,random,uniform
from datetime import datetime,timedelta
from faker import Faker
import pandas as pd
import json
import logging
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)

def generate_open_order(exchange:Exchange,username_list:list):
    exchange.load_markets()
    data_list = [symbol for symbol in exchange.symbols if ':USDT' in symbol]
    random_open_order_symbols = [data_list[i] for i in sorted([int(random()*len(data_list)) for _ in range(25)])]
    entry_data = {}
    entry_data = []
    order_id_count = 1
    for symbol,username in zip(random_open_order_symbols,username_list):
        side = randint(0,1)
        symbol_history_df = pd.DataFrame(exchange.fetch_ohlcv(symbol, '15m', limit=1000))
        symbol_min_value = exchange.markets[symbol]['limits']['amount']['min']
        symbol_max_value = exchange.markets[symbol]['limits']['amount']['max']
        if symbol_max_value == None or symbol_min_value == None:
            symbol_max_value, symbol_min_value = 100,500
        quantity = uniform(symbol_min_value,symbol_max_value)
        if quantity*symbol_history_df[4][1] > 1000:
            quantity = round(1000/symbol_history_df[4][1],4)
        if side == 0:
            most_lowest_price_index = symbol_history_df[4].idxmin()
            entry_data.append({
                'order_id': str(order_id_count)+str(datetime.fromtimestamp(symbol_history_df[0][most_lowest_price_index]/1000).strftime("%Y-%m-%d %H:%M:%S")),
                'order_time': datetime.fromtimestamp(symbol_history_df[0][most_lowest_price_index]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                'order_owner': username,
                'order_status': 'open',
                'order_detail': {
                    'symbol': symbol,
                    'side': 'buy',
                    'entry_price': symbol_history_df[4][most_lowest_price_index],
                    'entry_quantity': quantity,
                    'entry_leverage': randint(1,25),
                    'entry_type': 'market',
                    'entry_class_SF': 'swap',
                    'exchange': exchange.id,
                }
            }
            )
        else:
            most_highest_price_index = symbol_history_df[4].idxmax()
            entry_data.append({
                'order_id': str(order_id_count)+str(datetime.fromtimestamp(symbol_history_df[0][most_highest_price_index]/1000).strftime("%Y-%m-%d %H:%M:%S")),
                'order_time': datetime.fromtimestamp(symbol_history_df[0][most_highest_price_index]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                'order_owner': username,
                'order_status': 'open',
                'order_detail': {
                    'symbol': symbol,
                    'side': 'sell',
                    'entry_price': symbol_history_df[4][most_highest_price_index],
                    'entry_quantity': quantity,
                    'entry_leverage': randint(1,25),
                    'entry_type': 'market',
                    'entry_class_SF': 'swap',
                    'exchange': exchange.id,
                }
            }
            )
        order_id_count += 1
    return entry_data

def generate_Users_document(usernum:int):

    fake = Faker()
    users = []
    user_id_list = []

    for i in range(usernum):
        name = fake.name()
        user_id = name.lower().replace(' ','_')
        card_type = ''
        while card_type not in ['visa','mastercard','discover','jcb']:
            card_type = fake.credit_card_provider().lower()
        users.append({
            'user_id': user_id,
            'user_name': name,
            'user_email': name.split(' ')[1].lower() + '@gmail.com',
            'user_password': fake.password(),
            'user_details' : {
                'credit_card' : {
                    'card_number': fake.credit_card_number(card_type=str(card_type).lower().replace(' ','')),
                    'card_type': card_type,
                    'card_holder_name': name,
                    'card_expiry_date': fake.credit_card_expire(start='now', end='+10y', date_format='%m/%y'),
                    'card_cvv': fake.credit_card_security_code(card_type=str(card_type).lower().replace(' ','')),
            }
        }
        })
        user_id_list.append(user_id)
    return users,user_id_list

def generate_Accounts_document(usernum:int,user_id_list:list):

    Accounts = []

    for i in range(usernum):
        Accounts.append({
            'user_id': user_id_list[i],
            'user_details': {
                'account_balance': {
                    'USDT': randint(1000,10000),
                    'BTC': randint(1,5),
                    'ETH': randint(1,10),
                    'BNB': randint(1,10),
                }
            }
        })
    return Accounts



if __name__ == "__main__":

    log.info('Generating Data...')  
    #Users Document
    users,user_id_list = generate_Users_document(10)
    with open('users.json','w') as f:
        json.dump(users,f)
    log.info('Users Document Generated')

    log.info('Generating Accounts Document...')
    #Accounts Document
    Accounts = generate_Accounts_document(10,user_id_list)
    with open('Accounts.json','w') as f:
        json.dump(Accounts,f)
    log.info('Accounts Document Generated')

    log.info('Generating Open Orders Document...')
    #Open Orders Document
    exchange = binanceusdm()
    open_orders = generate_open_order(exchange,user_id_list)
    with open('open_orders.json','w') as f:
        json.dump(open_orders,f)
    log.info('Open Orders Document Generated')

    log.info('All Documents Generated')