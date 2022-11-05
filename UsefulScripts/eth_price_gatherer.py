import pandas as pd
import json
import requests
import datetime
import time

start_date = datetime.datetime.now()
target_date = datetime.datetime(2021, 10, 1)
time_interval = input("Input the time interval: ")
time_unit = input("Input the time unit (minute or hour): ")

BASE = "https://api.polygon.io/v2/aggs/ticker/X:ETHUSD/range/{}/{}/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey=2CiMnHo26Rsl7EfHzQHNnASWAHcKUvLB"
PATH = "../ETH_DATA/eth_{}_{}_price.csv"

df = pd.DataFrame(columns=['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n'])
while (start_date >= target_date):
    end_date = start_date - datetime.timedelta(days=33)
    print(end_date.strftime("%Y-%m-%d"))
    print(BASE.format(time_interval, time_unit, end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    resp = requests.get(BASE.format(time_interval, time_unit, end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    my_dic = resp.json()
    print(my_dic.keys())
    print(type(my_dic))
    my_df = pd.DataFrame(my_dic["results"])
    print(my_df)
    df = pd.concat([my_df, df]).reset_index(drop=True)
    time.sleep(15)
    start_date = end_date - datetime.timedelta(days=1)

print(df)

path = PATH.format(time_interval, time_unit)
try:
    open(path, 'x')
except:
    pass
file = open(path, 'w')
df.rename(
    columns=({ 'v': 'volume', 
               'vw': 'volume_weighted_average_price',
               'o': 'open',
               'c': 'close',
               'h': 'high',
               'l': 'low',
               't': 'time',
               'n': 'number_transactions'}), 
    inplace=True,
)
df.to_csv(file, index=False)