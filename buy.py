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

from datetime import datetime

db_user = os.environ.get('db_user')
db_pass = os.environ.get('db_pass')

cluster = MongoClient(f"mongodb+srv://{db_user}:{db_pass}@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["stockDB"]

collection = db["users"]

#Schema
post = {
"_id":5,
"balance":5000,
"stocks":{
    "appl":{
        "2017-10-1":{"price":200,"shares":10}
    },
    "googl":{
        "2019-10-1":{"price":1023,"shares":3},
        "2019-9-23":{"price":2000,"shares":2},
        }}}

#collection.insert_one(post)




def add_stock_to_db(userID,date_today,company_ticker,shares,buy_price,fresh_balance):

    shares = int(shares)
    total_shares = "total_shares"
    current_time_hms = datetime.now()

    current_time_hms = current_time_hms.strftime("%H:%M:%S")


    collection.update_one(
        {"_id":userID},
         {'$set':{"balance":fresh_balance,"stocks"+'.'+company_ticker +"."+ date_today+"."+current_time_hms:{"price": buy_price,"shares": shares}}},
          upsert = True
         
         )
    collection.update_one(
        {"_id":userID},
         {'$inc':{"stocks"+'.'+company_ticker+'.'+"total_shares":shares}}
         )
    # collection.update_one(
    #     {'$and':[{"_id":userID},{"stocks":{company_ticker:{}}}]},
    #      {'$inc':{"total_shares":shares}}
    #      )





#add_stock_to_db(userID=174900436363509761 , date_today="2018-10-4", company_ticker='appl',shares= 14 , buy_price= 453, fresh_balance=5000)



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






def buy_price(userInput):
    organisation , buy_quantity = analyse_text.process_text_buy(userInput)
    print('organ1',organisation)

    organisation = str(graph.company_name_converter(organisation))
    print('organ',organisation)

    stock_price = float(check_current_stock_price(organisation))
    buy_quantity = int(buy_quantity)
    

    buy_price= stock_price * buy_quantity

    return buy_price, organisation, buy_quantity
    


def get_user_balance(userID):
    balance = collection.find({"_id":userID},{"balance":1})
    
    for money in balance:
        balance =money["balance"]
    return balance



#print(get_user_balance(267402605318242304))

def buy_stock(userID,userInput):

    price_at_buy, organisation, buy_quantity = buy_price(userInput)

    user_bank = get_user_balance(userID)
    current_day =  datetime.today().strftime('%Y-%m-%d')
    new_balance = user_bank - price_at_buy
    if new_balance> -1 :
        print('You can buy ',buy_quantity," shares")
        add_stock_to_db(userID,date_today=current_day,company_ticker=organisation,shares=buy_quantity,buy_price=price_at_buy, fresh_balance = new_balance )
    
    else:
        print("Can't buy")



    
    
   
    




#buy_stock(267402605318242304,"buy 3 shares in Amazon Inc")

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