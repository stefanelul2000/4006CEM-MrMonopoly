import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://discord:pydiscord@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster['stockDB']
collection = db["users"]

def member_join(post):
    collection.insert_one(post)

def member_already_joined(ajoin):
    result = collection.find({"_id":ajoin})
    for result in result:
        return(result["_id"])

def get_user_balance(userID):
    balance = collection.find({"_id":userID},{"balance":1})
    
    for money in balance:
        balance =money["balance"]
    return balance

def get_portfolio(userID):
    portfolio = collection.find({"_id":userID},{"stocks":1}) 

    for object in portfolio:
        new_portfolio = object["stocks"]
        #print(new_portfolio)
    return new_portfolio

    