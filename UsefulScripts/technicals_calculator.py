import pandas as pd
import numpy as np
import ta


time_interval = input("Input the time interval: ")
time_unit = input("Input the time unit (minute or hour): ")
PATH = "../ETH_DATA/eth_{}_{}_price.csv"

data = pd.read_csv(PATH.format(time_interval, time_unit))

def calc_tech_perc(tech_data):
    tech_data_sorted = tech_data.sort_values(ascending=True)
    tech_data_sorted = tech_data_sorted.dropna()
    tech_data_length = len(tech_data_sorted)
    tech_perc = []
    for tech in tech_data:
        if (tech is None):
            tech_perc.append(None)
        else:
            tech_perc.append(tech_data_sorted.searchsorted(tech, side='left') / tech_data_length)
    return tech_perc

macd_ta = ta.trend.MACD(data["close"])
data['macd'] = macd_ta.macd()
data['macd_signal'] = macd_ta.macd_signal()
data['macd_diff'] = macd_ta.macd_diff()

rsi_ta = ta.momentum.RSIIndicator(close=data["close"])
rsi = rsi_ta.rsi()
data['rsi'] = rsi
data['rsi_perc'] = calc_tech_perc(rsi)

stoch_osc_ta = ta.momentum.StochasticOscillator(high=data["high"], low=data["low"], close=data["close"])
data['stoch_k'] = stoch_osc_ta.stoch()
stoch_k_signal = stoch_osc_ta.stoch_signal()
data['stoch_k_signal'] = stoch_k_signal
data['stoch_k_signal_perc'] = calc_tech_perc(stoch_k_signal)

williams_r_ta = ta.momentum.WilliamsRIndicator(high=data["high"], low=data["low"], close=data["close"])
data['williams_r'] = williams_r_ta.williams_r()
data['williams_r_perc'] = calc_tech_perc(data['williams_r'])

stoch_rsi_ta = ta.momentum.StochRSIIndicator(close=data["close"])
data['stoch_rsi'] = stoch_rsi_ta.stochrsi()
data['stoch_rsi'] = calc_tech_perc(data['stoch_rsi'])

sma_50_ta = ta.trend.SMAIndicator(close=data["close"], window=50)
data['50_sma'] = sma_50_ta.sma_indicator()
sma_100_ta = ta.trend.SMAIndicator(close=data["close"], window=100)
data['100_sma'] = sma_100_ta.sma_indicator()

ema_50_ta = ta.trend.EMAIndicator(close=data["close"], window=50)
data['50_ema'] = ema_50_ta.ema_indicator()
ema_100_ta = ta.trend.EMAIndicator(close=data["close"], window=100)
data['100_ema'] = ema_100_ta.ema_indicator()


file_path = '../ETH_DATA/eth_{}_{}_price_techs.csv'.format(time_interval, time_unit)
try:
    open(file_path, 'x')
except:
    pass
file = open(file_path, 'w')

data.to_csv(file, index=False)


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
