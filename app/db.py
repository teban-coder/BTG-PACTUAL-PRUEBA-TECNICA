from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["btg_db"]

users_collection = db["users"]
funds_collection = db["funds"]
transactions_collection = db["transactions"]
