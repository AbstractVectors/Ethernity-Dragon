import pandas as pd
import json
import requests
import datetime
import time

start_date = datetime.datetime.now()
target_date = datetime.datetime(2021, 10, 1)

BASE = "https://api.polygon.io/v2/aggs/ticker/X:ETHUSD/range/1/minute/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey=2CiMnHo26Rsl7EfHzQHNnASWAHcKUvLB"

df = pd.DataFrame(columns=['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n'])
while (start_date >= target_date):
    end_date = start_date - datetime.timedelta(days=33)
    print(end_date.strftime("%Y-%m-%d"))
    print(BASE.format(end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    resp = requests.get(BASE.format(end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d")))
    my_dic = resp.json()
    print(my_dic.keys())
    print(type(my_dic))
    my_df = pd.DataFrame(my_dic["results"])
    print(my_df)
    df = pd.concat([my_df, df]).reset_index(drop=True)
    time.sleep(10)
    start_date = end_date - datetime.timedelta(days=1)

['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n']
print(df)
try:
    open('../ETH_DATA/eth_minute_price.csv', 'x')
except:
    pass
file = open('../ETH_DATA/eth_minute_price.csv', 'w')
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
df.to_csv(file)