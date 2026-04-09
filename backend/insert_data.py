from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta, UTC
import uuid
import os

from utils.hash_utils import generate_hash

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["debris_deputy"]
collection = db["reports"]

# Ensure unique index (run once, safe if repeated)
collection.create_index("image_hash", unique=True)


def generate_filename(image_hash, extension="jpg"):
    return f"{image_hash}_{uuid.uuid4()}.{extension}"


def insert_report(image_path, lat, lng):
    try:
        # ✅ Check file exists
        if not os.path.exists(image_path):
            print("❌ Image file not found!")
            return

        # ✅ Generate image hash
        image_hash = generate_hash(image_path)

        # 🔍 Optional quick duplicate check
        if collection.find_one({"image_hash": image_hash}):
            print("⚠️ Duplicate report detected! Not inserting.")
            return

        # ✅ Generate unique filename
        filename = generate_filename(image_hash)
        stored_path = f"uploads/{filename}"

        # (Optional) You can move/rename file here if needed

        # ✅ Time fields
        current_time = datetime.now(UTC)
        expiry_time = current_time + timedelta(hours=48)

        # ✅ Data document
        data = {
            "image_url": stored_path,
            "location": {
                "lat": lat,
                "lng": lng
            },
            "status": "pending",
            "created_at": current_time,
            "expires_at": expiry_time,
            "image_hash": image_hash
        }

        # ✅ Insert into DB
        result = collection.insert_one(data)
        print("✅ Report inserted with ID:", result.inserted_id)

    except DuplicateKeyError:
        print("⚠️ Duplicate detected (DB level)!")

    except Exception as e:
        print("❌ Error:", e)


# 🔥 Test
insert_report("uploads/test.jpg", 12.9716, 77.5946)