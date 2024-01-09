import os
import time
from math import floor

from binance.client import Client
api_key= 'DwXGx3OHhJW3HLWunecES4yUzyQ2dCPSmKZiD6cWDMvbHmtDmfQexsjhkq3R8WT1'
api_secret= 'BAxDABXN4yl98s89KdRoy7cXEvk0SRqSzNRlFTyp4M4xdkNPfK5d2pAtQhe47Lot'
client = Client(api_key, api_secret)

def getpair(pair):
    prices = client.get_all_tickers()
    for x in prices:
        if x['symbol'] == pair:
            return x['price']
    return "Doesn't exist"


def gettrade(pair, recent):
    trades = client.get_my_trades(symbol=pair)
    recent = len(trades) - recent - 1
    return trades[recent]

def getorder(pair):
    tickers = client.get_orderbook_tickers()
    for x in tickers:
        if x['symbol'] == pair:
            return x

def cancel_orders(self, **params):
    return self._delete('openOrders', True, data=params)
def getbal(asset):
    balance = client.get_asset_balance(asset=asset)
    return balance

def getbidask(pair):
    tickers = client.get_orderbook_tickers()
    for x in tickers:
        if x['symbol'] == pair:
            return x

def process_message(msg):
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something

def prec(num, precise):
    return "{:0.0{}f}".format(num, precise)
from binance.websockets import BinanceSocketManager
# pr = BinanceSocketManager(client)
# pr.start_aggtrade_socket('USDCBUSD', process_message)
# pr.start()





current = 0
sessionprofit = 0
sessionstart = 0
while True:
    try:
        limbuy = 0
        limmid = 0
        limsell = 0
        USDCFREE = float(getbal('USDC')['free'])
        BUSDFREE = float(getbal('BUSD')['free'])
        avgprice = getpair('USDCBUSD')
        orders = client.get_open_orders(symbol='USDCBUSD')
        for x in orders:
            if x['price'] == '1.00010000':
                limsell += float(x['origQty'])
            elif x['price'] =='0.99990000':
                limbuy += float(x['origQty'])
            else:
                limmid += float(x['origQty'])
        USDCTOTAL = USDCFREE + limsell
        BUSDTOTAL = BUSDFREE + limbuy
        if sessionstart == 0:
            sessionstart = USDCTOTAL+BUSDTOTAL+limmid
        if USDCTOTAL+BUSDTOTAL+limmid>current:
            current = USDCTOTAL+BUSDTOTAL+limmid
            print('Total balance (including limits): $' + str(current))
            print('Session profit: $' + str(current-sessionstart))

        if USDCTOTAL-BUSDTOTAL>10 and USDCFREE > 10:
            try:
                order = client.order_limit_sell(
                    symbol='USDCBUSD',
                    quantity= floor(min(USDCFREE, (USDCTOTAL-BUSDTOTAL)/2)),
                    price='1.0000')
            except Exception as e:
                print(e)
        elif BUSDTOTAL-USDCTOTAL>10 and BUSDFREE > 10:
            try:
                order = client.order_limit_buy(
                    symbol='USDCBUSD',
                    quantity= floor(min(BUSDFREE, (BUSDTOTAL-USDCTOTAL)/2)),
                    price='1.0000')
            except Exception as e:
                print(e)
        if BUSDFREE>10:
            try:
                order = client.order_limit_buy(
                    symbol='USDCBUSD',
                    quantity=floor(BUSDFREE),
                    price='0.9999')
            except Exception as e:
                print(e)
        if USDCFREE>10:
            try:
                order = client.order_limit_sell(
                    symbol='USDCBUSD',
                    quantity=floor(USDCFREE),
                    price='1.0001')
            except Exception as e:
                print(e)
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(10)
