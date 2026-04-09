from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["debris_deputy"]

collection = db["reports"]

# Create TTL index on expires_at field
collection.create_index("expires_at", expireAfterSeconds=0)

print("✅ TTL index created successfully!")