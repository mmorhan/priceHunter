import datetime
from ta.trend import sma_indicator
import pandas as pd
import ccxt

def check():
    volumeSpikes=[]
    exchange = ccxt.binanceusdm()
    markets = exchange.load_markets()
    for i in markets:
        # every symbol taken here
        if i == "BTCSTUSDT":
            i = "BTC/USDT"
        bars = exchange.fetch_ohlcv(i, timeframe='5m', limit=50)
        data = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['sma_volume'] = sma_indicator(data['volume'], 20)
        data["symbol"] = i

        avgVolume = data['sma_volume'].iloc[len(data['sma_volume']) - 1]
        volume = data['volume'].iloc[len(data['volume']) - 1]
        print(f'Fecthing {i} {datetime.datetime.now().isoformat()} avgVolume: {avgVolume} Volume: {volume}')
        if volume > avgVolume * 2:
            print(i + " Volume Spike: " + str(avgVolume))
            # volume spike occurs notify here
            volumeSpikes.append([i,volume,avgVolume])


    print("Volume calculation over")
    return volumeSpikes