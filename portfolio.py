#Display portfolio
#pip install pymongo


import pymongo
from pymongo import MongoClient

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



add_stock_to_db(userID=267402605318242304 , date_today="2020-12-321", company_ticker='appl',shares= 108 , buy_price= 10000)







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