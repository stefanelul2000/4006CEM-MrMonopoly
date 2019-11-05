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
import db as databaseOwn
import buy



cluster = MongoClient("mongodb+srv://masooda6:ilovemongodb123@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["stockDB"]

collection = db["users"]

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


def add_balance_to_db(userID,date_today,company_ticker,shares,buy_price,fresh_balance):

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

def get_user_balance(userID):
    balance = collection.find({"_id":userID},{"balance":1})
    
    for money in balance:
        balance =money["balance"]
    return balance

def update_balance(userID,sell_price):
    
    new_balance = get_user_balance(userID) + sell_price
    
    return new_balance



# def extract_stock(userID, ):
    
#     collection.update_one(
#         {"_id":userID},
#          {collection.delete_one({})
         
#          )




def sell_price(userInput):

    organisation, selling_quantity  = analyse_text.process_text_buy(userInput)
    print('sell org before ticker', organisation)
    organisation = str(graph.company_name_converter(organisation))
    print('sell org', organisation)

    # stock_price = float(check_current_stock_price(organisation))

    stock_price = float(buy.check_current_stock_price(organisation))
    selling_quantity = int(selling_quantity)
    
    selling_price= stock_price * selling_quantity

    return selling_price , organisation, selling_quantity

def sell_stock(userID,userInput):
    price_at_sell, organisation, sell_quantity = sell_price(userInput)

    shares_in_port = databaseOwn.get_user_share_amount(userID,organisation)

    print('price at sell',price_at_sell)




    
    
    if sell_quantity<=shares_in_port:
        print('You sold ',sell_quantity," shares")
        current_day =  datetime.today().strftime('%Y-%m-%d')
        new_balance = update_balance(userID,price_at_sell)
        current_day =  datetime.today().strftime('%Y-%m-%d')
        sell_quantity =-sell_quantity
        add_balance_to_db(userID,current_day,organisation,sell_quantity,price_at_sell,new_balance)
        return True
        #extract_stock()
        
    else:
        print('Sorry, you cannot sell that ammount')