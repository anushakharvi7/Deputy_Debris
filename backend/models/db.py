from pymongo import MongoClient
from backend.config import Config

client = MongoClient(Config.MONGO_URI)
db = client["debris_deputy"]

# INSERT DATA FUNCTION
def insert_data(data):
    result = db.reports.insert_one(data)
    print("Inserted report ID:", result.inserted_id)