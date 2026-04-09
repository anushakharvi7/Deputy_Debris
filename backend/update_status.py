from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["debris_deputy"]
collection = db["reports"]


def update_status(report_id, new_status):
    try:
        # ✅ Validate ObjectId
        if not ObjectId.is_valid(report_id):
            print("❌ Invalid ObjectId format!")
            return

        # ✅ Validate status
        allowed_status = ["pending", "confirmed", "rejected"]
        if new_status not in allowed_status:
            print("❌ Invalid status! Use: pending / confirmed / rejected")
            return

        # ✅ Update query
        result = collection.update_one(
            {"_id": ObjectId(report_id)},
            {"$set": {"status": new_status}}
        )

        # ✅ Check result
        if result.matched_count == 0:
            print("❌ Report not found!")
        else:
            print("✅ Status updated successfully!")

    except Exception as e:
        print("❌ Error:", e)


# 🔥 Test (replace with your real ID)
update_status("69d6735b31d17afc438d1d26", "confirmed")