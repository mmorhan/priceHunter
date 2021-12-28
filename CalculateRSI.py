
from ta import momentum
import datetime
import pandas as pd
import ccxt


def check():
    exchange = ccxt.binanceusdm()
    markets = exchange.load_markets()
    rsispikes=[]
    for i in markets:
        # every symbol taken here
        if i == "BTCSTUSDT":
            i = "BTC/USDT"
        bars = exchange.fetch_ohlcv(i, timeframe='5m', limit=50)
        data = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['rsi'] = momentum.rsi(data['close'])
        data["symbol"] = i

        rsivalue = data['rsi'].iloc[len(data['rsi']) - 1]
        print(f'Fecthing {i} {datetime.datetime.now().isoformat()} RSI: {rsivalue}')
        if rsivalue >= 70.0:
            print(i+ " Overbought RSI: " + str(rsivalue))
            rsispikes.append([i, rsivalue, 1])
        elif rsivalue < 30:
            print(i + " Oversold RSI: " + str(rsivalue))
            rsispikes.append([i, rsivalue, -1])

    print("Calculation for RSI over")
    return rsispikes
