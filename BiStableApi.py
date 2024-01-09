import os
import time
from math import floor

from binance.client import Client

client = Client(os.getenv('api_key'), os.getenv('api_secret'))

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
# pr.start_aggtrade_socket('PAXBUSD', process_message)
# pr.start()



current = 0
sessionprofit = 0
sessionstart = 0
while True:
    try:
        limbuy = 0
        limmid = 0
        limsell = 0
        PAXFREE = float(getbal('PAX')['free'])
        BUSDFREE = float(getbal('BUSD')['free'])
        avgprice = getpair('PAXBUSD')
        orders = client.get_open_orders(symbol='PAXBUSD')
        # print(orders)
        for x in orders:
            if x['price'] == '1.00010000':
                limsell += float(float(x['origQty'])-float(x['executedQty']))
            elif x['price'] =='0.99990000':
                limbuy += float(float(x['origQty'])-float(x['executedQty']))
            else:
                limmid += float(float(x['origQty'])-float(x['executedQty']))
        PAXTOTAL = PAXFREE + limsell
        BUSDTOTAL = BUSDFREE + limbuy
        if sessionstart == 0:
            sessionstart = PAXTOTAL+BUSDTOTAL+limmid
        if PAXTOTAL+BUSDTOTAL+limmid>current:
            current = PAXTOTAL+BUSDTOTAL+limmid
            print('Total balance (including limits): $' + str(current))
            print('Session profit: $' + str(current-sessionstart))

        if PAXTOTAL-BUSDTOTAL>10 and PAXFREE > 10:
            try:
                order = client.order_limit_sell(
                    symbol='PAXBUSD',
                    quantity= floor(min(PAXFREE, (PAXTOTAL-BUSDTOTAL)/2)),
                    price='1.0000')
            except Exception as e:
                print(e)
        elif BUSDTOTAL-PAXTOTAL>10 and BUSDFREE > 10:
            try:
                order = client.order_limit_buy(
                    symbol='PAXBUSD',
                    quantity= floor(min(BUSDFREE, (BUSDTOTAL-PAXTOTAL)/2)),
                    price='1.0000')
            except Exception as e:
                print(e)
        if BUSDFREE>10:
            try:
                order = client.order_limit_buy(
                    symbol='PAXBUSD',
                    quantity=floor(BUSDFREE),
                    price='0.9999')
            except Exception as e:
                print(e)
        if PAXFREE>10:
            try:
                order = client.order_limit_sell(
                    symbol='PAXBUSD',
                    quantity=floor(PAXFREE),
                    price='1.0001')
            except Exception as e:
                print(e)
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(10)
