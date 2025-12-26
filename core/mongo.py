from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["practice_db"]

pizzerias = db["pizzerias"]
cookbooks = db["cookbooks"]
