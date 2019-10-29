#Display portfolio
#pip install pymongo


import pymongo
from pymongo import MongoClient
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries as ts
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import random
import os
import analyse_text
import numpy as np
import matplotlib.dates 
import analyse_text
import graph

cluster = MongoClient("mongodb+srv://masooda6:ilovemongodb123@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["stockDB"]

collection = db["users"]


post = {
"_id":5,
"balance":5000,
"stocks":{
    "appl":{},
    "googl":{
        "2019-10-1":{"price":1023,"shares":3},
        "2019-9-23":{"price":2000,"shares":2},
        }}}

#collection.insert_one(post)




def add_stock_to_db(userID,date_today,company_ticker,shares,buy_price):
    collection.update_one(
        {"_id":userID},
         {'$set':{"stocks"+'.'+company_ticker:{date_today:{"price": buy_price,"shares": shares}}}},
          upsert = True
         
         )


#add_stock_to_db(userID=267402605318242304 , date_today="2020-12-321", company_ticker='appl',shares= 108 , buy_price= 10000)


def check_current_stock_price(ticker):
    API_KEY = graph.generate_api_key()
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

"""
    closing_list = []
    dates = []

    days_get = days
    count = 0

    for day in results['Time Series (Daily)']:
        
        if count == days_get:
                break
        dt = datetime.datetime.strptime(day, '%Y-%m-%d').strftime('%d/%m')
        dates.append(dt)
       # dates.append(day)
        closing_list.append(float(results['Time Series (Daily)'][day]['4. close']))
        
        count += 1
    dates.reverse()
    closing_list.reverse()
    return dates,closing_list


"""










def buy_stock(userInput):
    organisation , buy_quantity = analyse_text.process_text_buy(userInput)
    organisation = str(graph.company_name_converter(organisation))
    print(organisation)

    stock_price = float(check_current_stock_price(organisation))
    buy_quantity = int(buy_quantity)
    

    buy_price= stock_price * buy_quantity

   
    




buy_stock("buy 5 shares in Apple Inc")

"""

collection.update_one(
        {"_id":userID},
         {'$set':{"stocks":
         {
         company_ticker:{
        
        "price": buy_price,
        "shares": shares


         }    

         }
         
          }},
          upsert = True
         
         )



"""