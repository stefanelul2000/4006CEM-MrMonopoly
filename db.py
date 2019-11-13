import pymongo
from pymongo import MongoClient
import os

db_user = os.environ.get('db_user')
db_pass = os.environ.get('db_pass')

cluster = MongoClient(f"mongodb+srv://{db_user}:{db_pass}@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster['stockDB']
collection = db["users"]

def member_join(post):
    collection.insert_one(post)

def member_already_joined(ajoin):
    result = collection.find({"_id":ajoin})
    for result in result:
        return(result["_id"])

def list_of_members():
    member_id_list = []
    result = collection.find().distinct('_id')
    for idKey in result:
       # member_id_list.append(result["_id"])
        member_id_list.append(idKey)

    return member_id_list

def get_name(userID):
    name = collection.find({"_id":userID},{"name":1})
    for username in name:
        name = username["name"]
    return name



def get_user_balance(userID):
    balance = collection.find({"_id":userID},{"balance":1})
    
    for money in balance:
        balance =money["balance"]
    return balance

def get_portfolio(userID):
    portfolio = collection.find({"_id":userID},{"stocks":1}) 

    for object in portfolio:
        new_portfolio = object["stocks"]
    return new_portfolio




    
def get_user_share_amount(userID,organisation):
    portfolio_dic = get_portfolio(userID)
    
    for stock_listing in portfolio_dic:   
        for v in portfolio_dic[stock_listing].keys():
            print(v)
            if v== "total_shares":
                shares_have =  portfolio_dic[organisation]["total_shares"]
                break

    return shares_have