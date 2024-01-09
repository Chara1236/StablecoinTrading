import websocket, json, numpy, talib, config, pprint
from binance.enums import *
import os
from binance.client import Client
import panel

client = Client(os.getenv('api_key'), os.getenv('api_secret'))
klines = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
print(klines)