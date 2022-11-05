import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
class make_data:
    def __init__(self, price_df, hours = 1, frequency = 1):
        self.adjust = hours * 60 // frequency
        self.df = price_df #df should have both price and tech data
        self.window = self.adjust // 2
        #print(self.window)
        #self.curr_df = self.df.loc[::self.window, :]
        self.curr_df = self.df
        #print(self.adjust)
        l = []
        #print(len(self.df.index))
        #print(len(self.curr_df['close']))
        flag = False
        print(self.adjust)
        #self.curr_df.reset_index(drop = True)
        self.curr_df['Y'] = 0
        print(self.window)
        for index, row in self.curr_df.iterrows():
            if len(self.curr_df['close']) < self.adjust + index:
                if not flag:
                    print(index)
                    flag = True
                #l.append([])
                continue
            if (index % self.window == 0):
                self.curr_df['Y'].iloc[index] = self.curr_df['close'].iloc[index + self.adjust]
                l.append(self.curr_df.iloc[index])
        self.finalDataFrame = pd.DataFrame(l)
        #print(self.finalDataFrame)
        #print(self.finalDataFrame[['close', 'Y']])
        self.finalDataFrame.to_csv("ETH_DATA/10_minute_ML_1_hour.csv")
class Model:
    def __init__(self, path):
        self.df = pd.read_csv(path)
    def linear_with_MACD(self):
        self.df = self.df.dropna(subset = ['macd_diff', 'close', 'Y'])
        X = self.df[['macd_diff', 'close']]  
        Y = self.df[['Y']]
        reg = LinearRegression().fit(X, Y)
        print(reg.coef_, reg.intercept_, reg.score(X, Y))
        #print(self.df['macd_diff'])
    def linear_with_rsi_perc(self):
        tempdf = self.df.dropna(subset = ['rsi_perc', 'close', 'Y', 'williams_r_perc'])
        X = tempdf[['rsi_perc', 'close', 'williams_r_perc']]
        Y = tempdf[['Y']]
        reg = LinearRegression().fit(X, Y)
        #print(self.df['macd_diff'])
        print(reg.coef_, reg.intercept_, reg.score(X, Y))
        #print(tempdf[['close', 'Y']])
price_data = pd.read_csv("ETH_DATA/eth_10_minute_price_techs.csv")
make_data(price_df = price_data, frequency = 10)
path = "ETH_DATA/10_minute_ML_1_hour.csv"
#m = Model(path)
#m.linear_with_rsi_perc()

