import pandas as pd
import ta

data = pd.read_csv("../TRADINGVIEW_DATA/data3.csv")
data = data.loc[::-1].reset_index(drop=True)
print(data.describe())

macd_ta = ta.trend.MACD(data["close"])
print(macd_ta.macd(), macd_ta.macd_signal(), macd_ta.macd_diff())

rsi_ta = ta.momentum.RSIIndicator(data["close"])
print(rsi_ta.rsi())

'''
def MACD(data, fast, slow, signal):    
    data2 = data["close"].copy()
    data2 = data2.to_frame()
    data2["ma_fast"] = data2["close"].ewm(span=fast,min_periods=fast).mean()
    data2["ma_slow"] = data2["close"].ewm(span=slow,min_periods=slow).mean()
    data2["macd"] = data2["ma_fast"] - data2["ma_slow"]
    data2["signal"] = data2["macd"].ewm(span=signal,min_periods=signal).mean()
    data2 = data2.dropna(axis=0, how='any')
    return data2

my_dic = MACD(data, 12, 26, 9)
ma_fast = my_dic["ma_fast"]
macd = my_dic["macd"]
signal = my_dic["signal"]
date = data["day"]
hour = data["hour"]
minute = data["minute"]


for i in range(33, 50):
    print(macd[i])
    #print(signal[i])
    print(date[i], hour[i], minute[i])
    #print(macd[i] - signal[i])


def rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data["close"].diff()

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")
'''

