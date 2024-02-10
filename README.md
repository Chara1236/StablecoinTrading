

## Installing

```
pip install python-binance
```

### Api usage:
Functions in the script which utilize binance API
```
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

```

### Setup
In BiAlt.py put your api key/secret into and you should be able to run it:

```
api_key='insert key'
api_secret= 'insert secret'
```

### Data
Each during each session, the code will provide you with 3 values

```
current = 0 #current balance in USD
sessionprofit = 0 $session profit in USD
sessionstart = 0 #how much your was in your balance at the start of the session in USD
```

The theory behind this script is that stablecoins should be pegged to a certain value. However in reality the stablecoins see slight fluctuations and since they should be pegged to a certain value, you can assume
the price of the coin will frequently return to it's pegged price. Thus it is very easy to see if a coin is over/undervalued which brings upon a arbitrage opportunity. 

Of course in reality this relatively simple script is probably not the most effective investment strategy for several reasons including lack of opportunities due to trading fees and stablecoins not actually being risk-free
(Like how some believe USDT to be a sort of ponzi).

Stablecoins used: PAX, BUSD, USDT, USDC, DAI




No longer functional in places where Binance doesn't operate.
