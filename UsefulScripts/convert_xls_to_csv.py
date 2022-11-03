import pandas as pd 

for i in range(0, 1):
    read_file = pd.read_excel("./SentimentData/sentiment.xls")
    read_file.to_csv("./SentimentData/sentiment.csv", index = None, header=True)