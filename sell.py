import pymongo
from pymongo import MongoClient
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries as ts
from alpha_vantage.techindicators import TechIndicators
import random
import os
import analyse_text
import graph
from datetime import datetime
import db

def check_current_stock_price(ticker):
    API_KEY = graph.generate_api_key()
    print(ticker)
   # print(API_KEY)

    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=5min&apikey=demo'+API_KEY)
    results = r.json()

   # print(results)
    count = 0

    for recent in results['Time Series (5min)']:
        if count == 1:
                break
        
        last_price = results['Time Series (5min)'][recent]['4. close']
        count += 1

    return last_price

def get_user_balance(userID):
    balance = collection.find({"_id":userID},{"balance":1})
    
    for money in balance:
        balance =money["balance"]
    return balance

def update_balance(userID):
    
    new_balance = get_user_balance(userID) + sell_price
    
    return new_balance



# def extract_stock(userID, ):
    
#     collection.update_one(
#         {"_id":userID},
#          {collection.delete_one({})
         
#          )




def sell_price(userInput):

    selling_quantity , organisation = analyse_text.process_text_buy(userInput)
    organisation = str(graph.company_name_converter(organisation))

    stock_price = float(check_current_stock_price(orsganisation))
    selling_quantity = int(selling_quantity)
    
    selling_price= stock_price * selling_quantity

    return selling_price , organisation, selling_quantity

def sell_stock(userID,userInput):
    price_at_sell, organisation, sell_quantity = sell_price(userInput)

    current_day =  datetime.today().strftime('%Y-%m-%d')
    new_balance = update_balance(userID)
    
    if sell_quantity>0:
        print('You sold ',sell_quantity," shares")
        extract_stock()
        
    else:
        print('Sorry, you cannot sell that ammount')