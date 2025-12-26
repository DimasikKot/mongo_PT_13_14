from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["PT_13_14"]

pizzerias = db["pizzerias"]
cookbooks = db["cookbooks"]
