import json
import os
import time

from binance.client import Client
from cryptography.fernet import Fernet
import requests


def get_config(db_url):
    response = requests.get(db_url)
    response_json = json.loads(response.text)
    key = response_json['key'].encode()
    fernet = Fernet(key)
    del response_json['key']
    config = {}
    for key, value in response_json.items():
        if key[0] != "_":
            config[key] = fernet.decrypt(value.encode()).decode()
    return config


# Get config
config = get_config(os.getenv("CONFIG_DB"))
symbol = "BNBEUR"
limit = 100
binance_api_key = config["binance_api_key"]
binance_api_secret = config["binance_api_secret"]
db_uri = config["orderbook_url"]

##Get time and order book from binance
client = Client(binance_api_key, binance_api_secret)
order_book = client.get_order_book(symbol=symbol, limit=limit)
server_time = client.get_server_time()

##Prepare json for database
server_time_order_book = {"time": server_time["serverTime"]}
server_time_order_book.update(order_book)

# Push the data to the database
if len(server_time_order_book["bids"]) >= 1 or len(server_time_order_book["asks"]) >= 1:
    response = requests.put(
        db_uri + f"/{server_time_order_book['lastUpdateId']}",
        data=json.dumps(server_time_order_book),
    )
