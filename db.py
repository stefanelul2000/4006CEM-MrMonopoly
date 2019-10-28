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
