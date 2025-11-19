import requests
import json 
import pandas as pd
import yfinance as yf
import math
import os


api_key = "ei26dGai7uqdGGGNW2Yi1A==CvCc8foCg3JDAmra" #add api-ninjas api key
url = f"https://api.api-ninjas.com/v1/sp500"
headers= {'X-Api-Key': api_key}
request = requests.get(url, headers=headers)
data = request.json()
#print(json.dumps(data, indent=2))


stocks = []
for i in data:
    stocks.append(i["ticker"])
for i, t in enumerate(stocks):
    stocks[i] = t.replace(".", "-")
ticker_list = " ".join(stocks)


tickers = yf.Tickers(ticker_list)

my_columns = ['Ticker', 'Price', 'MarketCap', 'suggested shares to buy']
actual_dataframe = pd.DataFrame(columns=my_columns)

while True:
    try:
        porfolio_amount = float(input("what is you rportfolio amount:"))
        break
    except ValueError:
        print("Please enter a valid number")
while True:        
    try:
        csv_file_name = input("what is the name of the csv file:")
        if csv_file_name.endswith(".csv"):
            print("filename should not have .csv extension")
            continue
        else:
            break
    except ValueError:
        print("Please enter a valid name")

for stock in stocks:
    info = tickers.tickers[stock].info or {}
    actual_dataframe.loc[len(actual_dataframe)] = [stock, info.get('currentPrice'), info.get('marketCap'), 'N/A']

# Coerce to numeric so blanks/None → NaN, then drop and reset index
actual_dataframe['Price'] = pd.to_numeric(actual_dataframe['Price'], errors='coerce')
actual_dataframe['MarketCap'] = pd.to_numeric(actual_dataframe['MarketCap'], errors='coerce')
actual_dataframe = actual_dataframe.dropna(subset=['Price', 'MarketCap']).reset_index(drop=True)

position_size = porfolio_amount / len(actual_dataframe) #how much money reserved for each stock
for i in range(0, len(actual_dataframe.index)):
        actual_dataframe.loc[i, 'suggested shares to buy'] = math.floor(position_size / actual_dataframe.loc[i, 'Price'])
print(actual_dataframe)

path = f"./{csv_file_name}.csv"
actual_dataframe.to_csv(path, mode="a", header=not os.path.exists(path), index=True)
