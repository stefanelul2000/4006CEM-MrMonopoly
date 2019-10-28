#Display portfolio
#pip install pymongo


import pymongo
from pymongo import mongo_client

cluster = mongo_client("mongodb+srv://masooda6:ilovemongodb123@cluster0-fkl2z.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["stockDB"]

collection = db["users"]
