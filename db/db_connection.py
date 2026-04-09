from pymongo import MongoClient

# Replace with your MongoDB URI
MONGO_URI = "mongodb://localhost:27017/"

try:
    # Create connection
    client = MongoClient(MONGO_URI)

    # Create / connect to database
    db = client["debris_deputy"]

    print("✅ Connected to MongoDB successfully!")

except Exception as e:
    print("❌ Connection failed:", e)